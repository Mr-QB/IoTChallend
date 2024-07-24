#!/usr/bin/env python

import os
import uuid
import numpy as np
import pyaudio
import queue
from google.cloud import dialogflow_v2 as dialogflow

# Audio recording parameters
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms


class ResumableMicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk_size):
        self._rate = rate
        self.chunk_size = chunk_size
        self._num_channels = 1
        self._buff = queue.Queue()
        self.is_final = False
        self.closed = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._fill_buffer,
        )

    def __enter__(self):
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, *args, **kwargs):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed and not self.is_final:
            data = []
            chunk = self._buff.get()
            if chunk is None:
                return
            data.append(chunk)
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b"".join(data)


def detect_intent_stream(project_id, session_id, language_code):
    """Detects intent with streaming audio as input."""

    session_client = dialogflow.SessionsClient()
    session_path = session_client.session_path(project_id, session_id)

    audio_encoding = dialogflow.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    audio_config = dialogflow.InputAudioConfig(
        audio_encoding=audio_encoding,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
    )

    def request_generator():
        query_input = dialogflow.QueryInput(audio_config=audio_config)
        yield dialogflow.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input
        )

        with ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE) as stream:
            for chunk in stream.generator():
                yield dialogflow.StreamingDetectIntentRequest(input_audio=chunk)
                if stream.is_final:
                    break

    requests = request_generator()
    responses = session_client.streaming_detect_intent(requests=requests)

    for response in responses:
        print(f'Intermediate transcript: "{response.recognition_result.transcript}".')
        if response.recognition_result.is_final:
            query_result = response.query_result
            print(f"Query text: {query_result.query_text}")
            print(
                f"Detected intent: {query_result.intent.display_name} (confidence: {query_result.intent_detection_confidence})"
            )
            print(f"Fulfillment text: {query_result.fulfillment_text}\n")
            break


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key/gcp_key.json"

    project_id = "citric-goal-343716"
    location_id = "asia-northeast1"
    agent_id = "8e648ef8-f318-4925-b99c-6242e5f802e7"
    session_id = str(uuid.uuid4())
    language_code = "vi-vn"

    detect_intent_stream(project_id, session_id, language_code)
