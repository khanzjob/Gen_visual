
import os
from re import search
import re
import time
import requests
from datetime import datetime
import pygame
from langchain.chat_models import ChatOpenAI
import cv2
import speech_recognition as sr  # required to return a string output by taking microphone input from the user
from dotenv import find_dotenv ,load_dotenv
import sounddevice as sd
import numpy as np
import wavio
import os
import keyboard
from datetime import datetime

# Parameters
RATE = 44100    # Sample rate
CHANNELS = 2    # Number of channels (1=mono, 2=stereo)
DTYPE = np.int16  # Data type
SAVE_FOLDER = "recorded_audios"  # Folder to save the audio files

# Create save folder if it doesn't exist
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def record_audio():
    speak("Recording... Press 'q' to stop and save.")
    
    # Start recording
    audio_data = []
    with sd.InputStream(samplerate=RATE, channels=CHANNELS) as stream:
        while True:
            audio_chunk, overflowed = stream.read(RATE)
            audio_data.append(audio_chunk)
            if keyboard.is_pressed('q'):
                break

    audio_data = np.concatenate(audio_data, axis=0)
    return audio_data

def save_wav(data, filename):
    wavio.write(filename, data, RATE, sampwidth=2)

def list_files(main_folder):
    all_files = []
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def play_audio(file_path):
    # Implement your logic to play audio here
    pass

def search_and_play(query, main_folder):
    all_files = list_files(main_folder)
    matches = [file for file in all_files if query.lower() in os.path.basename(file).lower()]
    
    if not matches:
        print(f"No files found with the name: {query}")
        return
    
    print("\nFound the following matches:")
    for index, path in enumerate(matches, 1):
        print(f"{index}. {path}")

    choice = int(input("\nEnter the file number to play or 0 to exit: "))
    if 0 < choice <= len(matches):
        play_audio(matches[choice-1])

        
def capture_recordings(main_folder, subfolder):
    audio_data = record_audio()
    
    # Ensure the main folder exists
    if not os.path.exists(main_folder):
        os.mkdir(main_folder)
    
    # Ensure the subfolder exists within the main folder
    subfolder_path = os.path.join(main_folder, subfolder)
    if not os.path.exists(subfolder_path):
        os.mkdir(subfolder_path)
    
    # Ensure date-based subfolder exists within the subfolder
    current_date = datetime.now().strftime('%Y-%m-%d')
    date_subfolder_path = os.path.join(subfolder_path, current_date)
    if not os.path.exists(date_subfolder_path):
        os.mkdir(date_subfolder_path)
    
    # Generate the file name based on the current time
    current_time = datetime.now().strftime('%H-%M-%S')
    file_name = os.path.join(date_subfolder_path, f"audio_recording_{current_time}.wav")
    
    save_wav(audio_data, file_name)
    print(f"Audio saved to {file_name}")
    all_files = list_files(main_folder)
    print("\nSummary of files:")
    for index, path in enumerate(all_files, 1):
        print(f"{index}. {path}")
   
def _approve(_input: str) -> bool:
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 200
            r.pause_threshold = 0.5
            msg = (
                "Do you approve of the following input? "
                "Please say 'Yes' or 'No'  within 30 seconds."
            )
            msg += "\n\n" + _input + "\n"
            speak(msg)
            try:
                audio = r.listen(source, timeout=30, phrase_time_limit=30)
                resp = r.recognize_google(audio)
                return resp.lower() in ("yes", "y")
            except Exception as e:
                print(f"An error occurred while recognizing your response: {e}")
                return False
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
voice_id = "pNInz6obpgDQGcFmaJgB"
Vid = os.getenv("voice_id")
elevenLabsAPI = os.getenv("elevenLabsAPI")

def count_tokens(text):
    tokens = text.split()
    NoOfTokens = len(tokens)
    return NoOfTokens

def speak(text):
    # if current_language.lower == "english":
        voice_id = Vid
        api_key = elevenLabsAPI
        CHUNK_SIZE = 1024
        
        # filename = now.strftime("%Y-%m-%d_%H-%M-%S")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_file = f'{timestamp}.mp3'
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            speak(f"HTTP error occurred: {err}")
            return
        except Exception as err:
            speak(f"An error occurred: {err}")
            return

        try:

            directory = datetime.now().strftime('%Y-%m-%d')
            os.makedirs(directory, exist_ok=True)

            file_path = os.path.join(directory, output_file)

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

            # Play the audio file with pygame
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue

            pygame.mixer.quit()  # Release the audio file after playing

            # Delete the audio file after it's been played
            try:
                os.remove(file_path)
            except Exception as err:
                print(f"An error occurred while deleting the file: {err}")

        except Exception as err:
            print(f"An error occurred: {err}")
   
    # elif current_language.lower == "luganda":
    #     translate_text_to_luganda(text)
    # elif current_language.lower == "acholi":
    #     translate_text_to_acholi(text)
    # elif current_language.lower == "ateso":
    #     translate_text_to_ateso(text)
    # elif current_language.lower == "lugbara":
    #     translate_text_to_lugbara(text)
    # elif current_language.lower == "runyankole":
    #     translate_text_to_Runyankole(text)
        
def wishMe():
    hour = int(datetime.now().hour)
    # hour = datetime.datetime.now().hour
    if(hour >= 6) and (hour < 12):
        speak(f"Good Morning ")
    elif(hour >= 12) and (hour < 18):
        speak(f"Good afternoon ")
    elif(hour >= 18) and (hour < 21):
        speak(f"Good Evening ")

def capture_image():
    # speak("wait for 10 seconds and press any button to capture image")
    # speak("press button to capture image after 10 seconds ")
    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Wait for user to press a key to take image
    while True:
        ret, frame = cap.read()
        cv2.imshow('Press Space to Capture Image', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            # Get current date and time
            now = datetime.now()
            filename = now.strftime("%Y-%m-%d_%H-%M-%S")
            # Create directory if it does not exist
            directory = './images/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            # Save image
            filepath = os.path.join(directory, f"{filename}.png")
            cv2.imwrite(filepath, frame)
            # Release camera and close window
            cap.release()
            cv2.destroyAllWindows()
            speak("image captured successfully")
            return filepath    

def speech_to_text():
    # Initialize speech recognizer
    r = sr.Recognizer()
    # Use default system microphone as source to listen to speech
    with sr.Microphone() as source:
        speak("hello, welcome.... How may i be of service....")
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        # Record the user's speech
        audio = r.listen(source)
    try:
        # Use Google speech recognition to convert speech to text
        text = r.recognize_google(audio)
        speak(f"You said: {text}")
        speak("Noted.")
        return text

    except sr.UnknownValueError:
        speak("Sorry, could not understand your input.")
    except sr.RequestError:
        speak("Sorry, there was an error with the speech recognition service.")

        # Return empty string on error
        return ""
    
# Luganda function
# def SetLanguage():
#     r = sr.Recognizer()

#     with sr.Microphone() as source:
        
#         r.adjust_for_ambient_noise(source, duration=5)
#         r.energy_threshold = 200
#         r.pause_threshold = 4

#         while True:
#             text = ""
#             speak("Choose your prefered language from the list below: English, Acholi, Ateso, Luganda, Lugbara and Runyankole")
#             try:
#                 audio = r.listen(source, timeout=90, phrase_time_limit=90)  # Updated to 90 seconds
#                 speak("Recognizing...")
#                 text = r.recognize_google(audio)

#                 approval = _approve(text)
#                 if approval:
#                     LanguageSetting.set_language(text)
#                 else:
#                     continue
#                 speak("language selected :", text)
#                 return text
#             except sr.UnknownValueError:
#                 print("Google Speech Recognition could not understand the audio")
#             except sr.RequestError as e:
#                 print("Could not request results from Google Speech Recognition service; {0}".format(e))

#  ###########################
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
        # loader = DirectoryLoader(directory)
        # documents = loader.load()
        # processed_files = load_processed_files_list()
        # new_documents = [doc for doc in documents if doc.filename not in processed_files]
        # return new_documents
        pass
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
        # speak("organizing content for output.")
        # text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        # docs = text_splitter.split_documents(documents)
        # return docs
        pass
    except Exception as err:
        speak(f"Couldn't split documents. Error: {err}")
        pass

def setup_embeddings(docs):
    try:

        # embeddings = OpenAIEmbeddings(model="ada")
        # pinecone.init(api_key="ad1d0ede-9c36-4444-9924-58c1cbe34d5e", environment="us-east1-gcp")
        # index_name = "gptdocs"
        # index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
        # speak("Content almost ready")
        # return index
        pass
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




def sanitize_and_get_user_query():
    r = sr.Recognizer()
    query = ""
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 200
            r.pause_threshold = 3
            
            while True:
                speak("Note: u  only have one minute for me to capture input. What would you like to research about?. ")
                audio = r.listen(source, timeout=60, phrase_time_limit=60)
                query = r.recognize_google(audio)
                
                approval = _approve(query)  # Add the approval check
                
                if approval:
                    break
                else:
                    speak("Sorry, the query you provided is not approved. Please try again.")
    except sr.WaitTimeoutError:
        print("Timeout error: the speech recognition operation timed out")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand your query. Please try again.")
    except sr.RequestError as e:
        speak(f"Could not request results from the speech recognition service; check your internet connection: {e}")
    except Exception as e:
        speak(f"An error occurred: {e}")
    
    return re.sub(r'(?u)[^-\w.]', '', query)


def download_files(max_results=4, base_directory='./pdfs'):
    keyword = sanitize_and_get_user_query()

    today = datetime.today().strftime('%Y-%m-%d')
    directory = os.path.join(base_directory, today)
    os.makedirs(directory, exist_ok=True)

    extensions = ['.pdf', '.docx', '.doc', '.txt']
    speak("Initializing downloads from the internet. This may take some time depending on your internet speed. Please wait for the response.")
    for url in search(keyword, num_results=max_results):
        try:
            response = requests.get(url, timeout=15)
        except requests.exceptions.RequestException as err:
            print(f"Couldn't download file {url}. Error: {err}")
            continue

        file_ext = os.path.splitext(url)[1].lower()
        if file_ext in extensions:
            filename = os.path.basename(url)
            if not os.path.isfile(os.path.join(directory, filename)):
                try:
                    with open(os.path.join(directory, filename), 'wb') as f:
                        f.write(response.content)
                    speak(f"Downloaded {filename}")
                except Exception as err:
                    print(f"Couldn't write file {filename}. Error: {err}")
                    continue
        else:
            speak(f"Skipped {url}")

    speak("Downloaded files successfully")




def sanitize(filename):
    return re.sub(r'(?u)[^-\w.]', '', filename)

def count_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return len(files)


def get_user_query(lg):
    r = sr.Recognizer()
    query = ""
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 200
            r.pause_threshold = 3
            
            while True:
                
                speak("Note: u  only have one minute for me to capture input. What would you like to research about?. ")
                audio = r.listen(source, timeout=60, phrase_time_limit=60)
                query = r.recognize_google(audio)
                # speak(f"Your query is: {query}")
                
                approval = _approve(query)  # Add the approval check
                
                if approval:
                    break
                else:
                    speak("Sorry, the query you provided is not approved. Please try again.")
    except sr.WaitTimeoutError:
        print("Timeout error: the speech recognition operation timed out")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand your query. Please try again.")
    except sr.RequestError as e:
        speak(f"Could not request results from the speech recognition service; check your internet connection: {e}")
    except Exception as e:
        speak(f"An error occurred: {e}")
    
    return query

def _download_pdf_filest( max_results=10, base_directory='./pdfs'):

    keyword = get_user_query()
    # Generate directory name for today's date
    today = datetime.today().strftime('%Y-%m-%d')
    directory = os.path.join(base_directory, today)
    
    # Create the directory to save the pdf files if it does not exist
    os.makedirs(directory, exist_ok=True)

    query = keyword + " filetype:pdf"

    # List to store the names of downloaded files
    downloaded_files = []

    # Search the web with the keyword
    speak("iNITIALIZING DOWNLOADS")
    for url in search(query, num_results=max_results):
        try:
            
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as err:
            print(f"Couldn't download file {url}. Error: {err}")
            continue

        # Check if the response content type is pdf
        if response.headers['content-type'] == 'application/pdf':
            # Extract the pdf file name from the url and sanitize it
            filename = sanitize(os.path.basename(url))
            
            # Check if the file already exists
            if not os.path.isfile(os.path.join(directory, filename)):
                try:
                    # Download and save the pdf file
                    with open(os.path.join(directory, filename), 'wb') as f:
                        f.write(response.content)
                    downloaded_files.append(filename)  # Add the file name to the list
                    speak("DOWNLOADED {filename}")
                except Exception as err:
                    print(f"Couldn't write file {filename}. Error: {err}")
                    continue

    # After downloading all files, print the count and the names
    # speak(f"Downloaded {len(downloaded_files)} files:")
    # speak(f"Downloaded filesnames include :")
    speak(f"Downloaded files successfully")



