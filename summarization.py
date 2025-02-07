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
    st.markdown("<h1 style='text-align: center;'>📜 Text Summarization</h1>", unsafe_allow_html=True)

    st.subheader("Summarizing the given long text :")

    input_text = st.text_area("Enter the long text here...", height=300)

    if st.button("Summarize"):
        if input_text.strip():
            prompt = f"""
            You are an AI assistant that summarizes long texts effectively.
            - Generate a **brief summary** of the given text.
            - Include **necessary headings** for clarity.
            - Format the response using **bold text** based on headings,sub headings.
            - Keep the summary **concise and informative**.

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
            st.warning("Please enter some text to summarize.")

if __name__ == "__main__":
    run()
