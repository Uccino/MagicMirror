from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import os
import json

class MagicMirrorServer(WebSocket):
    # Handles the incomming messages
    def handleMessage(self):
        jsonMessage = json.loads(self.data)
        if(jsonMessage["message"] == "get_config"):
            print("Send Config!")
            # Config should be any JSON message
            # Probably going to be positions of certain items 

    # Handles new connections with the server
    def handleConnected(self):
        print(f"[x] New connection! {self.address[0]}:{self.address[1]} connected.");
        
    # Handles closing connections.
    def handleClose(self):        
        print(f"[x] {self.address} disconnected!")

# Reads the config.json 
# contains the IP and PORT the webserver should be hosted on
def ReadConfig(path="config.json"):
    # Check if file exists
    if(not os.path.exists(path)):       
        return None
    
    with open(path, 'r') as jsonFile:
        configData = json.load(jsonFile)
        return configData

def main():
    print(f"[x] MagicMirror by Corné Hoeving")
    print("[x] Reading config")

    serverConfig = ReadConfig()
    if serverConfig == None:
        print("[!] Unable to read the config.json")
        return

    serverIp = serverConfig["websockets"]["ip"]
    serverPort = serverConfig["websockets"]["port"]

    print(f"[x] Starting server!")
    StartServer(serverIp, serverPort)

def StartServer(ip, port):    
    server = SimpleWebSocketServer(ip, port, MagicMirrorServer)
    server.serveforever()

if __name__ == '__main__':
    main()