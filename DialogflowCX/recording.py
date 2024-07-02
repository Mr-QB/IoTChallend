import pyaudio
import wave
import numpy as np
import time
from pynput import keyboard

chunk = 1024
format = pyaudio.paInt16
channels = 2
rate = 44100
Output_Filename = "Recorded.wav"

p = pyaudio.PyAudio()

stream = p.open(
    format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk
)

frames = []
recording = False


def on_press(key):
    global recording
    try:
        if key == keyboard.Key.space:
            if not recording:                                          
                print("Recording... Press SPACE to stop.")
                recording = True
            else:
                print("Stopping recording...")
                recording = False  
                return False
    except AttributeError:
        pass


listener = keyboard.Listener(on_press=on_press)
listener.start()  

print("Press SPACE to start recording")

# Chờ cho đến khi bắt đầu ghi âm
while not recording:
    time.sleep(0.1)
    
while recording:
    try:
        data = stream.read(chunk)
        frames.append(data)
    except Exception as e:
        print(f"Error: {e}")
        break

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(Output_Filename, "wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(format))
wf.setframerate(rate)
wf.writeframes(b"".join(frames))
wf.close()
