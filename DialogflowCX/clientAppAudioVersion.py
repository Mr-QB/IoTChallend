#!/usr/bin/env python

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""DialogFlow API Detect Intent Python sample with audio files processed as an audio stream.

Examples:
  python detect_intent_stream.py -h
  python detect_intent_stream.py --agent AGENT \
  --session-id SESSION_ID --audio-file-path resources/hello.wav
"""

import argparse
import uuid
import os

from google.cloud.dialogflowcx_v3beta1.services.agents import AgentsClient
from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import audio_config
from google.cloud.dialogflowcx_v3beta1.types import session

import pyaudio
import wave
from pynput import keyboard
import numpy as np
import time 

p = pyaudio.PyAudio()

channels = 1
chunk = 1024
rate = 24000
format = pyaudio.paInt16

stream = p.open(
    format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk
)

frames = []
recording = False

def rms_energy(audio_data):
    # Calculate the RMS energy of the audio data.
    rms = np.sqrt(np.mean(np.square(audio_data), axis=None))
    return rms

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


# [START dialogflow_detect_intent_stream]
def run_sample():
    # TODO(developer): Replace these values when running the function
    project_id = "YOUR-PROJECT-ID"
    # For more information about regionalization see https://cloud.google.com/dialogflow/cx/docs/how/region
    location_id = "YOUR-LOCATION-ID"
    # For more info on agents see https://cloud.google.com/dialogflow/cx/docs/concept/agent
    agent_id = "YOUR-AGENT-ID"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
    # For more information on sessions see https://cloud.google.com/dialogflow/cx/docs/concept/session
    session_id = uuid.uuid4()
    audio_file_path = "YOUR-AUDIO-FILE-PATH"
    # For more supported languages see https://cloud.google.com/dialogflow/es/docs/reference/language
    language_code = "en-us"

    detect_intent_stream(agent, session_id, audio_file_path, language_code)


def detect_intent_stream(agent, session_id, audio_file_path, language_code):
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

        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.


        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        print("Press SPACE to start recording")
        while not recording:
            time.sleep(0.1)

        while recording:
            try:
                data = stream.read(chunk)
                audio_input = session.AudioInput(audio=data)
                query_input = session.QueryInput(audio=audio_input)
                yield session.StreamingDetectIntentRequest(query_input=query_input)

                # detect human sounds
                threshold_energy = 1000
                audio_data = np.frombuffer(data, dtype=np.int16) 
                energy = rms_energy(audio_data)
                if energy < threshold_energy:
                    print("Stopping recording...")
                    recording = False
                    break
            except Exception as e:
                print(f"Error: {e}")
                break
        

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


# [END dialogflow_detect_intent_stream]

if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "DialogflowCX/key/gcp_key.json"

    project_id = "citric-goal-343716"
    location_id = "asia-northeast1"
    agent_id = "8e648ef8-f318-4925-b99c-6242e5f802e7"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
    session_id = uuid.uuid4()
    texts = ["xin chào"]
    language_code = "vi-vn"
    audio_file_path = "DialogflowCX/audio.wav"

    detect_intent_stream(
        agent, session_id, audio_file_path, language_code
    )