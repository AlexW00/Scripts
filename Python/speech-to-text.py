import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import requests
import tempfile
import os
import threading
import whisper
from pynput import keyboard

# Set the sample rate and channels for the recording
samplerate = 44100  # CD quality
channels = 2  # stereo

# Create a flag for stopping the recording
stop_recording = threading.Event()

# Define a function to be called when a key is pressed
def on_press(key):
    if key == keyboard.Key.enter:
        stop_recording.set()

# Start a keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start the recording
stream = sd.InputStream(samplerate=samplerate, channels=channels)
stream.start()

# Record audio until the user presses Enter
print("Recording started. Press Enter to stop.")
recording = []
while not stop_recording.is_set():
    data = stream.read(samplerate)
    recording.extend(data[0])

# Stop the stream and close it
stream.stop()
stream.close()

# Save the recording to a temporary WAV file
wav_file = tempfile.mktemp('.wav')
write(wav_file, samplerate, np.array(recording))

# Convert the WAV file to MP3
mp3_file = tempfile.mktemp('.mp3')
AudioSegment.from_wav(wav_file).export(mp3_file, format="mp3")

# Send the MP3 file to the OpenAI Whisper API
model = whisper.load_model("base")
result = model.transcribe(mp3_file)
print(result)
print("said: " + result["text"])

# Clean up the temporary files
os.remove(wav_file)
os.remove(mp3_file)
