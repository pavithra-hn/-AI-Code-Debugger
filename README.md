# 🐛 AI Code Debugger

An autonomous debugging assistant powered by LangGraph and multi-agent AI workflows that analyzes code, identifies errors, and provides intelligent fixes through collaborative AI agents.

## 🎯 Overview

The AI Code Debugger uses three specialized AI agents working in harmony:

- **🔍 Parser Agent**: Analyzes code and error logs to understand the root cause
- **🔧 Fixer Agent**: Generates intelligent code fixes based on the analysis  
- **✅ Reviewer Agent**: Validates fixes and provides feedback for improvement

The system runs in a feedback loop until a satisfactory solution is found or maximum iterations are reached.

## ✨ Features

- **Multi-Agent Workflow**: Three specialized AI agents collaborate to solve coding issues
- **Intelligent Error Analysis**: Deep understanding of error types, locations, and root causes
- **Iterative Improvement**: Continuous refinement through reviewer feedback loops
- **Explainable AI**: Clear reasoning steps and confidence scores for all fixes
- **Web Interface**: User-friendly Streamlit app for easy interaction
- **Docker Support**: Containerized deployment for scalability
- **Multiple LLM Support**: Works with GPT-4, GPT-3.5, and other OpenAI models

## 🏗️ Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Parser Agent  │───▶│   Fixer Agent   │───▶│ Reviewer Agent │
│                 │    │                 │    │                 │
│ • Error Analysis│    │ • Solution Gen  │    │ • Quality Check │
│ • Issue Extract │    │ • Code Fixing   │    │ • Validation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────────────────┐
                    │      LangGraph Workflow     │
                    │                             │
                    │ • State Management          │
                    │ • Conditional Routing       │
                    │ • Iteration Control         │
                    └─────────────────────────────┘
```
## Project Structure
```
ai-code-debugger/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── parser_agent.py
│   │   ├── fixer_agent.py
│   │   └── reviewer_agent.py
│   ├── workflow/
│   │   ├── __init__.py
│   │   └── debug_workflow.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── app/
│       ├── __init__.py
│       └── streamlit_app.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```
## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pavithra-hn/ai-code-debugger.git
   cd ai-code-debugger
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Run the application**
   ```bash
   streamlit run src/app/streamlit_app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the app** at `http://localhost:8501`

## 📖 Usage Guide

### Web Interface

1. **Enter API Key**: Add your OpenAI API key in the sidebar
2. **Configure Settings**: Choose your model and max iterations
3. **Input Code**: Paste your buggy code in the left panel
4. **Add Error Log**: Paste the error message/traceback in the right panel
5. **Debug**: Click "Debug Code" and watch the AI agents work
6. **Review Results**: Examine the fix, analysis, and reasoning process

### Example Usage

**Input Code:**
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# Test with empty list
result = calculate_average([])
print(result)
```

**Error Log:**
```
Traceback (most recent call last):
  File "test.py", line 8, in <module>
    result = calculate_average([])
  File "test.py", line 5, in calculate_average
    return total / len(numbers)
ZeroDivisionError: division by zero
```

**AI-Generated Fix:**
```python
def calculate_average(numbers):
    if not numbers:  # Handle empty list
        return 0  # or raise ValueError("Cannot calculate average of empty list")
    
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# Test with empty list
result = calculate_average([])
print(result)  # Output: 0
```

### Programmatic Usage

```python
from src.workflow.debug_workflow import DebugWorkflow
import os

# Set up API key
os.environ["OPENAI_API_KEY"] = "your-api-key"

# Initialize workflow
debugger = DebugWorkflow(llm_model="gpt-4")

# Debug code
result = debugger.debug_code(
    code="""
    def divide_numbers(a, b):
        return a / b
    
    result = divide_numbers(10, 0)
    """,
    error_log="ZeroDivisionError: division by zero",
    max_iterations=3
)

# Access results
if result["final_result"]:
    print("Fixed code:", result["final_result"].fixed_code)
    print("Explanation:", result["final_result"].explanation)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `DEFAULT_MODEL` | Default LLM model | `gpt-4` |
| `TEMPERATURE` | LLM temperature setting | `0.1` |
| `MAX_ITERATIONS` | Maximum fix attempts | `3` |
| `DEBUG_MODE` | Enable debug logging | `false` |

### Model Selection

Supported models:
- `gpt-4` (Recommended)
- `gpt-4o-mini`
- `gpt-3.5-turbo`

Higher-tier models provide better analysis and fixes but cost more.

## 🏛️ System Design

### Agent Responsibilities

#### Parser Agent 🔍
- **Input**: Source code + error log
- **Output**: Structured error analysis
- **Capabilities**:
  - Error type classification
  - Root cause identification
  - Affected code location mapping
  - Severity assessment

#### Fixer Agent 🔧
- **Input**: Error analysis + original code
- **Output**: Proposed code fix
- **Capabilities**:
  - Context-aware code generation
  - Minimal change optimization
  - Style preservation
  - Confidence scoring

#### Reviewer Agent ✅
- **Input**: Original code + proposed fix + error context
- **Output**: Validation result + feedback
- **Capabilities**:
  - Logic validation
  - Side effect analysis
  - Best practice enforcement
  - Improvement suggestions

### State Management

The system uses a shared state object that flows through all agents:

```python
class DebugState:
    original_code: str          # Input code
    error_log: str             # Input error
    error_analysis: ErrorAnalysis  # Parser output
    proposed_fixes: List[CodeFix]  # All attempted fixes
    current_fix: CodeFix       # Latest fix attempt
    review_feedback: str       # Reviewer comments
    status: DebugStatus        # Current workflow state
    iteration_count: int       # Loop counter
    reasoning_steps: List[str] # Explainability trail
    final_result: CodeFix      # Successful fix
```

### Workflow Logic

1. **Initialization**: Set up state with user input
2. **Parsing Phase**: Analyze error and code structure
3. **Fixing Phase**: Generate code improvements
4. **Review Phase**: Validate and provide feedback
5. **Decision Point**: 
   - If valid → Complete workflow
   - If invalid → Return to fixing (up to max iterations)
   - If max iterations reached → Mark as failed

## 🧪 Testing

### Unit Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_parser_agent.py -v

# Run with coverage
pytest --cov=src tests/
```

### Test Examples

```python
# tests/test_workflow.py
import pytest
from src.workflow.debug_workflow import DebugWorkflow

def test_simple_syntax_error():
    debugger = DebugWorkflow()
    
    result = debugger.debug_code(
        code="print('Hello World'",  # Missing closing parenthesis
        error_log="SyntaxError: unexpected EOF while parsing",
        max_iterations=1
    )
    
    assert result["status"] == "completed"
    assert ")" in result["final_result"].fixed_code
```

### Manual Testing Scenarios

1. **Syntax Errors**: Missing brackets, quotes, colons
2. **Runtime Errors**: Division by zero, index out of range
3. **Type Errors**: String/integer operations, method calls
4. **Logic Errors**: Incorrect algorithms, edge cases
5. **Import Errors**: Missing modules, circular imports

## 📊 Performance & Monitoring

### Metrics Tracked

- **Success Rate**: Percentage of successfully fixed bugs
- **Iteration Efficiency**: Average iterations per fix
- **Agent Performance**: Individual agent accuracy
- **Response Time**: Time to generate fixes
- **Confidence Scores**: AI certainty levels

### Logging

The system logs:
- Agent decisions and reasoning
- API calls and response times
- Error patterns and frequencies
- User interactions and feedback

### Optimization Tips

1. **Use GPT-4** for complex bugs (higher success rate)
2. **Limit iterations** to 3-5 for cost efficiency  
3. **Provide detailed error logs** for better analysis
4. **Include test cases** when possible
5. **Review AI suggestions** before implementing

## 🔒 Security & Privacy

### Data Handling

- **No Code Storage**: Code is processed in memory only
- **API Security**: Uses secure HTTPS connections
- **Key Management**: Environment variable isolation
- **Session Isolation**: Each debugging session is independent

### Best Practices

- Never commit API keys to version control
- Use environment variables for sensitive data
- Regularly rotate API keys
- Monitor API usage and costs
- Review generated code before execution

## 🐛 Troubleshooting

### Common Issues

#### "OpenAI API Error"
- **Cause**: Invalid or missing API key
- **Solution**: Check API key in sidebar/environment variables

#### "Max iterations reached"
- **Cause**: Complex bug requiring multiple attempts
- **Solution**: Increase max_iterations or provide more context

#### "No fix generated"
- **Cause**: Ambiguous error or unsupported language
- **Solution**: Provide clearer error logs or use different model

#### "Streamlit connection error"
- **Cause**: Port already in use
- **Solution**: Use `streamlit run app.py --server.port 8502`

### Debug Mode

Enable detailed logging:
```bash
export DEBUG_MODE=true
streamlit run src/app/streamlit_app.py
```

## 🚀 Deployment

### Production Deployment

#### Streamlit Cloud
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Add secrets (API keys) in dashboard
4. Deploy automatically

#### Docker Production
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  ai-debugger:
    build: .
    ports:
      - "80:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### AWS/GCP/Azure
- Use container services (ECS, Cloud Run, Container Instances)
- Set up load balancing for high availability
- Configure auto-scaling based on usage
- Implement monitoring and alerting

### Scaling Considerations

- **API Rate Limits**: Monitor OpenAI usage quotas
- **Memory Usage**: Large code files may require more RAM
- **Concurrent Users**: Use session state management
- **Cost Management**: Set usage alerts and budgets

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```
4. **Make your changes**
5. **Run tests**
   ```bash
   pytest tests/
   black src/
   ```

### Areas for Contribution

- **New Language Support**: Extend beyond Python
- **Additional LLM Providers**: Anthropic, Google, etc.
- **UI Improvements**: Better visualizations, mobile support
- **Performance Optimization**: Caching, parallel processing
- **Testing Coverage**: More test scenarios and edge cases

## 🙏 Acknowledgments

- **LangChain/LangGraph**: For the powerful agent orchestration framework
- **OpenAI**: For providing the GPT models
- **Streamlit**: For the intuitive web framework