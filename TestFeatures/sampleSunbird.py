import os
import requests
from dotenv import find_dotenv, load_dotenv
import textwrap
import base64

from TTS import count_tokens


def translate_text_to_luganda(query):
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    access_token = os.getenv("SunbirdAccessToken")

    url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "source_language": "English",
        "target_language": "Luganda",
        "text": query
    }

    tokenz = count_tokens(query)

    if tokenz <= 199 :
        response = requests.post(f"{url}/tasks/translate", headers=headers, json=payload)

        if response.status_code == 200:
            translated_text = response.json()["text"]
            print("Translate text:", translated_text)
        else:
            print("Error:", response.status_code, response.text)
    elif tokenz >=200:
        translate_batch_text_to_luganda()


    




def SpeechToText(file_path):
    url = "https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app/tasks/stt"
    access_token = os.getenv("SunbirdAccessToken")
    headers = {'Authorization': f'Bearer {access_token}'}

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        files = [('audio', (file_path, file, 'audio/wav'))]
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        print("Response text:", response.text)
        return response.text
    else:
        print("Error:", response.status_code, response.text)
        return None



def text_to_speech_lg(query):
    url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app/tasks/tts'
    access_token = os.getenv("SunbirdAccessToken")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": query
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        base64_string = response.json()["base64_string"]
        with open("temp.wav", "wb") as wav_file:
            decoded_audio = base64.decodebytes(base64_string.encode('utf-8'))
            wav_file.write(decoded_audio)
    else:
        print("Error:", response.status_code, response.text)



def translate_batch_text_to_luganda(query):
    url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'
    access_token = os.getenv("SunbirdAccessToken")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Remove unnecessary spaces
    query = ' '.join(query.split())

    # Split the query into chunks of 200 characters or less
    chunks = textwrap.wrap(query, 200)

    # Create requests payload
    requests_payload = []
    for chunk in chunks:
        requests_payload.append({
            "source_language": "English",
            "target_language": "Luganda",
            "text": chunk
        })

    payload = {"requests": requests_payload}

    response = requests.post(f"{url}/tasks/translate-batch", headers=headers, json=payload)

    if response.status_code == 200:
        translated_text = response.json()
        print("Translated text:", translated_text)
    else:
        print("Error:", response.status_code, response.text)
        return None  # Return None if there's an error

def translate_batch_text_to_acholi(query):
    url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'
    access_token = os.getenv("SunbirdAccessToken")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Remove unnecessary spaces
    query = ' '.join(query.split())

    # Split the query into chunks of 200 characters or less
    chunks = textwrap.wrap(query, 200)

    # Create requests payload
    requests_payload = []
    for chunk in chunks:
        requests_payload.append({
            "source_language": "English",
            "target_language": "Acholi",
            "text": chunk
        })

    payload = {"requests": requests_payload}

    response = requests.post(f"{url}/tasks/translate-batch", headers=headers, json=payload)

    if response.status_code == 200:
        translated_text = response.json()
        print("Translated text:", translated_text)
    else:
        print("Error:", response.status_code, response.text)
        return None  # Return None if there's an error  

def translate_text_to_acholi(query):
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    access_token = os.getenv("SunbirdAccessToken")

    url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "source_language": "English",
        "target_language": "Acholi",
        "text": query
    }

    tokenz = count_tokens(query)

    if tokenz <= 199 :
        response = requests.post(f"{url}/tasks/translate", headers=headers, json=payload)

        if response.status_code == 200:
            translated_text = response.json()["text"]
            print("Translate text:", translated_text)
        else:
            print("Error:", response.status_code, response.text)
    elif tokenz >=200:
        translate_batch_text_to_acholi()





def translate_batch_text_to_ateso(query):
    url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'
    access_token = os.getenv("SunbirdAccessToken")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Remove unnecessary spaces
    query = ' '.join(query.split())

    # Split the query into chunks of 200 characters or less
    chunks = textwrap.wrap(query, 200)

    # Create requests payload
    requests_payload = []
    for chunk in chunks:
        requests_payload.append({
            "source_language": "English",
            "target_language": "Ateso",
            "text": chunk
        })

    payload = {"requests": requests_payload}

    response = requests.post(f"{url}/tasks/translate-batch", headers=headers, json=payload)

    if response.status_code == 200:
        translated_text = response.json()
        print("Translated text:", translated_text)
    else:
        print("Error:", response.status_code, response.text)
        return None  # Return None if there's an error  
def translate_text_to_ateso(query):
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    access_token = os.getenv("SunbirdAccessToken")

    url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "source_language": "English",
        "target_language": "Ateso",
        "text": query
    }

    tokenz = count_tokens(query)

    if tokenz <= 199 :
        response = requests.post(f"{url}/tasks/translate", headers=headers, json=payload)

        if response.status_code == 200:
            translated_text = response.json()["text"]
            print("Translate text:", translated_text)
        else:
            print("Error:", response.status_code, response.text)
    elif tokenz >=200:
        translate_batch_text_to_ateso()

def translate_text_to_lugbara(query):
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    access_token = os.getenv("SunbirdAccessToken")

    url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "source_language": "English",
        "target_language": "Lugbara",
        "text": query
    }

    tokenz = count_tokens(query)

    if tokenz <= 199 :
        response = requests.post(f"{url}/tasks/translate", headers=headers, json=payload)

        if response.status_code == 200:
            translated_text = response.json()["text"]
            print("Translate text:", translated_text)
        else:
            print("Error:", response.status_code, response.text)
    elif tokenz >=200:
        translate_batch_text_to_Lugbara()

def translate_text_to_Runyankole(query):
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    access_token = os.getenv("SunbirdAccessToken")

    url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "source_language": "English",
        "target_language": "Runyankole",
        "text": query
    }

    tokenz = count_tokens(query)

    if tokenz <= 199 :
        response = requests.post(f"{url}/tasks/translate", headers=headers, json=payload)

        if response.status_code == 200:
            translated_text = response.json()["text"]
            print("Translate text:", translated_text)
        else:
            print("Error:", response.status_code, response.text)
    elif tokenz >=200:
        translate_batch_text_to_Runyankole()




querry = "The Software Development Life Cycle (SDLC) is a structured process that enables the production\
of high-quality, low-cost software, in the shortest possible production time. The goal of the SDLC is to produce\
 superior software that meets and exceeds all customer expectations and demands. The SDLC defines and outlines a \
 detailed plan with stages, or phases, that each encompass their own process and deliverables. Adherence to the \
 SDLC enhances development speed and minimizes project risks and costs associated with alternative methods of \
 production.The initial concept and creation of the SDLC only addressed security activities as a separate and \
 singular task, performed as part of the testing phase. The shortcomings of this after-the-fact approach were \
 the inevitably high number of vulnerabilities or bugs discovered too late in the process, or in certain cases,\
   not discovered at all. Today, it is understood that security is critical to a successful SDLC, and that \
   integrating security activities throughout the SDLC helps create more reliable software. By incorporating \
   security practices and measures into the earlier phases of the SDLC, vulnerabilities are discovered and \
   mitigated earlier, thereby minimizing overall time involved, and reducing costly fixes later in the life cycle.\
This idea of baking-in security provides a Secure SDLC- a concept widely recognized and adopted in the software industry today. A secure SDLC is achieved by conducting security assessments and practices during ALL phases of software development"

Querry2 = "This idea of baking-in security provides a Secure SDLC- a concept widely recognized and adopted in "

# translate_text_to_luganda(querry)

translate_batch_text_to_luganda(querry)