# import streamlit as st
# import os
# from typing import Optional
# from src.workflow.debug_workflow import DebugWorkflow
# # from src.models. import DebugStatus
# from src.models.schemas import DebugStatus

# # Page config
# st.set_page_config(
#     page_title="AI Code Debugger",
#     page_icon="🐛",
#     layout="wide"
# )

# class StreamlitApp:
#     def __init__(self):
#         self.workflow = None
        
#     def initialize_workflow(self, api_key: str, model: str = "gpt-4o-mini"):
#         """Initialize the debugging workflow"""
#         os.environ["OPENAI_API_KEY"] = api_key
#         self.workflow = DebugWorkflow(model)
    
#     def render_sidebar(self):
#         """Render sidebar with settings"""
#         st.sidebar.title("🔧 Settings")
        
#         # API Key input
#         api_key = st.sidebar.text_input(
#             "OpenAI API Key",
#             type="password",
#             help="Enter your OpenAI API key"
#         )
        
#         # Model selection
#         model = st.sidebar.selectbox(
#             "Select Model",
#             ["gpt-4", "gpt-4o-mini", "gpt-3.5-turbo"],
#             index=0
#         )
        
#         # Max iterations
#         max_iterations = st.sidebar.slider(
#             "Max Iterations",
#             min_value=1,
#             max_value=5,
#             value=3,
#             help="Maximum number of fix attempts"
#         )
        
#         return api_key, model, max_iterations
    
#     def render_main_interface(self, api_key: str, model: str, max_iterations: int):
#         """Render main debugging interface"""
        
#         st.title("🐛 AI Code Debugger")
#         st.markdown("Upload your buggy code and error log to get AI-powered debugging assistance!")
        
#         # Input section
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("📝 Code Input")
#             code_input = st.text_area(
#                 "Paste your code here:",
#                 height=300,
#                 placeholder="def my_function():\n    # Your buggy code here\n    pass"
#             )
        
#         with col2:
#             st.subheader("❌ Error Log")
#             error_input = st.text_area(
#                 "Paste your error log here:",
#                 height=300,
#                 placeholder="Traceback (most recent call last):\n  File...\nError: ..."
#             )
        
#         # Debug button
#         col1, col2, col3 = st.columns([1, 1, 1])
#         with col2:
#             debug_button = st.button("🔍 Debug Code", type="primary", use_container_width=True)
        
#         # Process debugging
#         if debug_button:
#             if not api_key:
#                 st.error("Please enter your OpenAI API key in the sidebar!")
#                 return
            
#             if not code_input or not error_input:
#                 st.error("Please provide both code and error log!")
#                 return
            
#             # Initialize workflow
#             if not self.workflow:
#                 with st.spinner("Initializing AI debugger..."):
#                     self.initialize_workflow(api_key, model)
            
#             # Run debugging workflow
#             with st.spinner("🤖 AI agents are analyzing your code..."):
#                 try:
#                     result = self.workflow.debug_code(
#                         code_input, 
#                         error_input, 
#                         max_iterations
#                     )
                    
#                     self.display_results(result)
                    
#                 except Exception as e:
#                     st.error(f"An error occurred during debugging: {str(e)}")
    
#     def display_results(self, result: dict):
#         """Display debugging results"""
        
#         st.divider()
#         st.subheader("🎯 Debugging Results")
        
#         # Status indicator
#         status = result.get("status")
#         if status == DebugStatus.COMPLETED:
#             st.success("✅ Debugging completed successfully!")
#         elif status == DebugStatus.FAILED:
#             st.error("❌ Debugging failed")
        
#         # Results tabs
#         tab1, tab2, tab3, tab4 = st.tabs(["🔧 Fixed Code", "📊 Analysis", "🔄 Process", "📈 Summary"])
        
#         with tab1:
#             final_result = result.get("final_result")
#             if final_result:
#                 st.subheader("Fixed Code")
#                 st.code(final_result.fixed_code, language="python")
                
#                 st.subheader("Explanation")
#                 st.write(final_result.explanation)
                
#                 st.subheader("Changes Summary")
#                 st.write(final_result.changes_summary)
                
#                 # Confidence score
#                 confidence = final_result.confidence_score
#                 st.metric(
#                     "Confidence Score", 
#                     f"{confidence:.1%}",
#                     help="AI's confidence in the fix"
#                 )
#             else:
#                 st.warning("No final fix was generated.")
        
#         with tab2:
#             error_analysis = result.get("error_analysis")
#             if error_analysis:
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     st.metric("Error Type", error_analysis.error_type)
#                     st.metric("Severity", error_analysis.severity)
                
#                 with col2:
#                     st.metric("Location", error_analysis.error_location)
#                     st.metric("Affected Lines", len(error_analysis.affected_lines))
                
#                 st.subheader("Root Cause Analysis")
#                 st.write(error_analysis.root_cause)
#             else:
#                 st.warning("No error analysis available.")
        
#         with tab3:
#             st.subheader("AI Reasoning Process")
#             reasoning_steps = result.get("reasoning_steps", [])
            
#             for i, step in enumerate(reasoning_steps, 1):
#                 st.write(f"**Step {i}:** {step}")
            
#             # Iteration info
#             iterations = result.get("iteration_count", 0)
#             max_iter = result.get("max_iterations", 3)
#             st.metric("Iterations Used", f"{iterations}/{max_iter}")
        
#         with tab4:
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 proposed_fixes = len(result.get("proposed_fixes", []))
#                 st.metric("Fixes Proposed", proposed_fixes)
            
#             with col2:
#                 status_color = "🟢" if status == DebugStatus.COMPLETED else "🔴"
#                 st.metric("Final Status", f"{status_color} {status.value}")
            
#             with col3:
#                 if final_result:
#                     st.metric("Final Confidence", f"{final_result.confidence_score:.1%}")
#                 else:
#                     st.metric("Final Confidence", "N/A")
    
#     def run(self):
#         """Run the Streamlit app"""
        
#         # Render sidebar
#         api_key, model, max_iterations = self.render_sidebar()
        
#         # Render main interface
#         self.render_main_interface(api_key, model, max_iterations)
        
#         # Footer
#         st.divider()
#         st.markdown(
#             """
#             <div style='text-align: center; color: #666;'>
#                 Built with ❤️ using LangGraph, OpenAI, and Streamlit
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

# if __name__ == "__main__":
#     app = StreamlitApp()
#     app.run()
import streamlit as st
import os
from typing import Optional
from dotenv import load_dotenv
from src.workflow.debug_workflow import DebugWorkflow
# from src.models. import DebugStatus
from src.models.schemas import DebugStatus

# Load environment variables from .env file
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Code Debugger",
    page_icon="🐛",
    layout="wide"
)

class StreamlitApp:
    def __init__(self):
        self.workflow = None
        # Load API key from environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        
    def initialize_workflow(self, model: str = "gpt-4o-mini"):
        """Initialize the debugging workflow"""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        os.environ["OPENAI_API_KEY"] = self.api_key
        self.workflow = DebugWorkflow(model)
    
    def render_sidebar(self):
        """Render sidebar with settings"""
        st.sidebar.title("🔧 Settings")
        
        # API Key status
        if self.api_key:
            st.sidebar.success("✅ API Key loaded from .env")
        else:
            st.sidebar.error("❌ API Key not found in .env file")
            st.sidebar.markdown("""
                **Setup Instructions:**
                1. Create a `.env` file in your project root
                2. Add: `OPENAI_API_KEY=your_api_key_here`
                3. Restart the application
            """)
        
        # Model selection
        model = st.sidebar.selectbox(
            "Select Model",
            ["gpt-4", "gpt-4o-mini", "gpt-3.5-turbo"],
            index=1
        )
        
        # Max iterations
        max_iterations = st.sidebar.slider(
            "Max Iterations",
            min_value=1,
            max_value=5,
            value=3,
            help="Maximum number of fix attempts"
        )
        
        return model, max_iterations
    
    def render_main_interface(self, model: str, max_iterations: int):
        """Render main debugging interface"""
        
        st.title("🐛 AI Code Debugger")
        st.markdown("Upload your buggy code and error log to get AI-powered debugging assistance!")
        
        # Check if API key is available
        if not self.api_key:
            st.error("🔑 No API key found! Please set up your `.env` file with your OpenAI API key.")
            st.markdown("""
                **Quick Setup:**
                1. Create a file named `.env` in your project root directory
                2. Add the following line to the file:
                   ```
                   OPENAI_API_KEY=sk-your-actual-api-key-here
                   ```
                3. Save the file and restart the Streamlit app
                4. Make sure to add `.env` to your `.gitignore` file to keep your API key secure
            """)
            return
        
        # Input section
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Code Input")
            code_input = st.text_area(
                "Paste your code here:",
                height=300,
                placeholder="def my_function():\n    # Your buggy code here\n    pass"
            )
        
        with col2:
            st.subheader("❌ Error Log")
            error_input = st.text_area(
                "Paste your error log here:",
                height=300,
                placeholder="Traceback (most recent call last):\n  File...\nError: ..."
            )
        
        # Debug button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            debug_button = st.button("🔍 Debug Code", type="primary", use_container_width=True)
        
        # Process debugging
        if debug_button:
            if not code_input or not error_input:
                st.error("Please provide both code and error log!")
                return
            
            # Initialize workflow
            if not self.workflow:
                with st.spinner("Initializing AI debugger..."):
                    try:
                        self.initialize_workflow(model)
                    except ValueError as e:
                        st.error(str(e))
                        return
            
            # Run debugging workflow
            with st.spinner("🤖 AI agents are analyzing your code..."):
                try:
                    result = self.workflow.debug_code(
                        code_input, 
                        error_input, 
                        max_iterations
                    )
                    
                    self.display_results(result)
                    
                except Exception as e:
                    st.error(f"An error occurred during debugging: {str(e)}")
    
    def display_results(self, result: dict):
        """Display debugging results"""
        
        st.divider()
        st.subheader("🎯 Debugging Results")
        
        # Status indicator
        status = result.get("status")
        if status == DebugStatus.COMPLETED:
            st.success("✅ Debugging completed successfully!")
        elif status == DebugStatus.FAILED:
            st.error("❌ Debugging failed")
        
        # Results tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🔧 Fixed Code", "📊 Analysis", "🔄 Process", "📈 Summary"])
        
        with tab1:
            final_result = result.get("final_result")
            if final_result:
                st.subheader("Fixed Code")
                st.code(final_result.fixed_code, language="python")
                
                st.subheader("Explanation")
                st.write(final_result.explanation)
                
                st.subheader("Changes Summary")
                st.write(final_result.changes_summary)
                
                # Confidence score
                confidence = final_result.confidence_score
                st.metric(
                    "Confidence Score", 
                    f"{confidence:.1%}",
                    help="AI's confidence in the fix"
                )
            else:
                st.warning("No final fix was generated.")
        
        with tab2:
            error_analysis = result.get("error_analysis")
            if error_analysis:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Error Type", error_analysis.error_type)
                    st.metric("Severity", error_analysis.severity)
                
                with col2:
                    st.metric("Location", error_analysis.error_location)
                    st.metric("Affected Lines", len(error_analysis.affected_lines))
                
                st.subheader("Root Cause Analysis")
                st.write(error_analysis.root_cause)
            else:
                st.warning("No error analysis available.")
        
        with tab3:
            st.subheader("AI Reasoning Process")
            reasoning_steps = result.get("reasoning_steps", [])
            
            for i, step in enumerate(reasoning_steps, 1):
                st.write(f"**Step {i}:** {step}")
            
            # Iteration info
            iterations = result.get("iteration_count", 0)
            max_iter = result.get("max_iterations", 3)
            st.metric("Iterations Used", f"{iterations}/{max_iter}")
        
        with tab4:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                proposed_fixes = len(result.get("proposed_fixes", []))
                st.metric("Fixes Proposed", proposed_fixes)
            
            with col2:
                status_color = "🟢" if status == DebugStatus.COMPLETED else "🔴"
                st.metric("Final Status", f"{status_color} {status.value}")
            
            with col3:
                if final_result:
                    st.metric("Final Confidence", f"{final_result.confidence_score:.1%}")
                else:
                    st.metric("Final Confidence", "N/A")
    
    def run(self):
        """Run the Streamlit app"""
        
        # Render sidebar
        model, max_iterations = self.render_sidebar()
        
        # Render main interface
        self.render_main_interface(model, max_iterations)
        
        # Footer
        st.divider()
        st.markdown(
            """
            <div style='text-align: center; color: #666;'>
                Developed with LangGraph, OpenAI, and Streamlit
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
