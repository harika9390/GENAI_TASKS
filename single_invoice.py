import streamlit as st
import google.generativeai as genai
import PyPDF2
import os


from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def run():
    
    def extract_text_from_pdf(pdf_path):
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text


    PDF_PATH = "invoice_.pdf"  
    pdf_content = extract_text_from_pdf(PDF_PATH)

    #st.set_page_config(page_title="ChatGPT-like Chatbot") 

    st.markdown("<h1 style='text-align: center;'>📜Single Invoice Chatbot</h1>", unsafe_allow_html=True)

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for role, text in st.session_state.chat_history:
        with st.chat_message("assistant" if role == "Bot" else "user"):
            st.write(text)

    # User input with chat UI
    user_query = st.chat_input("Ask something about the invoice...")

    if user_query:
        st.chat_message("user").write(user_query)

        prompt2 = f'''
            Instructions for Handling User Queries:

            ### Context:
            The provided response must only reference the content in {pdf_content} to answer the user's query.
            
            ### User Query Handling:
            - When a user asks a question related to the provided content, the response should directly address the query using the relevant information from the content.
            - If the user's question or message is unrelated to the provided content, the response should be:
                "I don't know, but I can help with questions about the content provided. How can I assist you?"
            
            ### Greeting Handling:
            - In case of casual greetings (e.g., "Hi", "Hello"), reply with: "Hi! How are you? How can I help you today?"

            ### Session Context:
            - When responding, reference relevant past interactions stored in {st.session_state.chat_history} 
            if they are relevant to the conversation.
            Use this context to ensure that responses feel natural and connected to the ongoing dialogue.

            ### User Question: {user_query}

            '''
        response = model.generate_content(prompt2)
        answer = response.text.strip()

        with st.chat_message("assistant"):
            st.write(answer)

        # Store chat history
        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("Bot", answer))

if __name__== "__main__":
    run()