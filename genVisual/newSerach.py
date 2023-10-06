import os
import re
import requests
import speech_recognition as sr
from datetime import datetime
from googlesearch import search
from TTS import speak
from _approve import _approve


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


# def download_pdf_files(max_results=4, base_directory='./pdfs'):
#     keyword = sanitize_and_get_user_query()

#     today = datetime.today().strftime('%Y-%m-%d')
#     directory = os.path.join(base_directory, today)
#     os.makedirs(directory, exist_ok=True)

#     query = keyword + " filetype:pdf"
#     speak("Initializing downloads from the internet. This may take sometime  depending on your internet speed. in the meantime relax and wait for response.")
#     for url in search(query, num_results=max_results):
#         try:
#             response = requests.get(url, timeout=15)
#         except requests.exceptions.RequestException as err:
#             print(f"Couldn't download file {url}. Error: {err}")
#             continue

#         if response.headers['content-type'] == 'application/pdf':
#             filename = os.path.basename(url)
#             if not os.path.isfile(os.path.join(directory, filename)):
#                 try:
#                     with open(os.path.join(directory, filename), 'wb') as f:
#                         f.write(response.content)
#                     speak(f"Downloaded {filename}")
#                 except Exception as err:
#                     print(f"Couldn't write file {filename}. Error: {err}")
#                     continue

#     speak(f"Downloaded files successfully")

# if __name__ == "__main__":
#     download_pdf_files(max_results=15)

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
