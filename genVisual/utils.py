import speech_recognition as sr
    
    
import os
import time
import requests
from datetime import datetime
import pygame
import cv2
import speech_recognition as sr  # required to return a string output by taking microphone input from the user
from dotenv import find_dotenv ,load_dotenv
# from languageSetting import LanguageSetting

# from sampleSunbird import text_to_speech_lg, translate_text_to_Runyankole, translate_text_to_acholi, 
# translate_text_to_ateso, translate_text_to_luganda, translate_text_to_lugbara

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
Vid = os.getenv("voice_id")
elevenLabsAPI = os.getenv("elevenLabsAPI")

current_language = LanguageSetting.get_language()

def count_tokens(text):
    tokens = text.split()
    NoOfTokens = len(tokens)
    return NoOfTokens


def speak(text):
    

    if current_language.lower == "english":
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
            print(f"HTTP error occurred: {err}")
            return
        except Exception as err:
            print(f"An error occurred: {err}")
            return

        try:
            directory = datetime.now().strftime('%Y-%m-%d')
            os.makedirs(directory, exist_ok=True)
            
            # Delete all files in the directory
            try:
                file_list = os.listdir(directory)
                for file_name in file_list:
                    file_path = os.path.join(directory, file_name)
                    if os.path.isfile(file_path):
                        time.sleep(0.1)
                        os.remove(file_path)
            except Exception as err:
                print(f"An error occurred while deleting files: {err}")
            
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
        
        except Exception as err:
            print(f"An error occurred: {err}")
   
    elif current_language.lower == "luganda":
        translate_text_to_luganda(text)
    elif current_language.lower == "acholi":
        translate_text_to_acholi(text)
    elif current_language.lower == "ateso":
        translate_text_to_ateso(text)
    elif current_language.lower == "lugbara":
        translate_text_to_lugbara(text)
    elif current_language.lower == "runyankole":
        translate_text_to_Runyankole(text)
        
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
def SetLanguage():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        
        r.adjust_for_ambient_noise(source, duration=5)
        r.energy_threshold = 200
        r.pause_threshold = 4

        while True:
            text = ""
            speak("Choose your prefered language from the list below: English, Acholi, Ateso, Luganda, Lugbara and Runyankole")
            try:
                audio = r.listen(source, timeout=90, phrase_time_limit=90)  # Updated to 90 seconds
                speak("Recognizing...")
                text = r.recognize_google(audio)

                approval = _approve(text)
                if approval:
                    LanguageSetting.set_language(text)
                else:
                    continue
                speak("language selected :", text)
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

