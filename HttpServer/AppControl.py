import json
import paho.mqtt.client as mqtt
from flask import Flask, jsonify, request
from bson import json_util
import subprocess
from threading import Thread
from pymongo import MongoClient
from config import *


class AppControl:
    def __init__(self):
        # self.startTunnel()
        self.app = Flask(__name__)

        self.client = MongoClient(DATABASEURL)
        self.database = self.client[DATABASENAME]
        self.users_database = self.database["Users"]
        self.devices_database = self.database["Devices"]
        self.scripts_database = self.database["Scripts"]

    def writeDataBase(self, users_database, data):
        users_database.insert_one(data)

    def setUpMqtt(self, broker, mqtt_port=1883, mqtt_username="", mqtt_password=""):
        self.broker = broker
        self.mqtt_port = mqtt_port
        self.mqtt_username = mqtt_username
        self.mqtt_password = mqtt_password

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.username_pw_set(self.mqtt_username, self.mqtt_password)
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.connect(broker, self.mqtt_port, 60)

    def startTunnel(self):
        command = "autossh -M 0 -o ServerAliveInterval=60 -i DialogflowCX/key/id_ssh -R iotchallengemqtt.rcuet.id.vn:80:localhost:5000 serveo.net"
        subprocess.Popen(command, shell=True)

    def sentMQTTMsg(self, topic, msg):
        self.mqtt_client.publish(topic, msg, 0, True)

    def startHttpServer(self):
        @self.app.route("/data", methods=["GET"])
        def get_data():
            data = {"msg": "Chao Phuong"}
            return jsonify(data)

        @self.app.route("/control", methods=["POST"])
        def control():
            json_data = request.get_json()
            device_id = int(json_data.get("device_id"))
            status = json_data.get("status")
            print(device_id, status)

            query = {"id": device_id}

            if status == "true":
                # self.sentMQTTMsg(device_id, 1)
                update_data = {"$set": {"status": 1}}

            if status == "false":
                # self.sentMQTTMsg(device_id, 0)
                update_data = {"$set": {"status": 0}}

            result = self.devices_database.update_one(query, update_data, upsert=True)

            if result.modified_count > 0:
                return (
                    jsonify(
                        {"status": "success", "message": "Device updated successfully"}
                    ),
                    200,
                )
            elif result.upserted_id is not None:
                return (
                    jsonify(
                        {"status": "success", "message": "Device created successfully"}
                    ),
                    201,
                )
            else:
                return jsonify({"status": "error", "message": "No changes made"}), 304

        @self.app.route("/login", methods=["POST"])
        def checkLoginInfo():
            json_data = request.get_json()
            username = json_data.get("username")
            password = json_data.get("password")
            print(username, password)

            query = {"username": username, "password": password}

            if self.users_database.count_documents(query) > 0:
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401

        @self.app.route("/createscipts", methods=["POST"])
        def createscipts():
            json_data = request.get_json()  # Lấy dữ liệu JSON từ yêu cầu
            print(json_data)
            if json_data is None:
                return (
                    jsonify({"error": "Invalid JSON"}),
                    400,
                )  # Trả về lỗi nếu không có dữ liệu JSON
            for script in json_data:
                if script["type"] == "Timer":
                    query = {"device_name": script["deviceName"]}
                    list_devices = list(self.devices_database.find(query, {"_id": 0}))
                    device_id = list_devices[0]["id"]

                    timer = script["timer"]

                    new_script = {
                        "type": "Timer",
                        "device_id": device_id,
                        "status": script["status"],
                        "timer": timer,
                    }

                    result = self.scripts_database.insert_one(new_script)

                    print(script)  # In dữ liệu JSON ra console

            return (
                jsonify({"message": "Data received successfully"}),
                200,
            )  # Trả về phản hồi thành công

        @self.app.route("/register", methods=["POST"])
        def createUser():
            json_data = request.get_json()
            username = json_data.get("username")
            password = json_data.get("password")
            email = json_data.get("email")

            query = {"username": username}
            if self.users_database.count_documents(query) > 0:
                return jsonify({"message": "Username already exists"}), 402

            data_write = {"username": username, "password": password, "email": email}
            try:
                self.writeDataBase(self.users_database, data_write)
                return jsonify({"message": "Registration Success"}), 200
            except:
                return jsonify({"message": "Registration failed"}), 401

        @self.app.route("/updatedevice", methods=["POST"])
        def addDivice():
            json_data = request.get_json()
            device_name = json_data.get("device_name")
            room_name = json_data.get("room_name")
            device_id = int(json_data.get("device_id"))

            query = {"id": device_id}
            update_data = {"$set": {"device_name": device_name, "room_name": room_name}}
            result = self.devices_database.update_one(query, update_data, upsert=True)

            if result.modified_count > 0:
                return (
                    jsonify(
                        {"status": "success", "message": "Device updated successfully"}
                    ),
                    200,
                )
            elif result.upserted_id is not None:
                return (
                    jsonify(
                        {"status": "success", "message": "Device created successfully"}
                    ),
                    201,
                )
            else:
                return jsonify({"status": "error", "message": "No changes made"}), 304

        @self.app.route("/deletedevice", methods=["POST"])
        def deleteDivice():
            json_data = request.get_json()
            # device_name = json_data.get("device_name")
            room_name = json_data.get("room_name")
            device_id = int(json_data.get("device_id"))
            # print(device_id)

            query = {"id": device_id}
            update_data = {"$set": {"device_name": "", "room_name": ""}}
            result = self.devices_database.update_one(query, update_data, upsert=True)

            if result.modified_count > 0:
                return (
                    jsonify(
                        {"status": "success", "message": "Device updated successfully"}
                    ),
                    200,
                )
            elif result.upserted_id is not None:
                return (
                    jsonify(
                        {"status": "success", "message": "Device created successfully"}
                    ),
                    201,
                )
            else:
                return jsonify({"status": "error", "message": "No changes made"}), 304

        @self.app.route("/getdevices", methods=["GET"])
        def getDevicesInfo():
            query = {
                "room_name": {"$ne": ""},
                "device_name": {"$ne": ""},
                "type": "plug",
            }
            list_devices = list(self.devices_database.find(query, {"_id": 0}))

            if list_devices:
                return json_util.dumps(list_devices), 200
            else:
                return jsonify({"message": "No devices found"}), 404

        @self.app.route("/getsensors", methods=["GET"])
        def getSensorsInfo():
            query = {
                "room_name": {"$ne": ""},
                "device_name": {"$ne": ""},
                "type": "sensor",
            }
            list_devices = list(self.devices_database.find(query, {"_id": 0}))
            if list_devices:
                return json_util.dumps(list_devices), 200
            else:
                return jsonify({"message": "No devices found"}), 404

        @self.app.route("/getscripts", methods=["GET"])
        def getScriptsInfo():
            all_scripts = list(self.scripts_database.find())
            if all_scripts:
                return json_util.dumps(all_scripts), 200
            else:
                return jsonify({"message": "No devices found"}), 404

        @self.app.route("/checkdevicesnotconfig", methods=["GET"])
        def checkDevicesNotConfig():
            query = {"$or": [{"room_name": ""}, {"device_name": ""}]}
            try:
                list_devices = list(self.devices_database.find(query, {"_id": 0}))
                return json_util.dumps(list_devices), 200
            except:
                return jsonify({"message": "Invalid credentials"}), 401

        # Run the Flask server in a separate thread
        Thread(
            target=lambda: self.app.run(debug=True, use_reloader=False, host="0.0.0.0")
        ).start()


if __name__ == "__main__":
    app_control = AppControl()
    # app_control.setUpMqtt("localhost")
    app_control.startHttpServer()
