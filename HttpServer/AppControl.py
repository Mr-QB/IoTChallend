import json
import paho.mqtt.client as mqtt
from flask import Flask, jsonify, request
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
            topic = json_data.get("topic")
            msg = json_data.get("msg")
            print("+++++\n", topic, msg)
            self.sentMQTTMsg(topic, msg)
            return "Message sent successfully"

        @self.app.route("/login", methods=["POST"])
        def checkLoginInfo():
            json_data = request.get_json()
            username = json_data.get("username")
            password = json_data.get("password")
            if username == "ac":
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401

        @self.app.route("/registers", methods=["POST"])
        def createUser():
            json_data = request.get_json()
            username = json_data.get("username")
            password = json_data.get("password")
            email = json_data.get("email")

            data_write = {"username": username, "password": password, "email": email}
            try:
                self.writeDataBase(self.users_database, data_write)
                return jsonify({"message": "Registration Success"}), 200
            except:
                return jsonify({"message": "Registration failed"}), 401

        # Run the Flask server in a separate thread
        Thread(
            target=lambda: self.app.run(debug=True, use_reloader=False, host="0.0.0.0")
        ).start()


if __name__ == "__main__":
    app_control = AppControl()
    # app_control.setUpMqtt("localhost")
    app_control.startHttpServer()
