import google.generativeai as genai
import os
import json

# Configure the Gemini API client.
genai.configure(api_key=os.getenv("AIzaSyCRg1y68H3cwDRImIIO2gDkbnPbv5RUjco"))

# Initialize the generative model.
model = genai.GenerativeModel("gemini-2.5-flash")

def debug_error(error_message, code_snippet=""):
    """
    Analyzes a provided error message and an optional code snippet.
    It returns a structured JSON object with the cause, a suggested fix, and corrected code.

    Args:
        error_message (str): The error log or message to be analyzed.
        code_snippet (str, optional): An optional code snippet related to the error.

    Returns:
        dict: A dictionary containing 'cause', 'fix', and 'fixed_code' fields.
              Returns a predictable error dictionary if parsing or API call fails.
    """
    try:
        # Construct the prompt with instructions for the model to return JSON.
        prompt = f"""
        Explain this error and suggest a fix.
        Return JSON with fields: "cause", "fix", "fixed_code".

        Error:
        {error_message}

        Code:
        {code_snippet}
        """
        
        # Make the API call to the generative model.
        # This is where the primary potential for network or API errors exists.
        response = model.generate_content(prompt)
        
        # Parse the JSON response from the model.
        # This is wrapped in a specific try-except block to handle parsing failures.
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # If the model's response is not valid JSON, we return a structured
            # error message to prevent the application from crashing.
            print(f"Warning: Model response was not valid JSON. Raw response: {response.text}")
            return {
                "cause": "The AI failed to generate a valid JSON response.",
                "fix": "Try rephrasing your error message or providing more context.",
                "fixed_code": ""
            }
            
    except Exception as e:
        # This broader except block handles any other issues, like API connectivity problems.
        print(f"An error occurred during the Gemini API call: {e}")
        return {
            "cause": "An error occurred with the API call.",
            "fix": "Please check your network connection and API key, and try again.",
            "fixed_code": ""
        }
