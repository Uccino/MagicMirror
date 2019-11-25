from components import WebServerManager
from components import WebSocketManager

from components import WeatherGatherer
from components import NewsGatherer
from components import CalendarGatherer

import os, sys
import json
import threading

# Main function
def main():
    mirrorConfig = ReadConfig()

    if mirrorConfig == None:
        print("[!] Unable to read the config file")
        return
    
    if StartWebserver(mirrorConfig) == False:
        print("[!] Unable to start the webserver")
        return
    

    if StartWebsocketServer(mirrorConfig) == None:
        print("[!] Unable to start the websocket server")
        return
    
    newsRequester = BuildNewsRequester(mirrorConfig)
    openWeatherApiRequests = BuildWeatherRequester(mirrorConfig)
    
    latestNews = newsRequester.GetNews()


# Builds the class for getting the weather
def BuildWeatherRequester(config):

    apiKey = config["weather"]["key"]
    language = config["weather"]["language"]
    locationName = config["weather"]["location"]["name"]
    locationLat = config["weather"]["location"]["latitude"]
    locationLong = config["weather"]["location"]["longitude"]

    weatherRequester = WeatherGatherer.OpenWeatherMap(apiKey, 
        language,
        locationLat,
        locationLong,
        locationName
    )

    return weatherRequester

# Builds the class for getting the news
def BuildNewsRequester(config):
    newsSiteIp = config["webserver"]["ip"]
    newsSitePort = config["webserver"]["port"]
    newsRequester = NewsGatherer.NewsRequester(5,newsSiteIp, newsSitePort)

    return newsRequester

# Starts the flask webserver
def StartWebserver(config):
    serverHost = config["webserver"]["ip"]
    serverPort = config["webserver"]["port"]
    webManager = WebServerManager.Webserver(serverHost, serverPort)    
    try:
        serverThread = threading.Thread(target=webManager.StartServer)
        serverThread.start()
        print(f"[x] Webserver runs on {serverHost}:{serverPort}")
        return True
    except:
        return False

# Starts the websocket server
def StartWebsocketServer(config):    
    wsServerIp = config["websockets"]["ip"]
    wsServerPort = config["websockets"]["port"]

    websocketServer = WebSocketManager.WebSocketServer(wsServerIp, wsServerPort)

    try:
        serverThread = threading.Thread(target=websocketServer.StartServer)
        serverThread.start()

        print(f"[x] Websocket server runs on {wsServerIp}:{wsServerPort}")

        return websocketServer
    except:        
        return None

# Reads the config.json from the filea
def ReadConfig(path="./config.json"):
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "\config.json"    
    if(not os.path.exists(dir_path)):        
        return None
    with open(dir_path, 'r') as jsonFile:
        configData = json.load(jsonFile)
        return configData

# Entry point of the program
if __name__ == '__main__':
    main()