import re
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
# from src.models.state import ErrorAnalysis, DebugStatus
from src.models.schemas import ErrorAnalysis, DebugStatus

class ErrorAnalysisOutput(BaseModel):
    error_type: str = Field(description="Type of error (e.g., SyntaxError, TypeError, etc.)")
    error_location: str = Field(description="Where the error occurs (line number, function, etc.)")
    root_cause: str = Field(description="Root cause explanation")
    severity: str = Field(description="Error severity: low, medium, high, critical")
    affected_lines: list[int] = Field(description="List of line numbers affected by the error")

class ParserAgent:
    def __init__(self, llm_model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.1)
        self.output_parser = PydanticOutputParser(pydantic_object=ErrorAnalysisOutput)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code parser and error analyst. Your job is to:
            1. Analyze the provided code and error log
            2. Identify the root cause of the error
            3. Determine error severity and affected code sections
            4. Provide clear, actionable insights
            
            Be precise and thorough in your analysis.
            
            {format_instructions}"""),
            ("user", """
            Code to analyze:
            ```
            {code}
            ```
            
            Error log:
            ```
            {error_log}
            ```
            
            Please provide a comprehensive analysis of this error.
            """)
        ])
    
    def parse_error(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and analyze the error from code and error log"""
        
        # Format the prompt
        formatted_prompt = self.prompt.format_messages(
            code=state["original_code"],
            error_log=state["error_log"],
            format_instructions=self.output_parser.get_format_instructions()
        )
        
        # Get LLM response
        response = self.llm.invoke(formatted_prompt)
        
        # Parse the output
        try:
            parsed_output = self.output_parser.parse(response.content)
            
            # Create ErrorAnalysis object
            error_analysis = ErrorAnalysis(
                error_type=parsed_output.error_type,
                error_location=parsed_output.error_location,
                root_cause=parsed_output.root_cause,
                severity=parsed_output.severity,
                affected_lines=parsed_output.affected_lines
            )
            
            # Update state
            state["error_analysis"] = error_analysis
            state["status"] = DebugStatus.FIXING
            state["reasoning_steps"].append(f"Parser: Identified {error_analysis.error_type} at {error_analysis.error_location}")
            
        except Exception as e:
            state["status"] = DebugStatus.FAILED
            state["reasoning_steps"].append(f"Parser: Failed to parse error - {str(e)}")
        
        return state