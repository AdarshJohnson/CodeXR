import google.generativeai as genai
import os

# Configure the Gemini API client using the API key from environment variables.
genai.configure(api_key=os.getenv("AIzaSyCRg1y68H3cwDRImIIO2gDkbnPbv5RUjco"))

# Initialize the generative model. Using 'gemini-2.5-flash' for speed.
model = genai.GenerativeModel("gemini-2.5-flash")

def rag_answer(user_input, docs_context):
    """
    This function uses a Retrieval-Augmented Generation (RAG) approach.
    It combines a user's query with a retrieved documentation context
    to generate a more accurate and grounded response using the Gemini model.

    Args:
        user_input (str): The original query from the user.
        docs_context (str): The documentation paragraphs retrieved by the RAG system.

    Returns:
        str: A helpful, concise answer to the user's query, or an error message if the API call fails.
    """
    try:
        # Construct the prompt with a system persona and clear separation of concerns.
        prompt = f"""
        You are CodeXR, an AI for AR/VR developers.
        User request: {user_input}
        
        Relevant docs context:
        {docs_context}
        
        Please give a helpful, concise answer with code if needed.
        """
        
        # Make the API call to the generative model.
        response = model.generate_content(prompt)
        
        # Return the generated text from the model's response.
        return response.text
        
    except Exception as e:
        # This catch block handles any potential errors during the API call
        # (e.g., network issues, authentication problems, or rate limits).
        # We print the full error for debugging but return a user-friendly message.
        print(f"An error occurred during the Gemini API call: {e}")
        return "I'm sorry, an error occurred while trying to generate a response. Please try again."
