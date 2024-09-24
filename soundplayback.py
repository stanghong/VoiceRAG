# %%
# Step 2: Import libraries
import sounddevice as sd
from scipy.io.wavfile import write, read
import numpy as np
import os
from IPython.display import Audio

# %%
# Step 3: Define recording function
def record_audio(filename="output.wav", duration=5, fs=44100, channels=2):
    print(f"Recording started for {duration} seconds...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='int16')
        sd.wait()
        write(filename, fs, recording)
        print(f"Recording finished. Audio saved as '{filename}'")
    except Exception as e:
        print(f"An error occurred during recording: {e}")

# %%
# Step 4: Define playback function
def play_audio(filename="output.wav"):
    if not os.path.isfile(filename):
        print(f"The file '{filename}' does not exist.")
        return
    print(f"Playing '{filename}'...")
    try:
        fs, data = read(filename)
        sd.play(data, fs)
        sd.wait()
        print("Playback finished.")
    except Exception as e:
        print(f"An error occurred during playback: {e}")

# %%
# Step 5: Record audio
filename = "my_recording.wav"
duration = 5
fs = 44100
channels = 1

record_audio(filename=filename, duration=duration, fs=fs, channels=channels)

# %%
