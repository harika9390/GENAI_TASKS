import streamlit as st 
import os     
import google.generativeai as genai 
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit App
def run():
    st.markdown("<h1 style='text-align: center;'>📧 Email Spam Detection</h1>", unsafe_allow_html=True)

    st.subheader("Detect whether the email is spam or not:")
    input_text = st.text_area("Enter the email text here...")
    
    if st.button("Submit"):
        if input_text.strip():
            prompt = f"""
                    You are an AI assistant that detects spam emails.
                    - Analyze the given email text.
                    - Classify it as either 'Spam' or 'Not spam'.
                    - Your response should be strictly in **JSON format**:

                    **Example JSON Response:**
                    - If spam: `{{"email_type": "Spam"}}`
                    - If not spam: `{{"email_type": "Not spam"}}`

                    Consider spam indicators such as:
                    - Promotional language
                    - Excessive links
                    - Rewards, urgency, unknown senders
                    - Requests for personal  etc.

                    **Email text:** {input_text}
                """

            response = model.generate_content(prompt)

            try:
                result = response.text.strip()
                st.write(result)
            except Exception as e:
                st.error(" Please enter email text.")
                

if __name__ == "__main__":
    run()
