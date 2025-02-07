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
    st.markdown("<h1 style='text-align: center;'>📜 Sentiment Analysis</h1>", unsafe_allow_html=True)

    st.subheader("Determining the sentiment of the given review:")

    input_text = st.text_area("Enter the review text here...", height=100)

    if st.button("Submit"):
        if input_text.strip():
            prompt = f"""
            You are an AI assistant that analyze the review .
            - Analyze the given input review carefully.
            - Classify the input review into Postive, Negative and Neutral
            - response should be in Json format:
                Eg: '{{‘review’: ‘POSITIVE’}}'

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
            st.warning("Please enter some text to review.")

if __name__ == "__main__":
    run()
