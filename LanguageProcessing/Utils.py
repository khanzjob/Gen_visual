from google.cloud import translate
import os
from dotenv import find_dotenv, load_dotenv

# Load environment variables from .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Get project ID and location from environment variables
project_id = os.getenv("GOOGLE_CLOUD_ID")
run_location = os.getenv("GOOGLE_CLOUD_LOCATION")

def translate_text(query: str, project_id: str = project_id) -> translate.TranslationServiceClient:
    """translates the input text to the target language using Google Cloud Translation API."""

    # Initialize Translation client
    client = translate.TranslationServiceClient()

    # Construct the parent parameter
    location = run_location
    parent = f"projects/{project_id}/locations/{location}"

    # translate text from English to French
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "en",
            "target_language_code": "fr",
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print(f"translated text: {translation.translated_text}")

    return response

# Example usage:
if __name__ == "__main__":
    query = "The input text can be plain text or HTML. Cloud Translation API does not translate any HTML tags in the input, only text that appears between the tags. The output retains the (untranslated) HTML tags, with the translated text between the tags to the extent possible due to differences between the source and target languages. The order of HTML tags in the output may differ from the order in the input text due to word order changes in the"
    translate_text(query)
