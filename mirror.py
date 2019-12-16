from Core.HtmlBuilder import HtmlBuilder
from Core.PageManager import PageManager
from Core.Webserver import Webserver
from Core.Websockets import WebSocketServer
from Core.InputManager import InputGetter
from Modules import News, Weather, Calendar

import os
import sys
import json
import threading
import webview
import time
import base64

__PLATFORM = sys.platform


def main():
    mirrorConfig = ReadConfig()
    if mirrorConfig is None:
        print("[!] Unable to read the configuration file!")
        return

    pageBuilder = HtmlBuilder()
    
    # wsServer = StartWebsocketServer(mirrorConfig)
    # if wsServer == None:
    #     print("[!] Unable to start the websocket server! ")
    #     return

    # if StartWebserver(mirrorConfig) == False:
    #     print("[!] Unable to start the webserver! ")
    #     return

    # StartWebview(mirrorConfig)

    # All the pages we're going to use
    pages = [
        Calendar.CalendarPage(mirrorConfig, pageBuilder),
        Weather.WeatherPage(mirrorConfig, pageBuilder),
        News.NewsPage(mirrorConfig, pageBuilder)
    ]

    pageManager = PageManager(pages)

    pageManager.UpdatePageData()
    pageManager.UpdatePageNotifications()

    pageManager.GetNotifications()

    # dataUpdateThread = threading.Thread(target=pageManager.UpdatePageData, daemon=True)
    # dataUpdateThread.start()

    # while 1:
    #     markup = pageManager.GetPageMarkup()
    #     SendMirrorPage(wsServer, markup)
    #     time.sleep(10)


def SendMirrorPage(websocketServer, data):
    """[Sends the HTML markup as a mirror page to all clients]
    
    Arguments:

        websocketServer {[WebsocketServer]} -- [Websocket server with the clients]
        data {[str]} -- [HTML markup to be send to the mirror]
    """            
    pageData = {
        "type": "mirror_page",
        "data": data
    }
    b64data = base64.b64encode(json.dumps(pageData).encode('utf-8'))
    websocketServer.SendMessage(b64data)

def SendMirrorNotification(websocketServer, data):
    pageData = {
        "type": "mirror_notification",
        "data": data
    }
    b64data = base64.b64encode(json.dumps(pageData).encode('utf-8'))
    websocketServer.SendMessage(b64data)

def StartWebsocketServer(mirrorConfig):
    """[Starts the websocket server]
    
    Arguments:

        mirrorConfig {[dict]} -- [Configuration read by ReadConfig()]
    
    Returns:

        [WebsocketServer] -- [Returns a websocket server instance if the server was succesfully started, else it returns none]
    """    
    serverIp = mirrorConfig["websockets"]["ip"]
    serverPort = mirrorConfig["websockets"]["port"]
    wsServer = WebSocketServer(serverIp, serverPort)
    websocketThread = threading.Thread(target=wsServer.StartServer)
    websocketThread.daemon = True
    try:
        websocketThread.start()
        return wsServer
    except Exception:
        return None

def StartWebserver(mirrorConfig):
    """[Starts the flask webserver in a seperate thread]
    
    Arguments:

        mirrorConfig {[dict]} -- [Configuration read by ReadConfig()]
    
    Returns:

        [bool] -- [True if succesfully started]
    """    
    serverIp = mirrorConfig["webserver"]["ip"]
    serverPort = mirrorConfig["webserver"]["port"]
    wServer = Webserver(serverIp, serverPort)
    websocketThread = threading.Thread(target=wServer.StartServer)
    websocketThread.daemon = True
    try:
        websocketThread.start()
        return True
    except BaseException:
        return False

def StartWebview(config):
    """[Starts the pywebview]
    
    Arguments:

        config {[dict]} -- [Configuration read by ReadConfig()]
    """        
    
    serverIp = config["webserver"]["ip"]
    serverPort = config["webserver"]["port"]
    serverUrl = f"http://{serverIp}:{serverPort}/mirror"
    url = serverUrl   
    webview.create_window("SmartMirror", url=url)
    webviewThread = threading.Thread(target=webview.start, name="MainThread")
    webviewThread.daemon = True
    webviewThread.start()

def ReadConfig(path="./config.json"):
    """Reads the configuration for the mirror
    
    Keyword Arguments:
        path {str} -- [path to the config file] (default: {"./config.json"})
    
    Returns:

        dict -- Configuration in JSON format

    """        
    if __PLATFORM == "win32":
        dir_path = os.path.dirname(
            os.path.realpath(__file__)) + r"\config.json"
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
