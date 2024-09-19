from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS

# Set OpenAI API key
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

# Define root route
@app.route('/', methods=['GET'])
def home():
    return "Flask server is running."

# Define /transcribe route
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Define the sample rate (samples per second) and duration of the recording
    sample_rate = 44100  # Standard sample rate for audio
    duration = 10  # Duration in seconds

    # Prompt the user to start recording
    print("Recording audio from the microphone for {} seconds...".format(duration))

    # Capture audio data from the microphone
    recorded_audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
    sd.wait()  # Wait until the recording is finished

    # Save the recorded audio to a file
    audio_filename = 'output_microphone_audio1.wav'
    write(audio_filename, sample_rate, np.array(recorded_audio))

    print("Recording complete. Audio saved to '{}'.".format(audio_filename))


    try:
        client = OpenAI()
        with open(audio_filename, 'rb') as af:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=af,
                response_format="text"
            )
        print(f'user question is {transcription}')

        # Now call ChatGPT with the transcription
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use a valid model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": transcription}
            ]
        )

        gpt_answer = response.choices[0].message.content

        if os.path.exists(audio_filename):
            os.remove(audio_filename)
            print(f"File '{audio_filename}' has been deleted successfully.")
        else:
            print(f"File '{audio_filename}' does not exist.")

        # Return both the user's question and GPT's answer
        return jsonify({
            'transcription': f"User question: {transcription}",
            'gpt_answer': f"GPT Ans: {gpt_answer}"
        })

    except Exception as e:
        app.logger.error(f"Error during transcription or GPT request: {e}")
        return jsonify({'error': 'Failed to process request', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)