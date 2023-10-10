import os
import speech_recognition as sr
import sys
# sys.path.append('C:/Users/DELL/Desktop/Marvin/Gen_visual/Calls_Messaging')
sys.path.append('C:/Users/DELL/Desktop/Marvin/Gen_visual/genVisual')
# import discordBot
import utils
def get_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = 200
        r.pause_threshold = 4
        audio = r.listen(source, timeout=30, phrase_time_limit=30)
        try:
            user_input = r.recognize_google(audio)
            return user_input
        except sr.UnknownValueError:
            utils.speak("Sorry, I did not catch that. Please speak again.")
            return get_user_input()  # recursively prompt the user to speak again
        except sr.RequestError:
            # API was unreachable or unresponsive
            utils.speak("API unavailable. Please try again later.")
            return None

class SubjectManager:
    def __init__(self, file_path="subjects.txt"):
        self.file_path = file_path
        # Load subjects from the text file
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.subjects = [line.strip() for line in f.readlines()]
        else:
            self.subjects = []

    def _update_file(self):
        """Update the text file with the current subjects."""
        with open(self.file_path, 'w') as f:
            for subject in self.subjects:
                f.write(f"{subject}\n")

    def list_subjects(self):
        return self.subjects

    def add_subject(self, subject_name):
        if subject_name not in self.subjects:
            self.subjects.append(subject_name)
            self._update_file()
            response = f"'{subject_name}' added successfully!"
            utils.speak(response)
        else:
            response = f"'{subject_name}' already exists!"
            utils.speak(response)

    def remove_subject(self, subject_name):
        if subject_name in self.subjects:
            self.subjects.remove(subject_name)
            self._update_file()
            response =f"'{subject_name}' removed successfully!"
            utils.speak(response)
        else:
            response =  f"'{subject_name}' not found!"
            utils.speak(response)

    def process_voice_commands(self):
        utils.speak("Welcome to the Voice Command Subject Manager!,You can say 'list subjects', 'add', or 'remove' followed by the subject name.")
        
        while True:
            utils.speak("Ready and....go.")
            command = get_user_input()
            
            if command is None:
                utils.speak("No input detected. Exiting...")
                break

            command = command.lower()

            if 'exit' in command:
                utils.speak("Well thank you.... Exiting...")
                break
            
            if 'list subjects' in command:
                subjects = self.list_subjects()
                utils.speak(f"Here are the available subjects: {', '.join(subjects)}")
            
            elif 'add' in command:
                subject_name = command.replace('add', '').strip()
                if utils._approve(f"Add the subject: {subject_name}?"):
                    result = self.add_subject(subject_name)
                    utils.speak(result)
                else:
                    utils.speak("Subject addition cancelled.")
            
            elif 'remove' in command:
                subject_name = command.replace('remove', '').strip()
                if utils._approve(f"Remove the subject: {subject_name}?"):
                    result = self.remove_subject(subject_name)
                    utils.speak(result)
                else:
                    utils.speak("Subject removal cancelled.")
            
            else:
                utils.speak("Sorry, I didn't recognize that command. Please try again.")
            utils.speak("What would you like to do next?")

# Instantiate and test
# subject_manager = SubjectManager()
# subject_manager.process_voice_commands()


