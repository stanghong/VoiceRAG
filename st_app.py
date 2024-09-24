import gradio as gr
import soundfile as sf
import tempfile
import requests
import json
import threading
import numpy as np

# Define the API endpoint
API_URL = 'http://54.226.8.225:8000/api/voicebot/'

def send_audio(filepath):
    """
    Sends the audio file to the API and returns the response.
    """
    try:
        with open(filepath, 'rb') as f:
            files = {'audio': (filepath, f, 'audio/wav')}
            response = requests.post(API_URL, files=files)
        return response
    except Exception as e:
        return {"error": f"Error sending audio: {e}"}

def process_and_send(audio, duration, samplerate):
    """
    Processes the recorded audio and sends it to the API.
    Returns the API response or an error message.
    """
    if audio is None:
        return "No audio recorded."

    try:
        # Save the uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_filepath = tmp_file.name
            sf.write(tmp_filepath, audio[0], samplerate, subtype='PCM_16')

        # Send audio to API
        response = send_audio(tmp_filepath)

        if isinstance(response, dict) and "error" in response:
            return response["error"]

        if response is not None:
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    return json_data.get('return_text', 'No return_text found in response.')
                except json.JSONDecodeError:
                    return "Failed to parse JSON from response."
                except KeyError:
                    return "Key 'return_text' not found in the JSON response."
            else:
                return f"Server returned an error with status code: {response.status_code}"
        else:
            return "No response from server."

    except Exception as e:
        return f"An error occurred: {e}"

def main():
    """
    Sets up the Gradio interface.
    """
    with gr.Blocks() as demo:
        gr.Markdown("# VoiceBot Gradio App")
        gr.Markdown("""
            Record your voice, and the app will send the audio to the API.
            The response from the API will be displayed below.
        """)

        with gr.Row():
            duration = gr.Slider(
                minimum=1, 
                maximum=60, 
                step=1, 
                value=5, 
                label="Recording Duration (seconds)"
            )
            samplerate = gr.Slider(
                minimum=8000, 
                maximum=48000, 
                step=1000, 
                value=16000, 
                label="Sample Rate (Hz)"
            )

        audio_input = gr.Audio(
            type="numpy",
            label="Record Your Voice"
        )

        send_button = gr.Button("Start Recording and Send")

        api_response = gr.Textbox(
            label="API Response",
            interactive=False
        )

        audio_playback = gr.Audio(
            label="Playback Recorded Audio",
            interactive=False
        )

        def on_send(audio, duration, samplerate):
            """
            Handles the recording and sending process.
            """
            return process_and_send(audio, duration, samplerate)

        send_button.click(
            fn=on_send, 
            inputs=[audio_input, duration, samplerate], 
            outputs=[api_response, audio_playback],
            api_name="process_audio"
        )

    demo.launch()

if __name__ == "__main__":
    main()