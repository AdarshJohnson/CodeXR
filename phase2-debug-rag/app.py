import os
import re
import json
import requests
import streamlit as st
from dotenv import load_dotenv

# --- Load API Key ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-2.5-flash"

# --- API Call Logic ---
def call_gemini_api(prompt: str, is_json_response: bool = False):
    """
    General purpose function to call the Gemini API.
    Can be configured to expect a structured JSON response or a plain text response.
    """
    if not api_key:
        if is_json_response:
            return {"cause": "Missing API Key", "fix": "Add GEMINI_API_KEY to .env", "fixed_code": ""}
        else:
            return "❌ Missing API Key. Add GEMINI_API_KEY to .env"

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        res = requests.post(endpoint, headers=headers, json=body)
        res.raise_for_status() # Raises an HTTPError for bad responses
        data = res.json()
        text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

        if is_json_response:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    return {"cause": "AI failed to generate valid JSON", "fix": "Try rephrasing or adding more context", "fixed_code": ""}
            else:
                # Fallback if no JSON object is found at all
                return {"cause": "AI failed to generate valid JSON", "fix": "Try rephrasing or adding more context", "fixed_code": ""}
        
        return text

    except requests.exceptions.RequestException as e:
        if is_json_response:
            return {"cause": f"API Request Error: {e}", "fix": "Check your API key and network connection.", "fixed_code": ""}
        else:
            return f"❌ API Request Error: {e}"

# --- Streamlit UI and Logic ---
def main():
    st.set_page_config(page_title="CodeXR Phase 2 Demo", layout="wide")
    st.title("🤖 CodeXR ")

    # Create tabs for RAG-Lite and Debugging sections
    tab1, tab2 = st.tabs(["📘 RAG-Lite Documentation Search", "🛠️ Error Debugging"])

    with tab1:
        st.header("Documentation Search")
        st.markdown("Use this section to get answers to your coding questions, enhanced by providing additional context (e.g., a documentation page or a code snippet).")
        
        question = st.text_area("Your Question:", placeholder="e.g., How do I add a new list item in React?")
        context = st.text_area("Documentation Context:", placeholder="Paste relevant documentation or code here for better results.", height=150)

        if st.button("Search with RAG-Lite"):
            if not question.strip():
                st.warning("⚠️ Please provide a question.")
                return

            rag_prompt = f"""
You are a helpful coding assistant.
Use the following documentation context to answer the question concisely and accurately.

Question:
{question}

Documentation Context:
{context or "No additional context provided."}
"""
            st.info("Searching...")
            with st.spinner("Calling Gemini API..."):
                answer = call_gemini_api(rag_prompt)
            
            st.markdown("### Answer")
            st.info(answer)

    with tab2:
        st.header("Error Debugging")
        st.markdown("Paste an error message and optional code snippet to get a structured diagnosis and fix.")

        error_message = st.text_area("Error Message:", placeholder="Paste your error message here...", height=100)
        code_snippet = st.text_area("Code Snippet (Optional):", placeholder="Paste the code snippet where the error occurs...", height=150)

        if st.button("Debug Error"):
            if not error_message.strip():
                st.warning("⚠️ Please provide an error message.")
                return

            debug_prompt = f"""
You are a strict JSON-only code debugging assistant.
Analyze the following error and optional code snippet.
Return ONLY a JSON object with the keys:
- cause: short explanation of the error
- fix: suggested fix
- fixed_code: corrected code snippet

Error:
{error_message}

Code:
{code_snippet or "None"}

Example output:
{{
  "cause": "Missing colon in function definition",
  "fix": "Add a colon at the end of the function signature",
  "fixed_code": "def add_numbers(a, b):\\n    return a + b"
}}
"""
            st.info("Debugging...")
            with st.spinner("Calling Gemini API..."):
                result = call_gemini_api(debug_prompt, is_json_response=True)
            
            st.markdown("### Diagnosis & Fix")
            st.write(f"**Cause:** {result.get('cause', 'N/A')}")
            st.write(f"**Fix:** {result.get('fix', 'N/A')}")
            
            fixed_code = result.get("fixed_code")
            if fixed_code:
                st.markdown("**Fixed Code:**")
                st.code(fixed_code)
            else:
                st.markdown("**Fixed Code:** None provided.")

if __name__ == "__main__":
    main()