from langchain.document_loaders import BSHTMLLoader, DirectoryLoader,TextLoader
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain import SerpAPIWrapper
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import  LLMChain
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings

from dotenv import find_dotenv, load_dotenv
dotenv_path= find_dotenv()
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
os.environ["OPENAI_API_KEY"] ="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"
os.environ["SERPAPI_API_KEY"] ="84c5633c21ec443a55d46de3d8dcfe90218c061e0fae4ea4eb1573ae3f0b12fa"

txt_dir_loader = DirectoryLoader('C:\\Users\\DELL\\Desktop\\Marvin\\Gen_visual\\documentProcessing\\data', loader_cls=TextLoader)
txt_data = txt_dir_loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 20,
    length_function = len,
)
txt_documents = text_splitter.split_documents(txt_data)
embeddings = OpenAIEmbeddings()
persist_directory = "vector_db"
vectordb = Chroma.from_documents(documents=txt_documents, embedding=embeddings, persist_directory=persist_directory)
vectordb.persist()
vectordb = None
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
# vectordb.similarity_search("rabbit")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
doc_retriever = vectordb.as_retriever()
search = SerpAPIWrapper()
memory = ConversationBufferMemory(memory_key="chat_history")
readonlymemory = ReadOnlySharedMemory(memory=memory)
alice_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_retriever, memory=readonlymemory)
tools = [
      Tool(
        name="Science Studies QA System",
        func=alice_qa.run,
        description="Useful for answering questions related to science studies. Input should be a fully formed question."
    ),
    Tool(
        name="Backup Science Google Search",
        func=search.run,
        description="Useful for when the Science Studies QA System couldn't find an answer. This tool will perform a Google search. Input should be a fully formed question."
    ),
]

prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"]
)

llm_chain = LLMChain(llm=llm, prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(agent=agent,handle_parsing_errors=True, tools=tools, verbose=True, memory=memory)
print(agent_chain.run(input="What is the deal with the Cheshire Cat?"))