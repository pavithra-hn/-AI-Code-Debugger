from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
# from src.models.state import DebugStatus
from src.models.schemas import  DebugStatus

class ReviewOutput(BaseModel):
    is_fix_valid: bool = Field(description="Whether the fix is valid and addresses the error")
    review_feedback: str = Field(description="Detailed feedback on the fix")
    confidence_score: float = Field(description="Confidence in the review (0-1)", ge=0, le=1)
    suggestions: str = Field(description="Additional suggestions or improvements")

class ReviewerAgent:
    def __init__(self, llm_model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.1)
        self.output_parser = PydanticOutputParser(pydantic_object=ReviewOutput)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code reviewer and validator. Your job is to:
            1. Review the proposed fix against the original error
            2. Validate that the fix addresses the root cause
            3. Check for potential new issues or side effects
            4. Provide constructive feedback
            
            Be thorough and critical in your review.
            Consider edge cases and potential improvements.
            
            {format_instructions}"""),
            ("user", """
            Original code:
            ```
            {original_code}
            ```
            
            Original error: {error_log}
            
            Proposed fix:
            ```
            {fixed_code}
            ```
            
            Fix explanation: {fix_explanation}
            
            Error analysis:
            - Error Type: {error_type}
            - Root Cause: {root_cause}
            
            Please review this fix and determine if it's valid and complete.
            """)
        ])
    
    def review_fix(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Review the proposed fix"""
        
        if not state.get("current_fix") or not state.get("error_analysis"):
            state["status"] = DebugStatus.FAILED
            state["reasoning_steps"].append("Reviewer: Missing fix or error analysis")
            return state
        
        current_fix = state["current_fix"]
        error_analysis = state["error_analysis"]
        
        # Format the prompt
        formatted_prompt = self.prompt.format_messages(
            original_code=current_fix.original_code,
            error_log=state["error_log"],
            fixed_code=current_fix.fixed_code,
            fix_explanation=current_fix.explanation,
            error_type=error_analysis.error_type,
            root_cause=error_analysis.root_cause,
            format_instructions=self.output_parser.get_format_instructions()
        )
        
        # Get LLM response
        response = self.llm.invoke(formatted_prompt)
        
        # Parse the output
        try:
            parsed_output = self.output_parser.parse(response.content)
            
            # Update state based on review
            state["review_feedback"] = parsed_output.review_feedback
            state["reasoning_steps"].append(f"Reviewer: {'Approved' if parsed_output.is_fix_valid else 'Rejected'} fix")
            
            if parsed_output.is_fix_valid:
                state["status"] = DebugStatus.COMPLETED
                state["final_result"] = current_fix
                state["reasoning_steps"].append("Reviewer: Fix approved - debugging complete")
            else:
                state["iteration_count"] += 1
                if state["iteration_count"] >= state["max_iterations"]:
                    state["status"] = DebugStatus.FAILED
                    state["reasoning_steps"].append("Reviewer: Max iterations reached")
                else:
                    state["status"] = DebugStatus.FIXING
                    state["reasoning_steps"].append(f"Reviewer: Fix rejected, iteration {state['iteration_count']}")
                    # Add feedback to help the next fix attempt
                    state["reasoning_steps"].append(f"Feedback: {parsed_output.review_feedback}")
                    
        except Exception as e:
            state["status"] = DebugStatus.FAILED
            state["reasoning_steps"].append(f"Reviewer: Failed to review fix - {str(e)}")
        
        return state