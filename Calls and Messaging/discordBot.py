
# import speech_recognition as sr
# import discord
# from discord.ext import commands
# import threading
# import asyncio
# import os
# from dotenv import find_dotenv, load_dotenv
# from plyer import notification
# from collections import deque
# import json

# # Initial setup
# dotenv_path = find_dotenv()
# load_dotenv(dotenv_path)
# TOKEN = os.getenv("discordToken")

# intents = discord.Intents.default()
# intents.messages = True
# intents.reactions = True
# intents.guilds = True
# intents.members = True
# intents.message_content = True
# bot = commands.Bot(command_prefix='!', intents=intents)

# last_message = None
# N = 10
# message_history = deque(maxlen=N)

# def get_user_input():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#         r.energy_threshold = 200
#         r.pause_threshold = 0.5
#         audio = r.listen(source, timeout=30, phrase_time_limit=30)  # Updated to 90 seconds
#         user_input = r.recognize_google(audio)
#     return user_input

# def load_message_history(filename):
#     if os.path.exists(filename):
#         with open(filename, 'r') as file:
#             return json.load(file)
#     else:
#         return []


# def save_message_history(filename, history):
#     with open(filename, 'w') as file:
#         json.dump(list(history), file)


# def send_notification(title, message):
#     notification.notify(
#         title=title,
#         message=message,
#         timeout=10
#     )


# @bot.event
# async def on_ready():
#     print(f'We have logged in as {bot.user}')


# @bot.event
# async def on_message(message):
#     global last_message

#     if message.author == bot.user:
#         return

#     author_id = message.author.id
#     author_name = message.author.name

#     if message.type == discord.MessageType.default:
#         message_content = message.content

#         if not message_content and message.embeds:
#             message_content = "Embed content detected."
#         elif not message_content and message.attachments:
#             message_content = "Attachment detected."

#         display_message = f"\nReceived message in channel {message.channel.name} from {author_name} (ID: {author_id}): {message_content}"
        
#         if isinstance(message.channel, discord.DMChannel):
#             display_message = f"\nReceived DM from {author_name} (ID: {author_id}): {message_content}"
        
#         print(display_message)
#         send_notification(f"Message from {author_name}", message_content)

#         last_message = message
#         message_data = {
#             "author_id": author_id,
#             "author_name": author_name,
#             "content": message_content,
#             "channel": message.channel.name if isinstance(message.channel, discord.TextChannel) else "DM"
#         }
#         message_history.append(message_data)
#         save_message_history('message_history.json', message_history)

#     await bot.process_commands(message)


# def input_thread(loop):
#     global last_message
#     while True:
#         reply = input("\nEnter your reply (or '!exit' to stop the bot): ")
        
#         if reply == "!exit":
#             loop.stop()
#             return

#         if last_message:
#             asyncio.run_coroutine_threadsafe(last_message.channel.send(reply), loop)


# def SendMessage():
#     # Load messages from history file
#     loaded_messages = load_message_history('message_history.json')
#     message_history.extend(loaded_messages)

#     # Start bot on a separate thread
#     loop = asyncio.get_event_loop()
#     t = threading.Thread(target=loop.run_until_complete, args=(bot.start(TOKEN),))
#     t.start()

#     # Start input thread for user to send replies
#     input_thread(loop)


# if __name__ == "__main__":
#     SendMessage()


import discord
from discord.ext import commands
import threading
import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from plyer import notification
from collections import deque
import json
import pygame
import requests
from datetime import datetime
import speech_recognition as sr

# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
TOKEN = os.getenv("discordToken")

Vid = os.getenv("voice_id")
elevenLabsAPI = os.getenv("elevenLabsAPI")

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

last_message = None
N = 10
message_history = deque(maxlen=N)
async def graceful_shutdown(bot, loop):
    await bot.logout()
    await bot.close()
    loop.stop()
def load_message_history(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        with open(filename, 'w') as file:
            json.dump([], file)
        return []


def save_message_history(filename, history):
    with open(filename, 'w') as file:
        json.dump(list(history), file)


def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def speak(text):
    # if current_language.lower == "english":
        voice_id = Vid
        api_key = elevenLabsAPI
        CHUNK_SIZE = 1024
        
        # filename = now.strftime("%Y-%m-%d_%H-%M-%S")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_file = f'{timestamp}.mp3'
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return
        except Exception as err:
            print(f"An error occurred: {err}")
            return

        try:

            directory = datetime.now().strftime('%Y-%m-%d')
            os.makedirs(directory, exist_ok=True)

            file_path = os.path.join(directory, output_file)

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

            # Play the audio file with pygame
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue

            pygame.mixer.quit()  # Release the audio file after playing

            # Delete the audio file after it's been played
            try:
                os.remove(file_path)
            except Exception as err:
                print(f"An error occurred while deleting the file: {err}")

        except Exception as err:
            print(f"An error occurred: {err}")
   
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
def get_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = 200
        r.pause_threshold = 0.5
        audio = r.listen(source, timeout=30, phrase_time_limit=30)
        user_input = r.recognize_google(audio)
    return user_input

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    global last_message

    if message.author == bot.user:
        return

    author_id = message.author.id
    author_name = message.author.name

    if message.type == discord.MessageType.default:
        message_content = message.content

        if not message_content and message.embeds:
            message_content = "Embed content detected."
        elif not message_content and message.attachments:
            message_content = "Attachment detected."

        display_message = f"\nReceived message  from {author_name} . Message is .  : {message_content}"
        
        if isinstance(message.channel, discord.DMChannel):
            display_message = f"\nReceived DM from {author_name} (ID: {author_id}): {message_content}"
        
        speak(display_message)
        send_notification(f"Message from {author_name}", message_content)

        last_message = message
        message_data = {
            "author_id": author_id,
            "author_name": author_name,
            "content": message_content,
            "channel": message.channel.name if isinstance(message.channel, discord.TextChannel) else "DM"
        }
        message_history.append(message_data)
        save_message_history('message_history.json', message_history)

    await bot.process_commands(message)


def voice_input_thread(loop, bot):
    global last_message
    while True:
        speak("\n Speak to Send message")
        reply = get_user_input()
        
        if not _approve(reply):
            speak("input withdrawn..")
            continue

        if reply.lower() == "exit":
            loop.create_task(graceful_shutdown(bot, loop))
            return

        if last_message:
            asyncio.run_coroutine_threadsafe(last_message.channel.send(reply), loop)




def main():
    # Load messages from history file
    loaded_messages = load_message_history('message_history.json')
    message_history.extend(loaded_messages)

    # Set up asyncio event loop
    loop = asyncio.get_event_loop()

    # Start voice input thread for user to send replies using voice commands
    t = threading.Thread(target=voice_input_thread, args=(loop, bot))
    t.start()

    # Start bot on the main thread
    loop.run_until_complete(bot.start(TOKEN))

if __name__ == "__main__":
    main()
