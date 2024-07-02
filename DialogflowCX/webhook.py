from flask import Flask, request, jsonify
import json
from datetime import datetime
import subprocess
import requests
import os
import google.generativeai as genai

# OpenWeatherMap API key
WEATHER_API_KEY = "2c430b975eca3a7ccf32915d7a02fb28"
GEMINI_API_KEY = "AIzaSyA0OoAfMr0qrBAdgJQ-TnM9dkWMDztKT2Q" # lấy ở đây nhé https://aistudio.google.com/app/apikey


def configGeminiBot():

    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
    )
    return model


model = configGeminiBot()  # Setup Gemini bot


def callGemini(msg, model=model):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(msg)
    return response.text


def start_tunnel():
    command = 'autossh -M 0 -o ServerAliveInterval=60 -i DialogflowCX/key/id_rsa -R iotchallenge.rcuet.id.vn:80:localhost:5000 serveo.net'
    subprocess.Popen(command, shell=True)


def save_to_json_file(data, filename="DialogflowCX/sample.json"):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)


def responseMgs(
    messages,
):  # The function writes the response json structure for the webhook call
    return jsonify(
        {"fulfillment_response": {"messages": [{"text": {"text": [messages]}}]}}
    )


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"Nhiệt độ hiện tại ở {city} là {temp} độ C với {description}."
    else:
        return "Không thể lấy thông tin thời tiết cho thành phố này."


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def dialogflow():
    data = request.get_json()
    if data:
        save_to_json_file(data)  # saves a message about the webhook call
        messages = ""

        webhook_tag = data["fulfillmentInfo"]["tag"]

        if webhook_tag == "askTime":  # Intent Ask about the current date and time
            now = datetime.now()

            hour = now.hour
            minute = now.minute
            day = now.day
            month = now.month
            year = now.year

            messages = f"Bây giờ là {hour} giờ {minute} phút ngày {day} tháng {month} năm {year}"

        elif webhook_tag == "askWeather":  # Intent Ask about the weather
            city = data["sessionInfo"]["parameters"]["geo-city"]
            messages = get_weather(city)

        elif webhook_tag == "askGemini":
            question = data["text"]
            messages = callGemini(question)
            # print(messages)

        return responseMgs(messages)


if __name__ == "__main__":
    # callGemini("một cộng một bằng  mấy")
    start_tunnel()
    app.run(host="0.0.0.0", port=5000)