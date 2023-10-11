import wavio
import os
import keyboard
from datetime import datetime
import sounddevice as sd
import numpy as np
# Parameters
RATE = 44100    # Sample rate
CHANNELS = 2    # Number of channels (1=mono, 2=stereo)
DTYPE = np.int16  # Data type
SAVE_FOLDER = "recorded_audios"  # Folder to save the audio files

# Create save folder if it doesn't exist
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def record_audio():
    print("Recording... Press 'q' to stop and save.")
    
    # Start recording
    audio_data = []
    with sd.InputStream(samplerate=RATE, channels=CHANNELS) as stream:
        while True:
            audio_chunk, overflowed = stream.read(RATE)
            audio_data.append(audio_chunk)
            if keyboard.is_pressed('q'):
                break

    audio_data = np.concatenate(audio_data, axis=0)
    return audio_data

def save_wav(data, filename):
    wavio.write(filename, data, RATE, sampwidth=2)

def list_files(main_folder):
    all_files = []
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def play_audio(file_path):
    # Implement your logic to play audio here
    pass

def search_and_play(query, main_folder):
    all_files = list_files(main_folder)
    matches = [file for file in all_files if query.lower() in os.path.basename(file).lower()]
    
    if not matches:
        print(f"No files found with the name: {query}")
        return
    
    print("\nFound the following matches:")
    for index, path in enumerate(matches, 1):
        print(f"{index}. {path}")

    choice = int(input("\nEnter the file number to play or 0 to exit: "))
    if 0 < choice <= len(matches):
        play_audio(matches[choice-1])

        
def capture_recordings(main_folder, subfolder):
    audio_data = record_audio()
    
    # Ensure the main folder exists
    if not os.path.exists(main_folder):
        os.mkdir(main_folder)
    
    # Ensure the subfolder exists within the main folder
    subfolder_path = os.path.join(main_folder, subfolder)
    if not os.path.exists(subfolder_path):
        os.mkdir(subfolder_path)
    
    # Ensure date-based subfolder exists within the subfolder
    current_date = datetime.now().strftime('%Y-%m-%d')
    date_subfolder_path = os.path.join(subfolder_path, current_date)
    if not os.path.exists(date_subfolder_path):
        os.mkdir(date_subfolder_path)
    
    # Generate the file name based on the current time
    current_time = datetime.now().strftime('%H-%M-%S')
    file_name = os.path.join(date_subfolder_path, f"audio_recording_{current_time}.wav")
    
    save_wav(audio_data, file_name)
    print(f"Audio saved to {file_name}")
    all_files = list_files(main_folder)
    print("\nSummary of files:")
    for index, path in enumerate(all_files, 1):
        print(f"{index}. {path}")
   

# capture_recordings("sciencce","recording")
search_and_play("audio_recording_22-51-00.wav","recording")