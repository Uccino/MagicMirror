from Core.HtmlBuilder import HtmlBuilder
from Core.PageManager import PageManager
from Core.Webserver import Webserver
from Core.Websockets import WebSocketServer
from Core.InputManager import InputGetter
from Modules import News, Weather, Calendar

import os, sys
import json
import threading
import webview
import time
import base64

__PLATFORM = sys.platform

def main():
    mirrorConfig = ReadConfig()
    if mirrorConfig == None:
        print("[!] Unable to read the configuration file!")
        return

    pageBuilder = HtmlBuilder()

    websocketIp = mirrorConfig["websockets"]["ip"]
    websocketPort = mirrorConfig["websockets"]["port"]

    wsServer = WebSocketServer(websocketIp, websocketPort)
    if StartWebsocketThread(wsServer) == False:
        print("[!] Unable to start the websocket server! ")
        return
    
    if StartWebserver(mirrorConfig) == False:
        print("[!] Unable to start the webserver! ")
        return
    
    StartWebview(mirrorConfig)

    # All the pages we're going to use
    pages = [
        Weather.WeatherPage(mirrorConfig,pageBuilder ),
        Calendar.CalendarPage(mirrorConfig, pageBuilder),
        News.NewsPage(mirrorConfig,pageBuilder)
    ]

    pageManager = PageManager(pages)

    updateThread = threading.Thread(target=pageManager.UpdatePages, daemon=True)
    updateThread.start()

    while 1:
        markup = pageManager.GetPageMarkup()
        SendMirrorPage(wsServer, markup)
        time.sleep(10)

def SendMirrorPage(websocketServer, data):
    pageData = {
        "type": "mirror_page",
        "data":data
    }
    b64data = base64.b64encode(json.dumps(pageData).encode('utf-8'))
    websocketServer.SendMessage(b64data)

def SendMirrorNotification(websocketServer, data):
    pageData = {
        "type": "mirror_notification",
        "data":data
    }
    b64data = base64.b64encode(json.dumps(pageData).encode('utf-8'))
    websocketServer.SendMessage(b64data)

def StartWebsocketThread(websocketServer):
    websocketThread = threading.Thread(target=websocketServer.StartServer)
    websocketThread.daemon = True
    try:
        websocketThread.start()
        return True
    except:
        return False

def StartWebserver(mirrorConfig):
    serverIp = mirrorConfig["webserver"]["ip"]
    serverPort = mirrorConfig["webserver"]["port"]
    wServer = Webserver(serverIp, serverPort)
    websocketThread = threading.Thread(target=wServer.StartServer)
    websocketThread.daemon = True
    try:
        websocketThread.start()
        return True
    except:
        return False

def StartWebview(config):
    serverIp = config["webserver"]["ip"]
    serverPort = config["webserver"]["port"]
    serverUrl = f"http://{serverIp}:{serverPort}/mirror"   
    url = serverUrl

    webview.create_window("SmartMirror", url=url)
    webviewThread = threading.Thread(target=webview.start, name="MainThread")
    webviewThread.daemon = True
    webviewThread.start()

# Reads the config.json from the file
def ReadConfig(path="./config.json"):
    if __PLATFORM == "win32":
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "\config.json"    
        if(not os.path.exists(dir_path)):        
            return None
        with open(dir_path, 'r') as jsonFile:
            configData = json.load(jsonFile)
            return configData
    elif __PLATFORM == "linux":
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/config.json"    
        print(dir_path)
        if(not os.path.exists(dir_path)):        
            return None
        with open(dir_path, 'r') as jsonFile:
            configData = json.load(jsonFile)
            return configData

if __name__ == "__main__":
    main()