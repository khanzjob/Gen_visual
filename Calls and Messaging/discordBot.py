import discord
from discord.ext import commands
import threading
import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from plyer import notification

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
TOKEN = os.getenv("discordToken")

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Store the last message received for replying
last_message = None

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
@bot.event
async def on_message(message):
    global last_message

    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    author_id = message.author.id
    author_name = message.author.name

    # Check if the message is a regular message
    if message.type == discord.MessageType.default:
        message_content = message.content
        
        # Check if the message has embeds or attachments
        if not message_content and message.embeds:
            message_content = "Embed content detected."
        elif not message_content and message.attachments:
            message_content = "Attachment detected."
        
        if isinstance(message.channel, discord.DMChannel):
            print(f"\nReceived DM from {author_name} (ID: {author_id}): {message_content}")
            send_notification(f"DM from {author_name}", message_content)
        elif isinstance(message.channel, discord.TextChannel):
            print(f"\nReceived message in channel {message.channel.name} from {author_name} (ID: {author_id}): {message_content}")
            send_notification(f"Message in {message.channel.name} from {author_name}", message_content)

        last_message = message

    await bot.process_commands(message)


def input_thread(loop):
    global last_message
    while True:
        reply = input("\nEnter your reply (or '!exit' to stop the bot): ")
        
        if reply == "!exit":
            loop.stop()
            return

        if last_message:
            asyncio.run_coroutine_threadsafe(last_message.channel.send(reply), loop)

# Run the bot on a separate thread so we can use input()
loop = asyncio.get_event_loop()
t = threading.Thread(target=loop.run_until_complete, args=(bot.start(TOKEN),))
t.start()

input_thread(loop)
