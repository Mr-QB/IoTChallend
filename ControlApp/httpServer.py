from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route("/data", methods=["GET"])
def get_data():
    data = {"msg": "Chao Phuong"}
    return jsonify(data)


@app.route("/control", methods=["POST"])
def control():
    json_data = request.get_json()
    with open("saved_data.json", "w") as f:
        json.dump(json_data, f)
    return "Data saved successfully"


if __name__ == "__main__":
    app.run(debug=True)
