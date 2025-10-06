import streamlit as st
from PyPDF2 import PdfReader
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Vérifie que la clé API est définie
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    st.error("❌ La variable d'environnement GOOGLE_API_KEY n'est pas définie.")
    st.stop()

import google.generativeai as genai
genai.configure(api_key=google_api_key)


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    prompt_template = """
    Answer the question with detail from the context provided. 
    Make sure to give all the details. 
    If the answer is not in the context, please say "I don't know". 
    Do not provide a wrong answer.

    Context: 
    {context}

    Question: 
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain


def user_input(user_question):
    if not os.path.exists("faiss_index"):
        st.warning("⚠️ Veuillez d'abord uploader des PDFs et cliquer sur 'Get Text'.")
        return

    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
        chain = get_conversational_chain()
        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )
        st.write("💬 **Réponse :**", response["output_text"])
    except Exception as e:
        st.error(f"Erreur lors du traitement de la question : {e}")


def main():
    st.set_page_config(page_title="Chat with PDFs", page_icon="📄")
    st.header("📄 Chat with multiple PDFs using Google Gemini AI")

    # Désactive le champ si l'index n'existe pas
    disabled = not os.path.exists("faiss_index")
    user_question = st.text_input("Posez une question sur vos PDFs :", disabled=disabled)

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("📁 Menu")
        pdf_docs = st.file_uploader(
            "Téléchargez vos PDFs ici",
            type=["pdf"],
            accept_multiple_files=True
        )
        if st.button("📝 Extraire le texte"):
            if not pdf_docs:
                st.warning("Veuillez uploader au moins un PDF.")
            else:
                with st.spinner("Extraction en cours..."):
                    raw_text = get_pdf_text(pdf_docs)
                    if not raw_text.strip():
                        st.error("Aucun texte extrait des PDFs. Vérifiez qu'ils ne sont pas scannés.")
                        return
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("✅ Index vectoriel créé avec succès !")


if __name__ == "__main__":
    main()