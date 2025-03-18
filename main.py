import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Multi-App Streamlit", layout="wide") 



import home
import json_extraction  # Import Extracting JSON app
import single_invoice
import multi_invoices
import language_translate
import email_spam
import summarization
import sentiment
import grammar
#import speech
import text_classification
import content_generation
from streamlit_option_menu import option_menu

# st.sidebar.title("📌 Navigation")
with st.sidebar:
    selected = option_menu(
        menu_title="Main menu",
        options=[
            "Home",
            "Data Extractor",
            "Invoice Chat", 
            "Multi Invoice chat",
            "Language Assistant",
            "Email spam filter",
            "Summarization",
            "Sentiment Analysis",
            "Text corrector",
           # "Speech to text",
            "Text classifier",
            "Content Generator"
        ],
            icons=[
            "house",  # Home
            "file-earmark-text",  # Data Extractor
            "file-text",  # Invoice Chat
            "files",  # Multi Invoice Chat
            "globe",  # Language Assistant
            "envelope",  # Email Spam Filter
            "file-text-fill",  # Summarization
            "emoji-frown",  # Sentiment Analysis
            "spellcheck",  # Text Corrector
            #"mic",  # Speech to Text
            "list-check",  # Text Classifier
            "pencil-square"  # Content Generator
        ]
    )

# Display the selected app
if selected == "Home":
    home.run()
elif selected == "Data Extractor":
    json_extraction.run()
elif selected == "Invoice Chat":
    single_invoice.run()
elif selected == "Multi Invoice chat":
    multi_invoices.run()
elif selected == "Language Assistant":
    language_translate.run()
elif selected == "Email spam filter":
    email_spam.run()
elif selected == "Summarization":
    summarization.run()
elif selected == "Sentiment Analysis":
    sentiment.run()
elif selected == "Text corrector":
    grammar.run()
#elif selected == "Speech to text":
#    speech.run()
elif selected == "Text classifier":
    text_classification.run()
elif selected == "Content Generator":
    content_generation.run()
