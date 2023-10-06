from TTS import speak
import speech_recognition as sr


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
    
    
