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

"""DialogFlow API Detect Intent Python sample with text inputs.

Examples:
  python detect_intent_texts.py -h
  python detect_intent_texts.py --agent AGENT \
  --session-id SESSION_ID \
  "hello" "book a meeting room" "Mountain View"
  python detect_intent_texts.py --agent AGENT \
  --session-id SESSION_ID \
  "tomorrow" "10 AM" "2 hours" "10 people" "A" "yes"
"""

import argparse
import uuid
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "DialogflowCX/key/gcp_key.json"

from google.cloud.dialogflowcx_v3beta1.services.agents import AgentsClient
from google.cloud.dialogflowcx_v3.services.intents import IntentsClient
from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session


def detect_intent_texts(agent, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_path = f"{agent}/sessions/{session_id}"
    # print(f"Session path: {session_path}\n")
    client_options = None
    agent_components = AgentsClient.parse_agent_path(agent)
    location_id = agent_components["location"]
    if location_id != "global":
        api_endpoint = f"{location_id}-dialogflow.googleapis.com:443"
        # print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)

    for text in texts:
        text_input = session.TextInput(text=text)
        query_input = session.QueryInput(text=text_input, language_code=language_code)
        request = session.DetectIntentRequest(
            session=session_path, query_input=query_input
        )
        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print(f"Query text: {response.query_result.text}")
        response_messages = [
            " ".join(msg.text.text) for msg in response.query_result.response_messages
        ]
        print(f"Response text: {' '.join(response_messages)}\n")


def detect_intent_with_intent_input(
    project_id,
    location,
    agent_id,
    intent_id,
    language_code,
):
    """Returns the result of detect intent with sentiment analysis"""
    client_options = None
    if location != "global":
        api_endpoint = f"{location}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)
    session_id = str(uuid.uuid4())
    intents_client = IntentsClient()

    session_path = session_client.session_path(
        project=project_id,
        location=location,
        agent=agent_id,
        session=session_id,
    )
    intent_path = intents_client.intent_path(
        project=project_id,
        location=location,
        agent=agent_id,
        intent=intent_id,
    )

    intent = session.IntentInput(intent=intent_path)
    query_input = session.QueryInput(intent=intent, language_code=language_code)
    request = session.DetectIntentRequest(
        session=session_path,
        query_input=query_input,
    )

    response = session_client.detect_intent(request=request)
    response_text = []
    for response_message in response.query_result.response_messages:
        response_text.append(response_message.text.text)
        print(response_message.text.text)
    return response_text
if __name__ == "__main__":

    project_id = "citric-goal-343716"
    location_id = "asia-northeast1"
    agent_id = "8e648ef8-f318-4925-b99c-6242e5f802e7"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
    session_id = uuid.uuid4()
    texts = ["xin chào"]
    language_code = "vi-vn"
    # detect_intent_with_intent_input(project_id,
    #     location_id,
    #     agent_id,
    #     "Default Welcome Intent",
    #     language_code,)
    while True:
        texts = [input("mé: ")]
        detect_intent_texts(agent, session_id, texts, language_code)


    # detect_intent_texts(agent, session_id, texts, language_code)
    
    # PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    # AGENT_ID = os.getenv("AGENT_ID")
    # AGENT = f"projects/{PROJECT_ID}/locations/global/agents/{AGENT_ID}"
    # SESSION_ID = uuid.uuid4()
    # TEXTS = ["hello", "book a flight"]
    # AGENT_ID_US_CENTRAL1 = os.getenv("AGENT_ID_US_CENTRAL1")
    # AGENT_US_CENTRAL1 = (
    #     f"projects/{PROJECT_ID}/locations/us-central1/agents/{AGENT_ID_US_CENTRAL1}"
    # )