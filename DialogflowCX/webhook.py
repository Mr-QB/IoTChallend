from flask import Flask, request, jsonify
import json
from datetime import datetime
import subprocess
import requests

# OpenWeatherMap API key
API_KEY = '2c430b975eca3a7ccf32915d7a02fb28'

def start_tunnel():
    command = 'autossh -M 0 -o ServerAliveInterval=60 -i DialogflowCX/key/id_rsa -R iotchallenge.rcuet.id.vn:80:localhost:5000 serveo.net'
    subprocess.Popen(command, shell=True)

def save_to_json_file(data, filename='DialogflowCX/sample.json'):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4) 

def responseMgs(messages): # The function writes the response json structure for the webhook call
    return jsonify(
        {
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [messages]}}
                ]
            }
        }
    )

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Nhiệt độ hiện tại ở {city} là {temp} độ C với {description}."
    else:
        return "Không thể lấy thông tin thời tiết cho thành phố này."

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def dialogflow():
    data = request.get_json()
    if data:
        save_to_json_file(data) # saves a message about the webhook call
        messages = ""

        webhook_tag = data["fulfillmentInfo"]["tag"]

        if webhook_tag == "askTime": # Intent Ask about the current date and time
            now = datetime.now()

            hour = now.hour
            minute = now.minute
            day = now.day
            month = now.month
            year = now.year

            messages = f"Bây giờ là {hour} giờ {minute} phút ngày {day} tháng {month} năm {year}"

        elif webhook_tag == "askWeather": # Intent Ask about the weather
            city = data["sessionInfo"]["parameters"]["geo-city"]
            messages = get_weather(city)

        return responseMgs(messages)
    

if __name__ == "__main__":
    start_tunnel()
    app.run(host="0.0.0.0", port=5000)