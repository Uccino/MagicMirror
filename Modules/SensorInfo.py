from Modules.MirrorModule import MirrorModule
import paho.mqtt.client as mqtt
import threading
import json
import os
import sys


class SensorModule(MirrorModule):

    def __init__(self, mirrorConfig, pageBuilder):
        self.PageBuilder = pageBuilder
        self.DataParser = MqttDataParser()
        self.MqttClient = MqttClient(mirrorConfig)
        self.PageMarkup = None

    def ZoomIn(self):
        pass

    def ZoomOut(self):
        pass

    def GetPageData(self):
        mqtt_data = self.MqttClient.GetMqttData()
        if mqtt_data is not None:
            return self.DataParser.ParseJsonData(mqtt_data)
        else:
            return {
                "name": "No data found",
                "temperature": 0,
                "humidity": 0
            }

    def BuildPageMarkup(self, pageData):
        self.PageMarkup = self.PageBuilder.BuildTemplate(
            "sensor_info.html", pageData)

    def GetPageMarkup(self):
        return self.PageMarkup

    def BuildPageNotifications(self, pageData):
        pass

    def GetPageNotifications(self):
        return None


class MqttDataParser():
    def __init__(self):
        pass

    def ParseJsonData(self, data):
        device_name = self._LookupSerial(data["hardware_serial"])
        temperature = data["payload_fields"]["Temperature"]
        humidity = data["payload_fields"]["Humidity"]

        data_json = {
            "name": device_name,
            "temperature": temperature,
            "humidity": humidity
        }

        return data_json

    def _LookupSerial(self, data):
        serialmap = self._ReadSerialmap()
        if data in serialmap:
            return serialmap[data]
        else:
            return data

    def _ReadSerialmap(self):
        platform = sys.platform
        json_path = None
        if not os.path.exists(f"{os.getcwd()}/Modules/data/serialmap.json"):
            return None

        with open(f"{os.getcwd()}/Modules/data/serialmap.json", "r") as serialmap:
            data = serialmap.read()
            return json.loads(data)


class MqttClient():
    def __init__(self, config):
        self.Client = mqtt.Client()
        self.Data = None

        broker_url = config["lora-mqtt"]["url"]
        broker_port = config["lora-mqtt"]["port"]
        self.broker_channel = config["lora-mqtt"]["channel"]

        self.Client.on_connect = self._on_connection
        self.Client.on_message = self._on_message

        self.Client.connect(broker_url, broker_port)
        listen_thread = threading.Thread(
            target=self.Client.loop_forever, daemon=True)
        listen_thread.start()

    def GetMqttData(self):
        if self.Data is not None and "payload_fields" in self.Data:
            return self.Data
        else:
            return None

    def _on_message(self, client, userdata, msg):
        try:
            print(msg.payload)
            data = json.loads(msg.payload)
            self.Data = data
        except:
            pass

    def _on_connection(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.Client.subscribe(self.broker_channel)
