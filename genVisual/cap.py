
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from TTS import capture_image, speak
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import speech_recognition as sr
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def _approve(_input: str) -> bool:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = 200
        r.pause_threshold = 0.5
        msg = (
            "Do you approve of the following input? "
            "Please say 'Yes' or 'No'."
        )
        msg += "\n\n" + _input + "\n"
        speak(msg)
        try:
            audio = r.listen(source, timeout=50, phrase_time_limit=50)
            resp = r.recognize_google(audio)
            return resp.lower() in ("yes", "y")
        except Exception as e:
            speak(f"An error occurred while recognizing your response: {e}")
            return False


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


def local_image_to_pil(path):
    img = Image.open(path).convert('RGB')
    return img


def generate_image_captions():
    local_model_dir = 'C:/Users/jukas/Desktop/LangChain/hackathon/captions'

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



