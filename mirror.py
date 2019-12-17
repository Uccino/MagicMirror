from Core.HtmlBuilder import HtmlBuilder
from Core.ModuleManager import ModuleManager
from Core.Webserver import Webserver
from Core.Websockets import WebSocketServer
# from Core.InputHandler import InputHandler
from Core.MirrorManager import MirrorManager
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

    wsServer = StartWebsocketServer(mirrorConfig)
    if wsServer == None:
        print("[!] Unable to start the websocket server! ")
        return

    if StartWebserver(mirrorConfig) == False:
        print("[!] Unable to start the webserver! ")
        return

    # All the pages we're going to use
    pages = [
        Calendar.CalendarModule(mirrorConfig, pageBuilder),
        Weather.WeatherModule(mirrorConfig, pageBuilder),
        News.NewsModule(mirrorConfig, pageBuilder)
    ]

    moduleManager = ModuleManager(pages)
    mirrorManager = MirrorManager(wsServer, moduleManager)

    # inputHandler = InputHandler(moduleManager, mirrorManager)
    # inputThread = threading.Thread(target=inputHandler.GetGestureInput, daemon=True)
    # inputThread.start()

    moduleManager.UpdatePages()
    mirrorManager.UpdateMirrorPage()
    mirrorManager.StartUpdatingData()

    # StartWebview(mirrorConfig)
    while 1:
        pass


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
    webview.start()
    # webviewThread = threading.Thread(target=webview.start, name="MainThread")
    # webviewThread.daemon = True
    # webviewThread.start()


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
