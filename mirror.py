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

__PLATFORM = sys.platform

def main():
    mirrorConfig = ReadConfig()
    if mirrorConfig == None:
        print("[!] Unable to read the configuration file!")
        return

    pageBuilder = HtmlBuilder()

    # All the pages we're going to use
    pages = [
        Calendar.CalendarPage(mirrorConfig, pageBuilder),
        News.NewsPage(mirrorConfig,pageBuilder),
        Weather.WeatherPage(mirrorConfig,pageBuilder )        
    ]
    
    pageManager = PageManager(pages)
    
    while 1:
        pageData = pageManager.GetPageData()
        if pageData is not None:
            print(pageManager.GetPageMarkup(pageData))
        time.sleep(60)

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