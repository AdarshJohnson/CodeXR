import os
import google.generativeai as genai

# Replace 'YOUR_API_KEY' with your actual API key
# It is recommended to use environment variables for security in production
# genai.configure(api_key=os.environ["API_KEY"])
genai.configure(api_key='GEMINI_API_KEY')

# Initialize the model
model = genai.GenerativeModel("gemini-2.5-flash")

# Send a simple prompt
try:
    response = model.generate_content("Explain how AI works")
    print("API call was successful!")
    print("Response text:", response.text)
except Exception as e:
    print("An error occurred during the API call.")
    print("Error details:", e)
