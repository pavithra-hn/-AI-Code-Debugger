from typing import List, Dict, Optional, TypedDict
from dataclasses import dataclass
from enum import Enum

class DebugStatus(Enum):
    PARSING = "parsing"
    FIXING = "fixing"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class CodeFix:
    original_code: str
    fixed_code: str
    explanation: str
    confidence_score: float
    changes_summary: str

@dataclass
class ErrorAnalysis:
    error_type: str
    error_location: str
    root_cause: str
    severity: str
    affected_lines: List[int]

class DebugState(TypedDict):
    original_code: str
    error_log: str
    current_code: str
    error_analysis: Optional[ErrorAnalysis]
    proposed_fixes: List[CodeFix]
    current_fix: Optional[CodeFix]
    review_feedback: Optional[str]
    status: DebugStatus
    iteration_count: int
    max_iterations: int
    reasoning_steps: List[str]
    final_result: Optional[CodeFix]




