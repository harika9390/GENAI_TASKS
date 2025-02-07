import streamlit as st
import google.generativeai as genai
import PyPDF2
import os
import re

from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Folder containing PDFs
PDF_FOLDER = "invoice_templates/"

# Extract text from all PDFs in the folder
def extract_text_from_pdfs(folder_path):
    pdf_texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = "\n".join([page.extract_text() or "" for page in reader.pages])
                normalized_name = filename.lower().replace(" ", "_")  # Normalize name
                pdf_texts[normalized_name] = text  # Store normalized name
    return pdf_texts

def run():
    st.markdown("<h1 style='text-align: center;'>📜 Multiple Invoices Chatbot</h1>", unsafe_allow_html=True)

    # Load PDF data
    pdf_data = extract_text_from_pdfs(PDF_FOLDER)

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Last referenced invoice
    if "last_invoice" not in st.session_state:
        st.session_state.last_invoice = None

    # Display chat history
    for role, text in st.session_state.chat_history:
        with st.chat_message("assistant" if role == "Bot" else "user"):
            st.write(text)

    # User input
    user_query = st.chat_input("Ask something about invoices")

    if user_query:
        st.chat_message("user").write(user_query)
        
        # Extract invoice name from query (e.g., "invoice6", "invoice_6.pdf")
        invoice_pattern = r"(invoice[_\s]?(\d+))"
        match = re.search(invoice_pattern, user_query.lower())

        pdf_name = None
        if match:
            extracted_invoice = f"invoice_{match.group(2)}.pdf"  # Normalize to match stored filenames

            for filename in pdf_data.keys():
                if extracted_invoice in filename:
                    pdf_name = filename
                    break

        if pdf_name:
            st.session_state.last_invoice = pdf_name  # Store last referenced invoice
            context_text = pdf_data[pdf_name]
        elif st.session_state.last_invoice:
            pdf_name = st.session_state.last_invoice
            context_text = pdf_data[pdf_name]
        else:
            context_text = "\n".join(pdf_data.values())

        if context_text:
            prompt = f'''
                The response must only reference content from the provided context_text data.

                ### User Query: {user_query}

                ### Relevant Invoice Data: {context_text}

                Follow these instructions:  
                - Use the user query and answer based on the query.
                - If no invoice is mentioned in the query and it is referring to all invoices, search across all {context_text}.
                - If the query is related to the last query, use the last referenced invoice {st.session_state.last_invoice}.
                - If the query involves numerical comparisons (e.g., total due amounts greater than $10,000),
                  take key-value pairs in total context and then compare based on key given in query.
                - Always check and verify extracted numerical values before answering any question.
                - If the question is unrelated, respond: "I don't know, but I can help with invoice-related questions."
            '''

            response = model.generate_content(prompt)
            answer = response.text.strip()
        else:
            answer = "I couldn't find the invoice you're referring to. Please specify a valid invoice number."

        with st.chat_message("assistant"):
            st.write(answer)
        
        # Store chat history
        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("Bot", answer))


if __name__== "__main__":
    run()