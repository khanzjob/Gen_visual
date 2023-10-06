import requests
import os
from dotenv import find_dotenv, load_dotenv
# import torchaudio
# from speechbrain.pretrained import Tacotron2, HIFIGAN
import streamlit as st
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
# SUNBIRD_MUL_EN_URL = os.getenv("SUNBIRD_MUL_EN_URL")
# HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
# SUNBIRD_EN_LUGA_URL = os.getenv("SUNBIRD_EN_LUGA_URL")
# SUNBIRD_ALL_LOCAL_TO_ENG = os.getenv("SUNBIRD_ALL_LOCAL_TO_ENG")
# SUNBIRD_ACCESSTOKEN = os.getenv("SUNBIRD_ACCESSTOKEN")
# ENGLISH_TO_ALL_LOCAL_URL = os.getenv("ENGLISH_TO_ALL_LOCAL_URL")

SUNBIRD_MUL_EN_URL = "https://api-inference.huggingface.co/models/Sunbird/sunbird-mul-en"
HUGGINGFACE_API_KEY = "Bearer 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"
SUNBIRD_EN_LUGA_URL = "https://api-inference.huggingface.co/models/Sunbird/sunbird-en-lg"
SUNBIRD_ALL_LOCAL_TO_ENG = "https://api-inference.huggingface.co/models/Sunbird/mbart-mul-en"
SUNBIRD_ACCESSTOKEN =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJCcnVuby5Tc2VraXdlcmUiLCJleHAiOjQ4Mzg2ODkxNjB9.o3u4vpxvSd10b552mS5FkATKAVN_R2_uSwC8tP0G-I8"
ENGLISH_TO_ALL_LOCAL_URL = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'

# SUNBIRD_MUL_EN_URL = st.secrets("SUNBIRD_MUL_EN_URL")
# HUGGINGFACE_API_KEY = st.secrets("HUGGINGFACE_API_KEY")
# SUNBIRD_EN_LUGA_URL = st.secrets("SUNBIRD_EN_LUGA_URL")
# SUNBIRD_ALL_LOCAL_TO_ENG = st.secrets("SUNBIRD_ALL_LOCAL_TO_ENG")
# SUNBIRD_ACCESSTOKEN = st.secrets("SUNBIRD_ACCESSTOKEN")
# ENGLISH_TO_ALL_LOCAL_URL = st.secrets("ENGLISH_TO_ALL_LOCAL_URL")

def LocaLToEnglish(query):
    API_URL = SUNBIRD_MUL_EN_URL
    headers = {"Authorization": HUGGINGFACE_API_KEY}

    payload = {"inputs": query}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# def EnglishToLuganda(query):
#     API_URL = SUNBIRD_EN_LUGA_URL
#     headers = {"Authorization": HUGGINGFACE_API_KEY}

#     payload = {"inputs": query}
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

def ALL_LOCAL_TO_ENG(input_text):
    
    API_URL = SUNBIRD_ALL_LOCAL_TO_ENG
    headers = {"Authorization": HUGGINGFACE_API_KEY}

    payload = {"inputs": input_text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()



def ENGLISH_TO_ALL_LOCAL(target_language, text):
    access_token = SUNBIRD_ACCESSTOKEN
    url = ENGLISH_TO_ALL_LOCAL_URL
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Split the text into chunks of up to 200 characters each
    chunks = [text[i:i+200] for i in range(0, len(text), 200)]
    translated_chunks = []
    for chunk in chunks:
        payload = {
            "source_language": "English",
            "target_language": target_language,
            "text": chunk
        }
        response = requests.post(f"{url}/tasks/translate", headers=headers, json=payload)

        if response.status_code == 200:
            translated_chunks.append(response.json()["text"])
        else:
            # Handle the error appropriately (for now, appending the error message)
            translated_chunks.append(f"Error: {response.status_code}, {response.text}")

    # Combine the translated chunks to get the full translated text
    return ' '.join(translated_chunks)
