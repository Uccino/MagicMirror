#!/usr/bin/python
from    PyMirror.webserver          import StartServer
from    PyMirror.websocketserver    import WebSocketServer
from    PyMirror.weatherapi         import OpenWeatherMap

import threading
import os
import json
import time
import locale
import os
import requests

def main():

    # Check if we're running on linux 
    if os.name == "posix":
        print("[!] YOU HAVEN'T SET THE LOCALE FOR LINUX YET ASSHAT [!]")
        print("[!] YOU HAVEN'T SET THE LOCALE FOR LINUX YET ASSHAT [!]")
        print("[!] YOU HAVEN'T SET THE LOCALE FOR LINUX YET ASSHAT [!]")
        print("[!] YOU HAVEN'T SET THE LOCALE FOR LINUX YET ASSHAT [!]")
        print("[!] YOU HAVEN'T SET THE LOCALE FOR LINUX YET ASSHAT [!]")
        print("[!] YOU HAVEN'T SET THE LOCALE FOR LINUX YET ASSHAT [!]")
        print("[!] YOU HAVEN'T SET THE LOCALE FOR LINUX YET ASSHAT [!]")
        print("[!] YOU HAVEN'T SET THE LOCALE FOR LINUX YET ASSHAT [!]")
        return
    else:        
        locale.setlocale(locale.LC_TIME,'nl-BE');        
        pass

    serverConfig = ReadConfig()
    if serverConfig == None:
        print("[!] Unable to read the config file")
        return

    serverIp = serverConfig["websockets"]["ip"]
    serverPort = serverConfig["websockets"]["port"]
    newsUrl = serverConfig["news"]["url"]

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
    forecast = GetWeatherInfo(weatherApi)
    news = GetNews(newsUrl)
    if news is None:
        print("[!] Unable to get the news!")
    print("[!] ENOUGH FOR THE DAY........")
    
def GetNews(url):    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            responseData = response.json()
            return responseData
        else:
            return None
    except Exception as generalException:
        print("[!] Undefined error!")
        print(generalException)
        return None    

def GetWeatherInfo(weatherApi):
    weatherInfo = weatherApi.GetWeatherInfo()

    currentForecast = weatherApi.GetCurrentWeatherForecast(weatherInfo)
    hourlyForecast = weatherApi.GetHourlyWeatherForecast(weatherInfo)
    dailyForecast = weatherApi.GetDailyForecast(weatherInfo)

    forecast = {
        "current":currentForecast,
        "hourly":hourlyForecast,
        "daily": dailyForecast
    }

    return forecast

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
