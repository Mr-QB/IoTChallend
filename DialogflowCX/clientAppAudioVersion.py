import argparse
import uuid
import os
import time
import sounddevice as sd
from recording import record_audio
from google.cloud.dialogflowcx_v3beta1.services.agents import AgentsClient
from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import audio_config
from google.cloud.dialogflowcx_v3beta1.types import session

import re

import unicodedata
from argparse import ArgumentParser
from pathlib import Path

import soundfile as sf


from vietTTS.vietTTS.hifigan.mel2wave import mel2wave
from vietTTS.vietTTS.nat.config import FLAGS
from vietTTS.vietTTS.nat.text2mel import text2mel


# [START dialogflow_detect_intent_stream]
def detect_intent_stream(agent, session_id, audio_data, language_code):
    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_path = f"{agent}/sessions/{session_id}"
    print(f"Session path: {session_path}\n")
    client_options = None
    agent_components = AgentsClient.parse_agent_path(agent)
    location_id = agent_components["location"]
    if location_id != "global":
        api_endpoint = f"{location_id}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)

    input_audio_config = audio_config.InputAudioConfig(
        audio_encoding=audio_config.AudioEncoding.AUDIO_ENCODING_LINEAR_16,
        sample_rate_hertz=24000,
    )

    def request_generator():
        audio_input = session.AudioInput(config=input_audio_config)
        query_input = session.QueryInput(audio=audio_input, language_code=language_code)
        voice_selection = audio_config.VoiceSelectionParams()
        synthesize_speech_config = audio_config.SynthesizeSpeechConfig()
        output_audio_config = audio_config.OutputAudioConfig()

        # Sets the voice name and gender
        voice_selection.name = "en-GB-Standard-A"
        voice_selection.ssml_gender = (
            audio_config.SsmlVoiceGender.SSML_VOICE_GENDER_FEMALE
        )

        synthesize_speech_config.voice = voice_selection

        # Sets the audio encoding
        output_audio_config.audio_encoding = (
            audio_config.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_UNSPECIFIED
        )
        output_audio_config.synthesize_speech_config = synthesize_speech_config

        # The first request contains the configuration.
        yield session.StreamingDetectIntentRequest(
            session=session_path,
            query_input=query_input,
            output_audio_config=output_audio_config,
        )

        # Here we are reading chunks of audio data from the recording
        offset = 0
        chunk_size = 4096
        while offset < len(audio_data):
            chunk = audio_data[offset : offset + chunk_size]
            offset += chunk_size
            # The later requests contain audio data.
            audio_input = session.AudioInput(audio=chunk)
            query_input = session.QueryInput(audio=audio_input)
            yield session.StreamingDetectIntentRequest(query_input=query_input)

    responses = session_client.streaming_detect_intent(requests=request_generator())

    print("=" * 20)
    for response in responses:
        print(f'Intermediate transcript: "{response.recognition_result.transcript}".')

    # Note: The result from the last response is the final transcript along
    # with the detected content.
    response = response.detect_intent_response
    print(f"Query text: {response.query_result.transcript}")
    response_messages = [
        " ".join(msg.text.text) for msg in response.query_result.response_messages
    ]
    print(f"Response text: {' '.join(response_messages)}\n")
    # tts ........
    if len(response_messages) > 0:
        mel = text2mel(
            response_messages[0],
            lexicon_fn="vietTTS/assets/infore/lexicon.txt",
            silence_duration=0.2,
        )
        # mel = text2mel(text, args.lexicon_file, args.silence_duration)
        wave = mel2wave(mel)
        # print("writing output to file", args.output)
        # sf.write("a.wav", wave, samplerate=16000)
        sd.play(wave, 16000)
        sd.wait()


# [END dialogflow_detect_intent_stream]

if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "DialogflowCX/key/gcp_key.json"

    project_id = "citric-goal-343716"
    location_id = "asia-northeast1"
    agent_id = "8e648ef8-f318-4925-b99c-6242e5f802e7"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
    language_code = "vi-vn"  # Ngôn ngữ tiếng Việt

    while True:
        session_id = uuid.uuid4()  # Tạo session_id mới cho mỗi lần ghi âm
        print("Ghi âm bắt đầu...")
        audio_data = record_audio()  # Ghi âm và nhận dữ liệu âm thanh
        print("Ghi âm hoàn tất, gửi dữ liệu đến Dialogflow...")

        detect_intent_stream(agent, session_id, audio_data, language_code)

        print("Chờ 2 giây trước khi ghi âm tiếp theo...")
        time.sleep(2)  # Chờ 5 giây trước khi bắt đầu vòng lặp ghi âm tiếp theo
