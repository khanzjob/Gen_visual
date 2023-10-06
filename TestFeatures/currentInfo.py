from langchain.utilities import GoogleSerperAPIWrapper
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, Tool, AgentType
import os
from dotenv import find_dotenv ,load_dotenv

from TTS import speak
dotenv_path= find_dotenv()
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY =  os.getenv("SERPAPI_KEY")


llm = OpenAI(temperature=0)
search = GoogleSerperAPIWrapper()

def run_google_serper(prompt):
    try:
        tools = [
            Tool(
                name="Intermediate Answer",
                func=search.run,
                description="useful for when you need to ask with search"
            )
        ]

        self_ask_with_search = initialize_agent(tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)
        answer = self_ask_with_search.run(prompt)
        speak(answer)
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I encountered an error while processing your request.")

run_google_serper("history of ugnda christian university")