import streamlit as st
import google.generativeai as genai
import PyPDF2
import re
import json
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def generate_json_from_text(text):
    """Generate JSON from extracted text using Gemini."""
    prompt = f"""
        Take the text given below:
        \"\"\"{text}\"\"\"
        Extract the details and provide them in JSON format with the following structure:
        {{
            "invoice_details": {{
                "invoice_number": "INV-XXXX",
                "order_number": "XXXXX",
                "invoice_date": "XXXX",
                "due_date": "XXXX",
                "total_due": "$XX.XX"
            }},
            "sender_details": {{
                "name": "XXXXX",
                "address": "XXXXX",
                "email": "XXXXX"
            }},
            "recipient_details": {{
                "name": "XXXXX",
                "address": "XXXXX",
                "email": "XXXXX"
            }},
            "items": [
                {{
                    "quantity": "X.XX",
                    "service": "XXXXX",
                    "rate": "$XX.XX",
                    "adjustment": "X.XX%",
                    "sub_total": "$XX.XX"
                }}
            ],
            "tax_details": {{
                "subtotal": "$XXX.XX",
                "tax_amount": "$XX.XX",
                "total": "$XXX.XX"
            }},
            "bank_details": {{
                "bank_name": "XXXXX",
                "account_number": "XXXXX",
                "bsb_number": "XXXXX"
            }}
        }}
        Only return JSON output, no explanations.
        """
    response = model.generate_content(prompt)
    match = re.search(r'\{.*\}', response.text, re.DOTALL)
    if match:
        valid_json_string = match.group(0)
        try:
            return json.loads(valid_json_string)
        except json.JSONDecodeError:
            st.error("Failed to decode JSON. Please check the extracted text.")
            return None
    return None

def save_json_file(json_data, filename):
    """Save JSON data to a file."""
    json_file_path = os.path.join("invoice_json", filename)
    os.makedirs("invoice_json", exist_ok=True)
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)
    return json_file_path

# Define run() to integrate with multi-page Streamlit app
def run():
    st.title("📜 Invoice PDF to JSON Extractor")
    st.write("Upload an invoice PDF to extract details and generate a structured JSON file.")

    uploaded_files = st.file_uploader("Upload Invoice PDF(s)", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.write(f"## Processing: {uploaded_file.name}")
            extracted_text = extract_text_from_pdf(uploaded_file)

            if extracted_text:
                st.write("### Generated JSON...")
                json_data = generate_json_from_text(extracted_text)

                if json_data:
                    st.json(json_data)

                    json_filename = uploaded_file.name.replace(".pdf", ".json")
                    json_file_path = save_json_file(json_data, json_filename)

                    with open(json_file_path, "rb") as f:
                        st.download_button(
                            label=f"Download {json_filename}",
                            data=f,
                            file_name=json_filename,
                            mime="application/json"
                        )
                else:
                    st.error("Failed to generate valid JSON. Please check the invoice format.")
            else:
                st.error("Could not extract text from the PDF.")



if __name__== "__main__":
    run()