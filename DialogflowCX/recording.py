import pyaudio
import wave
import numpy as np
import time

def record_audio(output_filename, max_silence_duration=3, sample_rate=44100, channels=1, chunk_size=1024, silence_threshold=500):
    audio = pyaudio.PyAudio()

    # Thiết lập các tham số cho ghi âm
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    print("Recording...")

    frames = []
    silent_chunks = 0

    while True:
        data = stream.read(chunk_size)
        frames.append(data)

        # Chuyển đổi dữ liệu sang numpy array để kiểm tra mức độ âm thanh
        audio_data = np.frombuffer(data, dtype=np.int16)
        if np.max(np.abs(audio_data)) < silence_threshold:
            silent_chunks += 1
        else:
            silent_chunks = 0

        # Kiểm tra nếu không có âm thanh mới trong thời gian quy định
        if silent_chunks > (sample_rate / chunk_size * max_silence_duration):
            print("No new audio detected, stopping recording.")
            break

    print("Recording finished.")

    # Dừng ghi âm
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Lưu dữ liệu vào tệp WAV
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

# Thiết lập các tham số ghi âm
output_filename = "output.wav"
max_silence_duration = 3  # Thời gian tối đa không có âm thanh (giây)
sample_rate = 44100  # Tần số mẫu
channels = 1  # Số kênh (1 cho mono, 2 cho stereo)
chunk_size = 1024  # Kích thước mỗi khối dữ liệu
silence_threshold = 500  # Ngưỡng im lặng (giá trị này có thể cần điều chỉnh)

# Ghi âm
record_audio(output_filename, max_silence_duration, sample_rate, channels, chunk_size, silence_threshold)
