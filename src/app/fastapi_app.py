from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.workflow.debug_workflow import DebugWorkflow

load_dotenv()

app = FastAPI(title="AI Code Debugger API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DebugRequest(BaseModel):
    code: str
    error_log: str
    max_iterations: int = 3
    api_key: str

class DebugResponse(BaseModel):
    success: bool
    fixed_code: str
    explanation: str
    is_fixed: bool
    iteration_count: int
    identified_issues: list
    error_message: str = None

@app.post("/debug", response_model=DebugResponse)
async def debug_code(request: DebugRequest):
    """Debug code using multi-agent workflow"""
    try:
        # Initialize workflow
        workflow = DebugWorkflow(request.api_key)
        
        # Run debugging
        result = workflow.debug_code(
            request.code,
            request.error_log,
            request.max_iterations
        )
        
        return DebugResponse(
            success=True,
            fixed_code=result.current_code,
            explanation=result.final_explanation,
            is_fixed=result.is_fixed,
            iteration_count=result.iteration_count,
            identified_issues=result.identified_issues
        )
        
    except Exception as e:
        return DebugResponse(
            success=False,
            fixed_code="",
            explanation="",
            is_fixed=False,
            iteration_count=0,
            identified_issues=[],
            error_message=str(e)
        )

@app.get("/")
async def root():
    return {"message": "AI Code Debugger API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)