import pyaudio
import wave
import numpy as np
import time
from collections import deque
from io import BytesIO

# Các hằng số
SAMPLE_RATE = 24000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms
FORMAT = pyaudio.paInt16
CHANNELS = 1
ENERGY_THRESHOLD = 35  # Ngưỡng năng lượng để xem xét bắt đầu ghi âm
STOP_THRESHOLD = 43  # Dừng ghi âm nếu năng lượng cao hơn ngưỡng này
SMOOTHING_FACTOR = 0.4  # Hệ số làm mượt

CONTINUOUS_BELOW_THRESHOLD = (
    1.5  # Thời gian liên tục dưới ngưỡng để bắt đầu ghi âm (giây)
)


def record_audio():
    p = pyaudio.PyAudio()

    # Mở luồng
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    frames = []

    smooth_energy = 0
    energy_deque = deque(maxlen=10)  # Cửa sổ lưu trữ các giá trị năng lượng

    # Hàm tính năng lượng RMS của dữ liệu âm thanh
    def rms_energy(audio_data):
        try:
            rms = np.sqrt(np.mean(np.square(audio_data), axis=None))
        except:
            rms = 0
        return rms

    print("Đang lắng nghe...")

    try:
        below_threshold_start_time = time.time()  # Thời điểm bắt đầu dưới ngưỡng
        recording = False

        while True:
            data = stream.read(CHUNK_SIZE)
            audio_data = np.frombuffer(data, dtype=np.int16)
            energy = rms_energy(audio_data)

            # Làm mượt giá trị năng lượng
            if energy != np.nan:
                energy_deque.append(energy)
            if smooth_energy != np.nan:
                smooth_energy = energy
            smooth_energy = SMOOTHING_FACTOR * smooth_energy + (
                1 - SMOOTHING_FACTOR
            ) * np.mean(energy_deque)

            # In ra năng lượng hiện tại và năng lượng đã làm mượt
            print(
                f"Năng lượng hiện tại: {energy:.2f}, Năng lượng đã làm mượt: {smooth_energy:.2f}",
                time.time() - below_threshold_start_time,
                recording,
            )

            # Kiểm tra điều kiện để bắt đầu ghi âm
            if smooth_energy < ENERGY_THRESHOLD:
                print("true")
                if below_threshold_start_time is None:
                    below_threshold_start_time = (
                        time.time()
                    )  # Ghi lại thời điểm dưới ngưỡng
                elif (
                    time.time() - below_threshold_start_time
                    >= CONTINUOUS_BELOW_THRESHOLD
                ):
                    if not recording:
                        print("Bắt đầu ghi âm...")
                        recording = True
                        frames = []  # Đặt lại các frame ghi âm
            # else:
            #     below_threshold_start_time = time.time()

            # Kiểm tra điều kiện để dừng ghi âm
            if recording and smooth_energy > STOP_THRESHOLD:
                print("Dừng ghi âm...")
                break

            if recording:
                frames.append(data)

    except Exception as e:
        print(e)
    finally:
        # Dừng và đóng luồng
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Trả về dữ liệu âm thanh dưới dạng byte
        output = BytesIO()
        with wave.open(output, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(b"".join(frames))
        output.seek(0)  # Đặt lại con trỏ về đầu file
        with open("output.wav", "wb") as f:
            f.write(output.getvalue())
        return output.getvalue()
