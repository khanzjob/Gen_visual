import json
from genVisual.utils import _approve, speak, wishMe
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import os
from dotenv import find_dotenv, load_dotenv
import speech_recognition as sr
import pyttsx3
from datetime import datetime
from ReadKeras import process_image
from cap import generate_image_captions


from genVisual.newPDFProcess import document_search

dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

template = """
TOM  is your assistant trained by OpenAI.

TOM  is designed to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics.

TOM is constantly learning and improving. It processes and understands large amounts of text, and uses this knowledge to provide accurate and informative responses.

Be aware that some errors might occur in the transcription of our conversations due to the audio input. TOM will attempt to account for words that may have been misinterpreted due to their similarity in sound.

Here is your conversation history:
{history}

TOM: {human_input}
USER:"""

def save_user_name(user_name):
    with open("user_name.txt", "w") as file:
        file.write(user_name)

def get_user_name():
    if os.path.exists("user_name.txt"):
        with open("user_name.txt", "r") as file:
            return file.read()
    return None

def save_conversation(user_input, bot_response):
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    conversation = {
        "datetime": current_datetime,
        "user_input": user_input,
        "bot_response": bot_response
    }
    conversation_dir = "conversations"
    if not os.path.exists(conversation_dir):
        os.makedirs(conversation_dir)
    file_path = os.path.join(conversation_dir, f"conversation_{current_datetime}.json")
    with open(file_path, "w") as file:
        json.dump(conversation, file)

def get_names():
    r = sr.Recognizer()
    user_name = get_user_name()
    bot_name = "Tom"
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 200
            r.pause_threshold = 0.5

            if user_name:
                speak(f"Welcome back, {user_name}!")
            else:
                speak("Hi there. i would like to know you better. What's your name?")
                audio = r.listen(source, timeout=30, phrase_time_limit=30) # Updated to 90 seconds
                user_name = r.recognize_google(audio)
                speak(f"I'm Tom. Nice to meet you, {user_name}.")

                # SetLanguage()
                
                help_content = """
                        Here are some available commands:
                        - Search: Perform a PDF search basing on input
                        - Caption Image: Generate captions for an image
                        - Read: Perform image reading, recognising text from image and and making sense out of it. 
                        - send message : use whatsap for messenging
                        - translate : feature to translate specch to sign language and signlanguage to speech            
                        - Help: Display available commands
                        """
                speak(f"Kindly consider the folowing. {help_content}")

                save_user_name(user_name)

    except sr.WaitTimeoutError:
        print("Timeout error: the speech recognition operation timed out")
        return get_names()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand your input. No worries, let's try that again.")
        return get_names()
    except sr.RequestError as e:
        print(f"Could not request results from the speech recognition service; check your internet connection: {e}")
        return get_names()
    except Exception as e:
        print(f"An error occurred: {e}")
        return get_names()
    return user_name, bot_name

prompt = PromptTemplate(input_variables=[ "history", "human_input"], template=template)
chatgpt_chain = LLMChain(
    llm=OpenAI(temperature=0),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
)

engine = pyttsx3.init()

def listen():
    r = sr.Recognizer()
    wishMe()
    get_names()

    try:

        with sr.Microphone() as source:
            speak("Initializing microphone for use...")
            r.adjust_for_ambient_noise(source, duration=5)
            r.energy_threshold = 200
            r.pause_threshold = 4

            speak("Okay, let's get started!. One sec please")
            while True:
                text = ""
                speak("Listening for new input. now...")
                try:
                    audio = r.listen(source, timeout=90, phrase_time_limit=90) # Updated to 90 seconds
                    speak("Recognizing...")
                    text = r.recognize_google(audio)
                    # Add conditionals for triggering your functions based on the recognized text
                    keyword_found = False

                    if 'search' in text.lower():
                        document_search()
                        keyword_found = True
                    elif 'caption image' in text.lower():
                        speak("image caption function selected")
                        generate_image_captions()
                        keyword_found = True
                    elif 'read' in text.lower():
                        speak("read function selected")
                        process_image()
                        keyword_found = True
                    elif 'send message' in text.lower():
                        # function goes here
                        keyword_found = True
                    elif 'translate' in text.lower():
                            #translate function goes here
                            keyword_found = True

                    elif 'help' in text.lower():
                        help_content = """
                        Here are some available commands:
                        - Search: Perform a PDF search basing on input
                        - Caption Image: Generate captions for an image
                        - Read: Perform image reading, recognising text from image and and making sense out of it. 
                        - send message : use whatsap for messenging
                        - translate : feature to translate specch to sign language and signlanguage to speech            
                        - Help: Display available commands
                        """
                        speak("Sure!.")
                        speak(help_content)
                        keyword_found = True

                    if not keyword_found:
                        approval = _approve(text)
                        if not approval:
                            continue

                except sr.WaitTimeoutError:
                    print("Timeout error: the speech recognition operation timed out")
                    continue
                except sr.UnknownValueError:
                    speak("Could not understand the audio")
                    continue
                except sr.RequestError as e:
                    speak(f"Could not request results from the speech recognition service; check your internet connection: {e}")
                    continue
                except Exception as e:
                    speak(f"An error occurred: {e}")
                    continue

                # If no keyword found, process the input
                if not keyword_found:
                    speak("Processing your input: " + text)

                    response_text = chatgpt_chain.predict(human_input=text)
                    if response_text.lower() == 'goodbye':
                        speak("See you later!")
                        exit()

                    speak(response_text)
                    save_conversation(text, response_text)
                engine.runAndWait()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    listen()



