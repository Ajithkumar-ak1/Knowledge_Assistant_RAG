import os
import streamlit as st
from utils.pdf_loader import extract_text_from_pdf, clean_text

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="PDF Knowledge Assistant", layout="centered")

st.title("📄 PDF Knowledge Assistant (RAG)")
st.write("Upload one or more PDFs to create a temporary knowledge base.")

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

documents = []

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded")

    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        # Save PDF
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extract + clean text
        raw_text = extract_text_from_pdf(file_path)
        cleaned_text = clean_text(raw_text)

        documents.append({
            "source": uploaded_file.name,
            "text": cleaned_text
        })

    st.subheader("📄 Ingested Documents")
    for doc in documents:
        st.markdown(f"**{doc['source']}**")
        st.write(f"Characters: {len(doc['text'])}")
        st.divider()

    st.success("Documents ingested successfully. Ready for chunking 🚀")
