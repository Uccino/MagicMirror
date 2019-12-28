import paho.mqtt.client as mqtt
import os
import time


def connected():
    print("[X] Connected!")


def main():
    if not os.path.exists("data.json"):
        print("[X] Data.json not found!")
        return
    print("[X] Data.json found!")

    json_data = None
    with open("data.json", "r") as data:
        json_data = data.read()
    print("[X] Read the data!")
    client = mqtt.Client()
    print("[X] Connecting!")
    client.connect("mqtt.eclipse.org", 1883, 60)

    client.on_connect = connected
    print("[X] sending data!!")
    while 1:
        print("[X] Sending JSON data")
        client.publish("mirror/test01", json_data)
        time.sleep(60)


if __name__ == "__main__":
    main()
