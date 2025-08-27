from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
# from src.models.state import CodeFix, DebugStatus
from src.models.schemas import CodeFix, DebugStatus

class CodeFixOutput(BaseModel):
    fixed_code: str = Field(description="The corrected code")
    explanation: str = Field(description="Detailed explanation of what was fixed and why")
    confidence_score: float = Field(description="Confidence in the fix (0-1)", ge=0, le=1)
    changes_summary: str = Field(description="Summary of changes made")

class FixerAgent:
    def __init__(self, llm_model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.2)
        self.output_parser = PydanticOutputParser(pydantic_object=CodeFixOutput)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code fixer. Your job is to:
            1. Take the error analysis and original code
            2. Generate a corrected version of the code
            3. Provide clear explanations for your fixes
            4. Ensure the fix addresses the root cause
            
            Focus on minimal, precise changes that solve the problem.
            Maintain code style and structure where possible.
            
            {format_instructions}"""),
            ("user", """
            Original code:
            ```
            {original_code}
            ```
            
            Error Analysis:
            - Error Type: {error_type}
            - Location: {error_location}
            - Root Cause: {root_cause}
            - Severity: {severity}
            - Affected Lines: {affected_lines}
            
            Please provide a fix for this code that addresses the identified error.
            """)
        ])
    
    def generate_fix(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a code fix based on error analysis"""
        
        if not state.get("error_analysis"):
            state["status"] = DebugStatus.FAILED
            state["reasoning_steps"].append("Fixer: No error analysis available")
            return state
        
        error_analysis = state["error_analysis"]
        
        # Format the prompt
        formatted_prompt = self.prompt.format_messages(
            original_code=state["original_code"],
            error_type=error_analysis.error_type,
            error_location=error_analysis.error_location,
            root_cause=error_analysis.root_cause,
            severity=error_analysis.severity,
            affected_lines=error_analysis.affected_lines,
            format_instructions=self.output_parser.get_format_instructions()
        )
        
        # Get LLM response
        response = self.llm.invoke(formatted_prompt)
        
        # Parse the output
        try:
            parsed_output = self.output_parser.parse(response.content)
            
            # Create CodeFix object
            code_fix = CodeFix(
                original_code=state["original_code"],
                fixed_code=parsed_output.fixed_code,
                explanation=parsed_output.explanation,
                confidence_score=parsed_output.confidence_score,
                changes_summary=parsed_output.changes_summary
            )
            
            # Update state
            state["current_fix"] = code_fix
            state["proposed_fixes"].append(code_fix)
            state["current_code"] = parsed_output.fixed_code
            state["status"] = DebugStatus.REVIEWING
            state["reasoning_steps"].append(f"Fixer: Generated fix with {parsed_output.confidence_score:.2f} confidence")
            
        except Exception as e:
            state["status"] = DebugStatus.FAILED
            state["reasoning_steps"].append(f"Fixer: Failed to generate fix - {str(e)}")
        
        return state
