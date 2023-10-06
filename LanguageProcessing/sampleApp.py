import streamlit as st
import requests
import os
from dotenv import find_dotenv, load_dotenv

# Load environment variables from .env
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Function to translate from any local language to English
def ALL_LOCAL_TO_ENG(input_text):
    API_URL = os.getenv("SUNBIRD_ALL_LOCAL_TO_ENG")
    headers = {"Authorization": os.getenv("HUGGINGFACE_API_KEY")}

    payload = {"inputs": input_text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to translate from English to any local language
def ENGLISH_TO_ALL_LOCAL(target_language, text):
    access_token = os.getenv("SUNBIRD_ACCESSTOKEN")
    url = os.getenv("ENGLISH_TO_ALL_LOCAL_URL")

    # First, translate the input text to English
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "source_language": target_language,
        "target_language": "English",
        "text": text
    }

    response = requests.post(f"{url}/tasks/translate", headers=headers, json=payload)

    if response.status_code == 200:
        english_text = response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

    # Now, translate the English text to the target local language
    headers["Authorization"] = os.getenv("HUGGINGFACE_API_KEY")
    payload["source_language"] = "English"
    payload["target_language"] = target_language
    payload["text"] = english_text

    response = requests.post(f"{url}/tasks/translate", headers=headers, json=payload)

    if response.status_code == 200:
        translated_text = response.json()
        return translated_text
    else:
        return f"Error: {response.status_code}, {response.text}"

def main():
    st.title("Language Translation App")

    translation_option = st.selectbox(
        "Choose translation option:",
        ("Translate all languages to English", "Translate all languages to Local")
    )

    if translation_option == "Translate all languages to English":
        input_text = st.text_area("Enter text to translate:", height=150)
        if st.button("Translate"):
            translated_text = ALL_LOCAL_TO_ENG(input_text)
            st.write("Translated text to English:")
            st.write(translated_text)

    elif translation_option == "Translate all languages to Local":
        target_language = st.text_input("Enter target language (e.g., Acholi):")
        input_text = st.text_area("Enter text to translate:", height=150)
        if st.button("Translate"):
            # First, translate input text to English
            english_text = ENGLISH_TO_ALL_LOCAL("English", input_text)

            # Now, translate English text to the target local language
            translated_text = ENGLISH_TO_ALL_LOCAL(target_language, english_text)

            st.write(f"Translated text to {target_language}:")
            st.write(translated_text)

if __name__ == "__main__":
    main()
