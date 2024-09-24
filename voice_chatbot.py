# %%
# Import necessary libraries
import sounddevice as sd
import numpy as np
import wave
import random
import os
from pydub import AudioSegment

# Define the sample rate (samples per second) and duration of the recording
sample_rate = 44100  # Standard sample rate for audio
duration = 10  # Duration in seconds
output_file = f"output_audio_recording_{random.randint(1000, 9999)}.wav"  # Output file name with random number

# Record audio
print("Recording...")
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')  # Use 1 channel for mono recording
sd.wait()  # Wait for the recording to finish
print("Recording finished")

# Convert the NumPy array to bytes
audio_bytes = audio.tobytes()

# Save the recorded audio to a .wav file
with wave.open(output_file, 'wb') as wf:
    wf.setnchannels(1)  # Mono recording
    wf.setsampwidth(2)  # Sample width in bytes (16-bit audio)
    wf.setframerate(sample_rate)
    wf.writeframes(audio_bytes)

print(f"Recording complete. Audio saved to '{output_file}'.")

# Transcribe the audio using OpenAI's API
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI()

audio_file = open(output_file, "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file, 
  response_format="text"
)

print(transcription)

# # Delete the audio file
# if os.path.exists(output_file):
#     os.remove(output_file)
#     print(f"Deleted audio file: {output_file}")
# else:
#     print(f"Audio file {output_file} not found.")

# %%

import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI()
# %%
audio_file = open(output_file, "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file, 
  response_format="text"
)

print(transcription)



# %%
import requests
import json

# Define the API endpoint
#local
# url = 'http://127.0.0.1:8000/api/voicebot/'
# docker
# url = 'http://0.0.0.0:8000/api/voicebot/'
# aws
url = 'http://184.73.60.223:8000/api/voicebot/'
# Function to send a text query
def send_text_query(query: str):
    data = {
        'text': query  # Text is sent as form data
    }
    response = requests.post(url, data=data)
    return response

# Function to send an audio file
def send_audio_file(filepath: str):
    with open(filepath, 'rb') as f:
        files = {'audio': (filepath, f, 'audio/wav')}  # 'audio' matches the UploadFile parameter in FastAPI
        response = requests.post(url, files=files)
    return response

audio_file_path = "output_audio_recording.wav"
response = send_audio_file(audio_file_path)
print(f"Response status code: {response.status_code}")
print(f"Raw response content: {response.content.decode()}")

if response.status_code == 200:
    try:
        json_data = json.loads(response.text)
        print(f"Response text: {json_data['return_text']}")
    except json.JSONDecodeError:
        print("Failed to parse JSON from response")
    except KeyError:
        print("Key 'return_text' not found in the JSON response")
else:
    print(f"Server returned an error with status code: {response.status_code}")

# %%
# Delete the audio file
# if os.path.exists(output_file):
#     os.remove(output_file)
#     print(f"Deleted audio file: {output_file}")
# else:
#     print(f"Audio file {output_file} not found.")
# %%
import streamlit as st
import tempfile
import os

def main():
    st.set_page_config(page_title="VoiceChat", page_icon="🎙️")
    st.title("VoiceChat")

    if 'recording' not in st.session_state:
        st.session_state.recording = False
    if 'audio_data' not in st.session_state:
        st.session_state.audio_data = None

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.button("🎙️ Record / Stop"):
        st.session_state.recording = not st.session_state.recording
        if st.session_state.recording:
            st.write("Recording... Click again to stop.")
            st.session_state.audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
            sd.wait()
            st.session_state.audio_data = np.int16(st.session_state.audio_data * 32767)
        else:
            st.write("Recording stopped.")
            if st.session_state.audio_data is not None:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                    with wave.open(temp_file.name, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(sample_rate)
                        wf.writeframes(st.session_state.audio_data.tobytes())
                    response = send_audio_file(temp_file.name)
                os.unlink(temp_file.name)

                if response.status_code == 200:
                    try:
                        json_data = json.loads(response.text)
                        ai_response = json_data['return_text']
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        with st.chat_message("assistant"):
                            st.markdown(ai_response)
                    except (json.JSONDecodeError, KeyError):
                        st.error("Failed to process the response from the server.")
                else:
                    st.error(f"Server returned an error with status code: {response.status_code}")

if __name__ == "__main__":
    main()

# %%
