import os
from dotenv import find_dotenv, load_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone 
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from datetime import datetime

from TTS import speak
from genVisual.newSerach import download_files
from genVisual.searchPdf import get_user_query

def load_env_vars():
    try:
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    except Exception as err:
        speak(f"Couldn't load environment variables. Error: {err}")
        pass

def load_processed_files_list():
    try:
        if os.path.exists('processed_files.txt'):
            with open('processed_files.txt', 'r') as f:
                return f.read().splitlines()
        else:
            return []
    except Exception as err:
        speak(f"Couldn't load processed files list. Error: {err}")
        pass

def save_processed_file(file):
    try:
        with open('processed_files.txt', 'a') as f:
            f.write(f"{file}\n")
    except Exception as err:
        speak(f"Couldn't save processed file. Error: {err}")
        pass

def load_docs(directory):
    try:
        loader = DirectoryLoader(directory)
        documents = loader.load()
        processed_files = load_processed_files_list()
        new_documents = [doc for doc in documents if doc.filename not in processed_files]
        return new_documents
    except Exception as err:
        speak(f"Couldn't load documents. Error: {err}")
        pass

def setup_directory(directory):
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        directory = os.path.join(directory, today)
        os.makedirs(directory, exist_ok=True)
    except Exception as err:
        speak(f"Couldn't create directory. Error: {err}")
        pass

# def delete_non_pdf_files(directory):
#     for filename in os.listdir(directory):
#         if not filename.endswith('.pdf'):
#             os.remove(os.path.join(directory, filename))
#             speak(f"Deleted {filename}")
#         else:
#             speak(f"Skipped {filename}")

def delete_non_doc_files(directory):
    valid_extensions = ['.pdf', '.docx', '.doc', '.txt']
    for filename in os.listdir(directory):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in valid_extensions:
            os.remove(os.path.join(directory, filename))
            speak(f"Deleted {filename}")
        else:
            speak(f"Skipped {filename}")


def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    try:
        speak("organizing content for output.")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(documents)
        return docs
    except Exception as err:
        speak(f"Couldn't split documents. Error: {err}")
        pass

def setup_embeddings(docs):
    try:

        embeddings = OpenAIEmbeddings(model="ada")
        pinecone.init(api_key="ad1d0ede-9c36-4444-9924-58c1cbe34d5e", environment="us-east1-gcp")
        index_name = "gptdocs"
        index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
        speak("Content almost ready")
        return index
    except Exception as err:
        speak(f"Couldn't initialize embeddings or Pinecone. Error: {err}")
        pass

def get_similiar_docs(index, query, k=2, score=False):
    try:
        if score:
            similar_docs = index.similarity_search_with_score(query, k=k)
        else:
            similar_docs = index.similarity_search(query, k=k)
        return similar_docs
    except Exception as err:
        speak(f"Couldn't retrieve similar documents. Error: {err}")
        pass

def setup_chat_model():
    try:
        chat_model = ChatOpenAI(model="gpt-3.5-turbo")
        return chat_model
    except Exception as err:
        speak(f"Couldn't setup chat model. Error: {err}")
        pass

def load_qa_chain(chat_model):
    try:
        qa_chain = load_qa_chain(chat_model)
        return qa_chain
    except Exception as err:
        speak(f"Couldn't load question answering chain. Error: {err}")
        pass

def get_answer(qa_chain, query, similar_docs):
    try:
        message = {"role": "user", "content": query}
        for doc in similar_docs:
            message["document"] = doc.content
        answer = qa_chain.get_answer(message)
        return answer
    except Exception as err:
        speak(f"Couldn't generate answer. Error: {err}")
        pass



def document_search():

    # download_pdf_files(max_results=5)
    download_files(max_results=10)

    speak("files downloded, initialising preprocessing to meaningfull content. please be patient. This  may take some time depending on the number of documents being used.")

    # load_env_vars()
    directory = '/pdfs'
    setup_directory(directory)
    delete_non_doc_files(directory)

    new_documents = load_docs(directory)
    for doc in new_documents:
        save_processed_file(doc.filename)
    split_documents = split_docs(new_documents)
    index = setup_embeddings(split_documents)
    chat_model = setup_chat_model()
    qa_chain = load_qa_chain(chat_model)

    # Uncomment the lines below if you want to test the full process
    query = get_user_query()
    similar_docs = get_similiar_docs(index, query)
    answer = get_answer(qa_chain, query, similar_docs)
    speak(answer)

