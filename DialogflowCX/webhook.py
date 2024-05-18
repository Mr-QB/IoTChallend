from flask import Flask, request, jsonify
import json
from datetime import datetime

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

        return responseMgs(messages)


    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
