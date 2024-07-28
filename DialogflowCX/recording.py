import pyaudio
import wave
import numpy as np
import time
from collections import deque
from io import BytesIO

# Constants
SAMPLE_RATE = 24000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms
FORMAT = pyaudio.paInt16
CHANNELS = 1
ENERGY_THRESHOLD = 35  # Energy threshold to consider starting recording
STOP_THRESHOLD = 43  # Stop recording if energy exceeds this threshold
SMOOTHING_FACTOR = 0.4  # Smoothing factor

CONTINUOUS_BELOW_THRESHOLD = (
    1.5  # Continuous time below threshold to start recording (seconds)
)


def record_audio():
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    frames = []

    smooth_energy = 0
    energy_deque = deque(maxlen=10)  # Window to store energy values

    # Function to calculate RMS energy of audio data
    def rms_energy(audio_data):
        try:
            rms = np.sqrt(np.mean(np.square(audio_data), axis=None))
        except:
            rms = 0
        return rms

    print("Listening...")

    try:
        below_threshold_start_time = time.time()  # Start time below threshold
        recording = False

        while True:
            data = stream.read(CHUNK_SIZE)
            audio_data = np.frombuffer(data, dtype=np.int16)
            energy = rms_energy(audio_data)

            # Smooth energy value
            if energy != np.nan:
                energy_deque.append(energy)
            if smooth_energy != np.nan:
                smooth_energy = energy
            smooth_energy = SMOOTHING_FACTOR * smooth_energy + (
                1 - SMOOTHING_FACTOR
            ) * np.mean(energy_deque)

            # Print current and smoothed energy values
            print(
                f"Current energy: {energy:.2f}, Smoothed energy: {smooth_energy:.2f}",
                time.time() - below_threshold_start_time,
                recording,
            )

            # Check condition to start recording
            if smooth_energy < ENERGY_THRESHOLD:
                print("true")
                if below_threshold_start_time is None:
                    below_threshold_start_time = (
                        time.time()
                    )  # Record the time below threshold
                elif (
                    time.time() - below_threshold_start_time
                    >= CONTINUOUS_BELOW_THRESHOLD
                ):
                    if not recording:
                        print("Starting recording...")
                        recording = True
                        frames = []  # Reset recording frames

            # Check condition to stop recording
            if recording and smooth_energy > STOP_THRESHOLD:
                print("Stopping recording...")
                break

            if recording:
                frames.append(data)

    except Exception as e:
        print(e)
    finally:
        # Stop and close stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Return audio data as bytes
        output = BytesIO()
        with wave.open(output, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(b"".join(frames))
        output.seek(0)  # Reset pointer to the beginning of the file
        with open("output.wav", "wb") as f:
            f.write(output.getvalue())
        return output.getvalue()
