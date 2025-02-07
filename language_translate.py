import streamlit as st 
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def run():
# Title of the app
    st.markdown("<h1 style='text-align: center; white-space: nowrap;'>🎯 Language Detection and Translation</h1>", unsafe_allow_html=True)

    # Select action for language detection or translation
    option = st.selectbox("Select action", ["Detection", "Translation"])

    # Language Detection Section
    
    if option == "Detection":
        st.subheader("Language Detection")
        input_text = st.text_area("Enter text to detect language", "")
        if st.button("Detect"):
            if input_text:
                try:
                    prompt1 = f"""
                        You are an AI assistant.
                        ### Detect Language
                        - Based on the given text, detect the language of the text.
                        - Only respond with the name of the language.
                        {input_text}
                    """
                    detected_language = model.generate_content(prompt1)
                    st.write(f"Detected language is: {detected_language.text.strip()}")
                except Exception as e:
                    st.error(f"Error: {e}")
    # Language Translation Section
    else:
        st.subheader("Language Translation")
        
        # Dropdowns for source and destination languages
        source_options = st.selectbox("Source language", ["English", "Hindi", "Telugu", "French", "Spanish", "German"])
        destination_options = st.selectbox("Destination language", ["English", "Hindi", "Telugu", "French", "Spanish", "German"])
        
        # Input text for translation
        input_text = st.text_area("Enter text to translate...")
        if st.button("Translate"):
            if input_text:
                try:
                    prompt2 = f"""
                        You are an AI Assistant.
                        ### Text Translation
                        - Take the input text, then convert the text from source to destination language.
                        - Here are the input, selected source language, and destination language:
                        Input text: {input_text}
                        Source language: {source_options}
                        Destination language: {destination_options}
                    """
                    translated_text = model.generate_content(prompt2)
                    st.write(f"Translated Text-------> {translated_text.text.strip()}")
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__=="__main__":
    run()