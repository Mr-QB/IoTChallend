from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Route để nhận yêu cầu GET từ client
@app.route('/api/data', methods=['GET'])
def get_data():
    # Dữ liệu ví dụ
    data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }
    return jsonify(data)

# Route để nhận yêu cầu POST từ client và lưu vào file JSON
@app.route('/api/save', methods=['POST'])
def save_data():
    # Lưu dữ liệu nhận được từ client vào file JSON
    json_data = request.get_json()
    with open('saved_data.json', 'w') as f:
        json.dump(json_data, f)
    return 'Data saved successfully'

if __name__ == '__main__':
    app.run(debug=True)
