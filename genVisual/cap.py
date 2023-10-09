
import requests
from PIL import Image
from utils import _approve, capture_image, speak
from transformers import BlipProcessor, BlipForConditionalGeneration
from langchain import OpenAI, LLMChain, PromptTemplate
# from langchain.memory import ConversationBufferWindowMemory
import speech_recognition as sr
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY



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
    # memory=ConversationBufferWindowMemory(k=2),
)


def local_image_to_pil(path):
    img = Image.open(path).convert('RGB')
    return img


def generate_image_captions():
    local_model_dir = 'C:\Users\DELL\Desktop\Marvin\Gen_visual\genVisual\captions'

    try:
        processor = BlipProcessor.from_pretrained(local_model_dir)
        model = BlipForConditionalGeneration.from_pretrained(local_model_dir)

        img_path = capture_image()
        img_url = local_image_to_pil(img_path)
        raw_image = img_url

        text = "a photography of"
        inputs = processor(raw_image, text, return_tensors="pt")

        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        print(caption)

        speak("Caption generated: " + caption)

        if _approve("Do you want to retake the image?"):
            generate_image_captions()
        else:
            interpretation = chatgpt_chain.predict(caption=caption)
            speak("Interpretation:")
            speak(interpretation)

    except Exception as e:
        speak("An error occurred: " + str(e))
        if _approve("Do you want to retake the image?"):
            generate_image_captions()
        else:
            speak("Caption generation failed.")



