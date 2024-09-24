# %%
import requests
import json

# Define the API endpoint
#local
# url = 'http://127.0.0.1:8000/api/voicebot/'
# docker
# url = 'http://0.0.0.0:8000/api/voicebot/'
# aws
# url = 'http://184.73.60.223:8000/api/voicebot/'
#aws ip with url
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
    with open(filepath, 'rb') as f:
        files = {'audio': (filepath, f, 'audio/wav')}  # 'audio' matches the UploadFile parameter in FastAPI
        response = requests.post(url, files=files)
    return response

audio_file_path = "./data/downloaded_audio.wav"
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
