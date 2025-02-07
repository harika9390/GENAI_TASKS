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
    st.markdown("<h1 style='text-align: center;'>📜Text Classification</h1>", unsafe_allow_html=True)

    st.subheader("Categorizing text:")

    input_text = st.text_area("Enter the text here:", height=100)

    if st.button("classify"):
        if input_text.strip():
            prompt = f"""
            You are an AI assistant.
            - consider the input text.
            - analyze the input text and Categorize text into predefined labels
              ex labels:Technology, Finance, Medical, Agriculture etc
            - Return the output in table format with **two columns**: "Text" and "Label".
            - Ensure the response is **only** a table, no extra explanation.
            
        
               

            **Input Text:** {input_text}
            """

            response = model.generate_content(prompt)

            try:
                summary = response.text.strip()
                st.write(summary)
            except Exception as e:
                st.error("Failed to process response. Please try again.")
                print(f"Error: {e}")

        else:
            st.warning("Please enter some text .")

if __name__ == "__main__":
    run()
