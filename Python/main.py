#!/usr/bin/python
from    PyMirror.webserver          import StartServer
from    PyMirror.websocketserver    import WebSocketServer
from    PyMirror.weatherapi         import OpenWeatherMap

import threading
import os
import json
import urllib
import time

def main():
    serverConfig = ReadConfig()
    if serverConfig == None:
        print("[!] Unable to read the config file")
        return

    serverIp = serverConfig["websockets"]["ip"]
    serverPort = serverConfig["websockets"]["port"]

    websocketServer = WebSocketServer(serverIp, serverPort)

    print("[x] Starting websocket server thread")
    if StartWebsocketServer(websocketServer) == False:
        print("[!] Unable to start the websocket server")
        return
    print("[x] Starting webserver thread")
    if StartWebserver() == False:
        print("[!] Unable to start the webserver")
        return
    
    weatherApi = BuildWeatherApi(serverConfig)
    
    weatherInfo = weatherApi.GetWeatherInfo()

    currentForecast = weatherApi.GetCurrentWeatherForecast(weatherInfo)
    hourlyForecast = weatherApi.GetHourlyWeatherForecast(weatherInfo)
    dailyForecast = weatherApi.GetDailyForecast(weatherInfo)

    forecast = {
        "current":currentForecast,
        "hourly":hourlyForecast
    }

# Builds the weather API class from the configuration file
def BuildWeatherApi(serverConfig):
    weatherLanguage = serverConfig["weather"]["language"]
    weatherApiKey = serverConfig["weather"]["key"]
    
    weatherLat = serverConfig["weather"]["location"]["latitude"]
    weatherLong = serverConfig["weather"]["location"]["longitude"]
    weatherLocationName = serverConfig["weather"]["location"]["name"]

    weatherApi = OpenWeatherMap(weatherApiKey,
        weatherLanguage, 
        weatherLat, 
        weatherLong,
        weatherLocationName
    )

    return weatherApi

# Starts the websocket server
def StartWebsocketServer(websocketServer):
    try:        
        websocketServer.SetupServer()
        serverThread = threading.Thread(target=websocketServer.StartServer)
        serverThread.start()
    except:        
        return False

# Starts the flask webserver
def StartWebserver():    
    try:
        print("[x] Starting webserver thread")
        serverThread = threading.Thread(target=StartServer)
        serverThread.start()
        return True
    except:        
        return False

# Reads the config.json from the file
def ReadConfig(path="./config.json"):
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "\config.json"    
    if(not os.path.exists(dir_path)):        
        return None
    with open(dir_path, 'r') as jsonFile:
        configData = json.load(jsonFile)
        return configData

if __name__ == '__main__':    
    main()
