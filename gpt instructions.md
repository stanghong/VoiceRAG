To capture audio from your MacBook's microphone using Python, you can use the `sounddevice` or `PyAudio` library. Here’s a simple approach using the `sounddevice` library, which is easier to use.

### Step 1: Install the necessary Python libraries
You need to install `sounddevice` and optionally `scipy` if you want to save the recorded audio as a WAV file.

```bash
pip install sounddevice numpy scipy
```

### Step 2: Python code to capture audio from the MacBook microphone
Here is a Python script that captures audio from your microphone and saves it as a WAV file:

```python
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Define the sample rate (samples per second) and duration of the recording
sample_rate = 44100  # Standard sample rate for audio
duration = 10  # Duration in seconds

# Prompt the user to start recording
print("Recording audio from the microphone for {} seconds...".format(duration))

# Capture audio data from the microphone
recorded_audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
sd.wait()  # Wait until the recording is finished

# Save the recorded audio to a file (e.g., 'output_microphone_audio.wav')
write("output_microphone_audio.wav", sample_rate, np.array(recorded_audio))

print("Recording complete. Audio saved to 'output_microphone_audio.wav'.")
```

### Explanation:
- **`sample_rate`**: This is set to 44100 Hz, which is the standard sample rate for CD-quality audio.
- **`duration`**: The length of the recording in seconds. You can adjust this based on how long you want to record.
- **`sd.rec()`**: This function records audio from your default input device (in this case, the MacBook's microphone).
- **`sd.wait()`**: Ensures the program waits until the recording is finished.
- **`write()`**: Saves the recorded audio as a `.wav` file using `scipy.io.wavfile.write`.

### Step 3: Run the script
1. Make sure your MacBook's microphone is selected as the default input device (you can check this in **System Preferences > Sound > Input**).
2. Run the Python script, and it will record audio from your microphone for the specified duration (10 seconds in this example).
3. After the recording is complete, the audio will be saved as `output_microphone_audio.wav` in your working directory.

This code captures audio from your MacBook's microphone and writes it to a file. Let me know if you encounter any issues or need further customization!