import streamlit as st
import requests
import json
import sounddevice as sd
import soundfile as sf
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

# Define the API endpoint
url = 'http://54.226.8.225:8000/api/voicebot/'

# Function to send an audio file
def send_audio_file(filepath: str):
    with open(filepath, 'rb') as f:
        files = {'audio': (filepath, f, 'audio/mp3')}
        response = requests.post(url, files=files)
    return response

def record_audio(duration, fs, filename):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    
    # Normalize the audio data
    recording = np.int16(recording * 32767)
    
    # Save as WAV file
    wavfile.write(filename, fs, recording)
    print(f"Audio saved as {filename}")

    # Convert WAV to MP3
    audio = AudioSegment.from_wav(filename)
    mp3_filename = filename.replace('.wav', '.mp3')
    audio.export(mp3_filename, format='mp3')
    print(f"Audio converted to {mp3_filename}")

    # Print some debug information
    print(f"Recording shape: {recording.shape}")
    print(f"Recording dtype: {recording.dtype}")
    print(f"Max value: {np.max(np.abs(recording))}")

    return mp3_filename

# Streamlit app
st.title("Voicebot API Interaction")

# Audio recording parameters
duration = st.slider("Select recording duration (seconds)", 1, 10, 5)
fs = 44100  # Sample rate
filename = "./data/downloaded_audio.wav"

if st.button("Start Recording"):
    mp3_filename = record_audio(duration, fs, filename)
    st.success(f"Recording saved as {mp3_filename}")
    
    # Playback the recorded audio
    audio_bytes = open(mp3_filename, 'rb').read()
    st.audio(audio_bytes, format='audio/mp3')

if st.button("Send Audio to API"):
    response = send_audio_file(mp3_filename)
    st.write(f"Response status code: {response.status_code}")

    if response.status_code == 200:
        try:
            json_data = json.loads(response.text)
            st.write(f"Response text: {json_data['return_text']}")
            
            # Display the audio file URL
            if 'audio_url' in json_data:
                st.write(f"Audio file URL: {json_data['audio_url']}")
                st.audio(json_data['audio_url'])
            else:
                st.write("No audio file URL returned from the API")
        except json.JSONDecodeError:
            st.write("Failed to parse JSON from response")
        except KeyError as e:
            st.write(f"Key '{e}' not found in the JSON response")
    else:
        st.write(f"Server returned an error with status code: {response.status_code}")