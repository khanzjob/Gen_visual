
import requests
from PIL import Image
from utils import _approve, capture_image, speak
from transformers import BlipProcessor, BlipForConditionalGeneration
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import speech_recognition as sr
import os
from dotenv import find_dotenv, load_dotenv

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}

dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = "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"

template = """
Interpreting the Image Caption:

Caption: {caption}

Please contribute your insights, interpretations, or clarifications to help unravel the meaning behind the generated caption.

Let's embark on this meaningful journey together, embracing the opportunities presented by image captioning and the power of ChatGPT!

"""
prompt = PromptTemplate(input_variables=["caption"], template=template)
chatgpt_chain = LLMChain(
    llm=OpenAI(temperature=0),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
) 



def generate_image_captions():
    # local_model_dir = 'C:\\Users\DELL\\Desktop\\Marvin\\Gen_visual\\genVisual\\captions'

    try:
       
        img_path = capture_image()
        
        caption = query(img_path)
        generated_text = caption[0]['generated_text']
        speak("Caption generated: " + generated_text)

        if _approve("Do you want to retake the image?"):
            generate_image_captions()
        else:
            interpretation = chatgpt_chain.predict(caption=generated_text)
            speak("Interpretation:")
            speak(interpretation)

    except Exception as e:
        speak("An error occurred: " + str(e))
        print(("An error occurred: " + str(e)))
        if _approve("Do you want to retake the image?"):
            generate_image_captions()
        else:
            speak("Caption generation failed.")
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

# generate_image_captions() 


