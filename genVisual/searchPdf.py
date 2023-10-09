

import os
import re
import requests
from datetime import datetime
from .utils import speak
from googlesearch import search
import speech_recognition as sr


from _approve import _approve


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

def download_pdf_files( max_results=10, base_directory='./pdfs'):

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

# luganda 

