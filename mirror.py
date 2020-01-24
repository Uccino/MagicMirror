from Core.HtmlBuilder import HtmlBuilder
from Core.ModuleManager import ModuleDataManager, ModulePositionManager
from Core.Websockets import WebSocketServer, MirrorConnectionHandler
from Core.Webserver import Webserver
from Core.InputHandler import InputHandler

from Modules import News, Weather, Calendar, SensorInfo

import os
import sys
import json
import threading
import webview
import time

__PLATFORM = sys.platform


def main():
    mirrorConfig = ReadConfig()
    if mirrorConfig is None:
        print("[!] Unable to read the configuration file!")
        return

    pageBuilder = HtmlBuilder()
    # All the pages we're going to use
    pages = []
    try:
        pages = [
            SensorInfo.SensorModule(mirrorConfig, pageBuilder),
            Weather.WeatherModule(mirrorConfig, pageBuilder),
            Calendar.CalendarModule(pageBuilder),
            News.NewsModule(mirrorConfig, pageBuilder)
        ]
    except Exception as e:
        print("Unable to setup the modules properly. Error:")
        print(e)
        return

    wsServer = StartWebsocketServer(mirrorConfig)
    if wsServer == None:
        print("[!] Unable to start the websocket server! ")
        return

    if StartWebserver(mirrorConfig) == False:
        print("[!] Unable to start the webserver! ")
        return

    module_position_manager = ModulePositionManager(pages)
    module_data_manager = ModuleDataManager(module_position_manager)

    while wsServer.IsRunning() is not True:
        time.sleep(1)

    connection_handler = MirrorConnectionHandler(wsServer)
    user_input_handler = InputHandler(
        module_position_manager, module_data_manager, connection_handler)

    # Uses keyboard & mouse on windows and gesture input on linux
    input_thread = threading.Thread(
        target=user_input_handler.GetUserInput, daemon=True)
    input_thread.start()

    data_update_interval = mirrorConfig["mirror"]["data_update_interval"]
    page_refresh_interval = mirrorConfig["mirror"]["mirror_refresh_interval"]
    notification_refresh_interval = mirrorConfig["mirror"]["notification_refresh_interval"]

    # Thread to update the module data
    data_update_thread = threading.Thread(
        target=module_data_manager.StartUpdatingMirrorData, daemon=True, args=[data_update_interval])
    data_update_thread.start()

    # Thread to keep refreshing the mirror page every few seconds
    mirror_refresh_thread = threading.Thread(target=RefreshMirror, args=[
        connection_handler, module_data_manager, page_refresh_interval])
    mirror_refresh_thread.daemon = True
    mirror_refresh_thread.start()

    # Thread to refresh the mirror's notifications every few seconds
    notification_refresh_thread = threading.Thread(
        target=RefreshNotifications, args=[
            connection_handler, module_data_manager, page_refresh_interval])
    notification_refresh_thread.daemon = True
    notification_refresh_thread.start()

    mirror_url = "http://" + \
        mirrorConfig["webserver"]["ip"] + ":" + \
        str(mirrorConfig["webserver"]["port"]) + "/mirror"

    print(mirror_url)
    webview.create_window(
        title="Mirror page", url=mirror_url, width=1920, height=1080)
    webview.start()


def RefreshNotifications(mirror_connection, mirror_data, refresh_interval):
    while 1:
        mirror_notifications = mirror_data.GetModuleNotifications()
        mirror_connection.SendMirrorNotifications(mirror_notifications)
        time.sleep(refresh_interval)


def RefreshMirror(mirror_connection, mirror_data, refresh_interval):
    while 1:
        data = mirror_data.GetModuleData()
        mirror_connection.SendMirrorPage(data)

        time.sleep(refresh_interval)


def StartWebsocketServer(mirrorConfig):
    """[Starts the websocket server]

    Arguments:

        mirrorConfig {[dict]} -- [Configuration read by ReadConfig()]

    Returns:

        [WebsocketServer] -- [Returns a websocket server instance if the server was succesfully started, else it returns none]
    """
    serverIp = None
    serverPort = None

    try:
        serverIp = mirrorConfig["websockets"]["ip"]
        serverPort = mirrorConfig["websockets"]["port"]
    except:
        return None

    wsServer = WebSocketServer(serverIp, serverPort)
    websocketThread = threading.Thread(target=wsServer.StartServer)
    websocketThread.daemon = True

    try:
        websocketThread.start()
        return wsServer
    except:
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
    except:
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
    dir_path = ""
    if __PLATFORM == "win32":
        dir_path = os.path.dirname(
            os.path.realpath(__file__)) + r"\config.json"
    elif __PLATFORM == "linux":
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/config.json"

    if(not os.path.exists(dir_path)):
        return None
    with open(dir_path, 'r') as jsonFile:
        configData = json.load(jsonFile)
        return configData


if __name__ == "__main__":
    main()
