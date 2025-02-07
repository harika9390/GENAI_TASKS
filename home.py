import streamlit as st

def run():
    st.title("🎉 Welcome to the Multi-App AI-Powered Platform!")
    
    st.write(
        "This platform provides AI-driven tools designed to simplify your tasks."
        "Explore the features below:"
    )

    st.markdown("""
    ### 🔹 **Core Features**
    
    - 📝 **Data Extractor:** Convert invoice details into structured JSON format.
    - 🗂️ **Single Invoice Chat:** Interact with AI to extract insights from a single invoice.
    - 📂 **Multi-Invoice Chat:** Analyze and compare multiple invoices in a unified conversation.
    - 🌍 **Language Assistant:** Detect languages and translate text seamlessly.
    - 📧 **Email Spam Filter:** Identify and filter out potential spam emails.
    - ✍️ **Text Summarization:** Generate concise summaries from long documents.
    - 😊 **Sentiment Analysis:** Determine the emotional tone of text.
    - 🔤 **Grammar & Spelling Correction:** Automatically fix language errors.
    - 🎙️ **Speech to Text:** Convert spoken words into accurate text.
    - 🏷️ **Text Classifier:** Categorize text into predefined labels.
    - ✨ **Content Generator:** Generate human-like text based on prompts.

    ---
    **👈Use the sidebar to navigate and explore each application!**
    """)

if __name__ == "__main__":
    run()
