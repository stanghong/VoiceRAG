# %%
import streamlit as st
import requests
import json
import os

# AWS IP with URL
url = 'http://54.226.8.225:8000/api/voicebot/'

# Function to send a text query
def send_text_query(query: str):
    data = {
        'text': query  # Text is sent as form data
    }
    response = requests.post(url, data=data)
    return response

# Function to send an audio file
def send_audio_file(filepath: str):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        files = {'audio': (filepath, f, 'audio/wav')}  # 'audio' matches the UploadFile parameter in FastAPI
        response = requests.post(url, files=files)
    return response

def main():
    st.title("Voice Bot Interface")

    if st.button("Start"):
        audio_file_path = "./data/downloaded_audio.wav"
        response = send_audio_file(audio_file_path)

        if response is None:
            st.write("Error: Audio file not found.")
        elif response.status_code == 200:
            try:
                json_data = json.loads(response.text)
                st.write(json_data['return_text'])
                
                if 'output_wav_url' in json_data:
                    st.audio(json_data['output_wav_url'], format='audio/wav')
            except json.JSONDecodeError:
                st.write("Failed to parse JSON from response")
            except KeyError:
                st.write("Required keys not found in the JSON response")
        else:
            st.write(f"Server returned an error with status code: {response.status_code}")

if __name__ == "__main__":
    main()

# %%
