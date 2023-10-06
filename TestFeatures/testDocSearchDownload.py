import os
import re
import requests
from datetime import datetime
from googlesearch import search
import speech_recognition as sr

from TTS import speak
from genVisual._approve import _approve
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone 
# This function might need to be replaced or modified to use ChromaDB
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI

from genVisual.searchPdf import get_user_query

# Replace with the actual location of your documents
base_directory = '/pdfs'



def load_documents(base_directory):
    documents = []
    for file in os.listdir(base_directory):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(base_directory, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
        elif file.endswith('.docx') or file.endswith('.doc'):
            doc_path = os.path.join(base_directory, file)
            loader = Docx2txtLoader(doc_path)
            documents.extend(loader.load())
        elif file.endswith('.txt'):
            text_path = os.path.join(base_directory, file)
            loader = TextLoader(text_path)
            documents.extend(loader.load())
    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=10):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

def setup_embeddings(docs):
    embeddings = OpenAIEmbeddings(model="ada")  # Assuming you're using the "ada" model
    pinecone.init(api_key="your-pinecone-api-key", environment="your-pinecone-environment")
    index_name = "your-index-name"
    index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    speak("Embeddings setup complete")
    return index

# Replace this function with the equivalent function for ChromaDB
def get_similiar_docs(index, query, k=2, score=False):
    if score:
        similar_docs = index.similarity_search_with_score(query, k=k)
    else:
        similar_docs = index.similarity_search(query, k=k)
    return similar_docs

def setup_chat_model():
    chat_model = ChatOpenAI(model="gpt-3.5-turbo")  # Assuming you're using the "gpt-3.5-turbo" model
    return chat_model

def load_qa_chain(chat_model):
    qa_chain = load_qa_chain(chat_model)
    return qa_chain

def get_answer(qa_chain, query, similar_docs):
    message = {"role": "user", "content": query}
    for doc in similar_docs:
        message["document"] = doc.content
    answer = qa_chain.get_answer(message)
    return answer

def main():
    documents = load_documents(base_directory)
    split_documents = split_documents(documents)
    index = setup_embeddings(split_documents)
    chat_model = setup_chat_model()
    qa_chain = load_qa_chain(chat_model)

    while True:
        query = get_user_query()
        similar_docs = get_similiar_docs(index, query)
        answer = get_answer(qa_chain, query, similar_docs)
        speak(answer)

if __name__ == "__main__":
    main()
