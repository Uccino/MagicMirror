from Modules.MirrorModule import MirrorModule
import paho.mqtt.client as mqtt
import threading
import json


class SensorModule(MirrorModule):

    def __init__(self, mirrorConfig, pageBuilder):
        self.PageBuilder = pageBuilder

        self.MqttClient = MqttClient(mirrorConfig)
        self.MqttClient.Start_listening()

    def ZoomIn(self):
        pass

    def ZoomOut(self):
        pass

    def GetPageData(self):
        return self.MqttClient.GetMqttData()

    def BuildPageMarkup(self, pageData):
        pass

    def GetPageMarkup(self):
        pass

    def BuildPageNotifications(self, pageData):
        pass

    def GetPageNotifications(self):
        return None


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
        self.Client.loop_forever()

    def GetMqttData(self):
        return self.Data

    def _on_message(self, client, userdata, msg):
        try:
            print(msg.payload)
            data = json.loads(msg.payload)
            self.Data = data
        except:
            print("Whats dis shit")
            pass

    def _on_connection(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.Client.subscribe(self.broker_channel)
