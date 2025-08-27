from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from src.agents.parser_agent import ParserAgent
from src.agents.fixer_agent import FixerAgent
from src.agents.reviewer_agent import ReviewerAgent
# from src.models.state import DebugState, DebugStatus
from src.models.schemas import DebugState, DebugStatus

class DebugWorkflow:
    def __init__(self, llm_model: str = "gpt-4"):
        self.parser_agent = ParserAgent(llm_model)
        self.fixer_agent = FixerAgent(llm_model)
        self.reviewer_agent = ReviewerAgent(llm_model)
        
        # Build the workflow graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        workflow = StateGraph(DebugState)
        
        # Add nodes
        workflow.add_node("parser", self.parser_agent.parse_error)
        workflow.add_node("fixer", self.fixer_agent.generate_fix)
        workflow.add_node("reviewer", self.reviewer_agent.review_fix)
        
        # Add edges
        workflow.add_edge("parser", "fixer")
        workflow.add_edge("fixer", "reviewer")
        
        # Add conditional edges from reviewer
        workflow.add_conditional_edges(
            "reviewer",
            self._should_continue,
            {
                "continue": "fixer",  # Go back to fixer for another iteration
                "end": END           # End the workflow
            }
        )
        
        # Set entry point
        workflow.set_entry_point("parser")
        
        return workflow.compile()
    
    def _should_continue(self, state: Dict[str, Any]) -> str:
        """Determine if workflow should continue or end"""
        status = state.get("status")
        
        if status in [DebugStatus.COMPLETED, DebugStatus.FAILED]:
            return "end"
        elif status == DebugStatus.FIXING:
            return "continue"
        else:
            return "end"
    
    def debug_code(self, code: str, error_log: str, max_iterations: int = 3) -> Dict[str, Any]:
        """Run the debugging workflow"""
        
        # Initialize state
        initial_state = {
            "original_code": code,
            "error_log": error_log,
            "current_code": code,
            "error_analysis": None,
            "proposed_fixes": [],
            "current_fix": None,
            "review_feedback": None,
            "status": DebugStatus.PARSING,
            "iteration_count": 0,
            "max_iterations": max_iterations,
            "reasoning_steps": [],
            "final_result": None
        }
        
        # Run the workflow
        result = self.graph.invoke(initial_state)
        
        return result