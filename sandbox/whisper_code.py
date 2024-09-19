# %%
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import boto3
from io import BytesIO

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# %%
client = OpenAI()

# AWS S3 details
bucket_name = 'voice-rag'
object_key = 'output_microphone_audio1.wav'
local_filename = 'downloaded_audio.wav'

# Initialize an S3 client
s3 = boto3.client('s3')

# %%
# Dthe file frownload om S3
try:
    s3.download_file(bucket_name, object_key, local_filename)
    print(f"File downloaded successfully from {bucket_name}/{object_key}")
except Exception as e:
    print(f"Error downloading file from S3: {e}")
    exit(1)
try:
    with open(local_filename, 'rb') as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    print("Transcription:")
    print(transcription)
except Exception as e:
    print(f"Error during transcription: {e}")
finally:
    # Clean up the local file
    if os.path.exists(local_filename):
        os.remove(local_filename)
# %%
# Create an in-memory bytes buffer
# audio_buffer = BytesIO()
# # Download the file from S3 into the in-memory buffer
# try:
#     s3.download_fileobj(bucket_name, object_key, audio_buffer)
#     print(f"File '{object_key}' downloaded successfully from bucket '{bucket_name}' into memory.")
# except Exception as e:
#     print(f"Error downloading file from S3: {e}")
#     exit(1)

# # Reset the buffer position to the beginning
# audio_buffer.seek(0)

# # Proceed to process the in-memory file with OpenAI Whisper API
# try:
#     transcription = client.audio.transcriptions.create(
#         model="whisper-1",
#         file=audio_buffer,
#         response_format="text"
#     )
#     print("Transcription:")
#     print(transcription)
# except Exception as e:
#     print(f"Error during transcription: {e}")
# %%
