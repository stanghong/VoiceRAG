# %%
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# Set the sample rate and duration
fs = 44100  # Sample rate in Hz
duration = 5  # Duration of recording in seconds
# List available input devices
print(sd.query_devices())
sd.default.reset()
print("Recording...") 

# %%
# need to check the devices from print list make sure the name matches 
sd.default.device = (1, 2) 
# %%
# Record audio
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished

print("Recording complete.")
# %%
# Normalize and convert the recording to 16-bit data
myrecording_int16 = np.int16(myrecording / np.max(np.abs(myrecording)) * 32767)

# Save the recording as a WAV file
write('output_microphone_audio.wav', fs, myrecording_int16)
# %%
print("Playing back the recording...")

# Play back the recorded audio
sd.play(myrecording, fs)
sd.wait()  # Wait until playback is finished

print("Playback complete.")

# %%

# %%

import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI()
# %%
audio_file = open("output_microphone_audio.wav", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file, 
  response_format="text"
)

print(transcription)

# %%
import sys
from rag_chromadb_qa import load_documents, chunk_documents, chromadb_retrieval_qa
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
# %%
file_name ='./data/Self-correcting LLM-controlled Diffusion Models.pdf'
question = transcription

# Load the documents
data = load_documents(file_name)

# Chunk the documents
texts = chunk_documents(data)

# Perform the QA retrieval
result = chromadb_retrieval_qa(texts, question)
# %%
# Print the result
print(f"Answer: {result}")
# %%
# playback voice
from gtts import gTTS
import os

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("afplay output.mp3")  # Use 'afplay' to play mp3 on macOS

# Test the function
speak_text(transcription)
speak_text(result)


# %%