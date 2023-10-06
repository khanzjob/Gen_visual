


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
from langchain.vectorstores import Chroma
from langchain.chains import RetrievaQA
from langchain.llms import OpenAI
from datetime import datetime

from TTS import speak

try:
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
except Exception as err:
    speak(f"Couldn't load environment variables. Error: {err}")
    exit()

def load_processed_files_list():
    speak("Loading files for preprocessing")
    
    try:
        if os.path.exists('processed_files.txt'):
            with open('processed_files.txt', 'r') as f:
                return f.read().splitlines()
        else:
            return []
    except Exception as err:
        speak(f"Couldn't load processed files list. Error: {err}")
        exit()

def save_processed_file(file):
    try:
        with open('processed_files.txt', 'a') as f:
            f.write(f"{file}\n")
    except Exception as err:
        speak(f"Couldn't save processed file. Error: {err}")
        exit()

def load_docs(directory):
    speak("Loading file directory for preprocessing")
    try:
        loader = DirectoryLoader(directory)
        documents = loader.load()
      
        processed_files = load_processed_files_list()
        new_documents = [doc for doc in documents if doc.filename not in processed_files]
      
        return new_documents
    except Exception as err:
        speak(f"Couldn't load documents. Error: {err}")
        exit()

try:
    directory = 'C:/Users/jukas/Desktop/LangChain/pdfs/'
    today = datetime.today().strftime('%Y-%m-%d')
    directory = os.path.join(directory, today)
    os.makedirs(directory, exist_ok=True)
except Exception as err:
    speak(f"Couldn't create directory. Error: {err}")
    exit()

def delete_non_pdf_files(directory):
    speak("cleaning files for preprocessing")
    for filename in os.listdir(directory):
        if not filename.endswith('.pdf'):
            os.remove(os.path.join(directory, filename))
            print(f"Deleted {filename}")
        else:
            speak(f"Skipped {filename}")

try:
    delete_non_pdf_files(directory)
    speak("files cleaned successfully to pdf only.")
    documents = load_docs(directory)
    speak("pdfs loaded successfully")
except Exception as err:
    speak(f"Couldn't delete non-pdf files or load documents. Error: {err}")
    exit()

def split_docs(documents,chunk_size=1000,chunk_overlap=20):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(documents)
        return docs
    except Exception as err:
        speak(f"Couldn't split documents. Error: {err}")
        exit()

try:
    docs = split_docs(documents)
    print(len(docs))
    print("pdfs splitting completed successfully")
except Exception as err:
    print(f"Couldn't split documents. Error: {err}")
    exit()

try:
    embeddings = OpenAIEmbeddings(model="ada")

    pinecone.init(
        api_key="99d7dd90-0e36-49af-8757-338526a1e150",  # find at app.pinecone.io
        environment="asia-southeast1-gcp-free"  # next to api key in console
    )

    index_name = "hack"
    index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
except Exception as err:
    print(f"Couldn't initialize embeddings or Pinecone. Error: {err}")
    exit()

def get_similiar_docs(query,k=2,score=False):
    try:
        if score:
            similar_docs = index.similarity_search_with_score(query,k=k)
        else:
            similar_docs = index.similarity_search(query,k=k)
        return similar_docs
    except Exception as err:
        print(f"Couldn't get similar documents. Error: {err}")
        exit()

try:
    # query = "How is india's economy"
    # similar_docs = get_similiar_docs(query)
    # similar_docs
    print("embeddings complete")
    model_name = "gpt-3.5-turbo"
    llm = ChatOpenAI(model_name=model_name)
    chain = load_qa_chain(llm, chain_type="stuff")
except Exception as err:
    print(f"Couldn't complete embeddings or initialize chat model. Error: {err}")
    

def get_answer(query):
    try:
        similar_docs = get_similiar_docs(query)
        answer =  chain.run(input_documents=similar_docs, question=query)
        return  answer
    except Exception as err:
        print(f"Couldn't get answer. Error: {err}")
        
