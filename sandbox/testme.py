# %%
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# Set the sample rate and duration
fs = 44100  # Sample rate in Hz
duration = 5  # Duration of recording in seconds

print("Recording...")

# Record audio
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished

print("Recording complete.")

# Normalize and convert the recording to 16-bit data
myrecording_int16 = np.int16(myrecording / np.max(np.abs(myrecording)) * 32767)

# Save the recording as a WAV file
write('output.wav', fs, myrecording_int16)

print("Playing back the recording...")
# %%
# Play back the recorded audio
sd.play(myrecording, fs)
sd.wait()  # Wait until playback is finished

print("Playback complete.")
