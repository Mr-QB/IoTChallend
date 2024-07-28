import json
import paho.mqtt.client as mqtt
import time as time_module
from threading import Thread, Event
from pymongo import MongoClient
from config import *
from datetime import datetime, time


class RunScripts:
    def __init__(self):
        self.client = MongoClient(DATABASEURL)
        self.database = self.client[DATABASENAME]
        self.users_database = self.database["Users"]
        self.devices_database = self.database["Devices"]
        self.scripts_database = self.database["Scripts"]

        self.stop_event = Event()

    def isPastTimer(self, timer_str):
        now = datetime.now().time()
        timer = datetime.strptime(timer_str, "%H:%M").time()
        return now > timer

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

    def checkTimer(self):
        query = {"type": "Timer"}
        scripts = list(self.scripts_database.find(query))
        for script in scripts:
            if self.isPastTimer(script["timer"]):
                if script["status"] == "ON":
                    # self.mqtt_client.publish(script["device_id"], 1, 0, True)
                    pass
                elif script["status"] == "OFF":
                    # self.mqtt_client.publish(script["device_id"], 0, 0, True)
                    print(script["device_id"])
                    pass

    def startChecking(self):
        def run():
            while not self.stop_event.is_set():
                self.checkTimer()
                self.stop_event.wait(7)  # Wait for 7 seconds before checking again

        self.check_thread = Thread(target=run)
        self.check_thread.start()

    def stopChecking(self):
        self.stop_event.set()
        self.check_thread.join()  # Wait for the thread to finish


if __name__ == "__main__":
    runtool = RunScripts()
    # runtool.setUpMqtt("broker_address")
    runtool.startChecking()

    # while True:
    #     time_module.sleep(1)
