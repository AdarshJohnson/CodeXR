import streamlit as st

def call_gemini_mock(prompt: str, mode: str) -> str:
    if mode == "plan":
        return """
            {
                "steps": [
                    "Define the project scope and goals (difficulty: easy, time: 30)",
                    "Set up the development environment (difficulty: easy, time: 20)",
                    "Implement core features (difficulty: medium, time: 120)"
                ],
                "difficulty": ["easy", "easy", "medium"],
                "time": [30, 20, 120]
            }
        """
    elif mode == "code":
        return """
            {
                "code": "print('Hello, world!')",
                "explanation": "This is a simple Python code snippet that prints 'Hello, world!' to the console."
            }
        """
    elif mode == "debug":
        return """
            {
                "cause": "A syntax error occurred because of a missing parenthesis.",
                "fix": "Add a closing parenthesis at the end of the print statement.",
                "fixed_code": "print('Hello, world!')"
            }
        """
    return "Mock response from Gemini."

def main():
    st.set_page_config(page_title="CodeXR Demo", layout="wide")
    st.title("CodeXR AI Assistant Demo")

    st.markdown("### Choose a Mode and Enter Your Request")
    
    mode = st.selectbox(
        "Select Mode:",
        ["Task Planner", "Code Generator", "Error Debugger"],
        index=1,
        help="Choose the type of task you want the AI assistant to perform."
    )

    mode_map = {
        "Task Planner": "plan",
        "Code Generator": "code",
        "Error Debugger": "debug"
    }
    internal_mode = mode_map[mode]

    user_input = st.text_area(
        "Input:",
        placeholder=f"Describe your {mode.lower()} request...",
        height=150
    )

    st.text_area(
        "Optional Context:",
        placeholder="Paste related code, documentation, or constraints...",
        height=100
    )

    if st.button("Generate Response"):
        if not user_input:
            st.warning("Please provide some input to get a response.")
            return

        st.info("Generating response...")
        
        with st.spinner("Calling Gemini..."):
            prompt = f"User request for {mode}: {user_input}"
            response_text = call_gemini_mock(prompt, internal_mode)
            st.success("Response received!")

        st.markdown("### Response from CodeXR")
        st.code(response_text, language="json")
        
        st.markdown("---")
        st.markdown("""
        **Note:** This is a mock response. In a real application, you would replace
        the `call_gemini_mock` function with a real API call to Gemini.
        """)

if __name__ == "__main__":
    main()