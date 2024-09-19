from openai import OpenAI
import os

OpenAI.api_key = os.getenv('OPENAI_API_KEY')

# with open('uploaded_audio.wav', 'rb') as af:
#     transcription = openai.Audio.transcribe(
#         model="whisper-1",
#         file=af,
#         response_format="text"
#     )

# print(f"Transcription: {transcription}")
client = OpenAI()
with open('uploaded_audio.wav', 'rb') as af:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=af,
        response_format="text"
    )
print(f"Transcription: {transcription}")