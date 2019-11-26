from websocket_server import WebsocketServer as wsServer

class WebSocketServer():
    def __init__(self, ip, port):
        self.ServerIp = ip
        self.ServerPort = port
        self.Server = wsServer(port, ip)

        self.SetupServer()

    def SetupServer(self):
        self.Server.set_fn_client_left(self._ClientLeft)
        self.Server.set_fn_message_received(self._MessageReceived)

    def StartServer(self):
        try:
            print("[x] Starting websocket server.")
            self.Server.run_forever()
        except:
            print("[!] Unable to run the server.")

    def SendMessage(self, data):
        print("[x] Sending message to all the clients.")
        self.Server.send_message_to_all(data)

    def CloseServer(self):
        self.Server.server_close()

    def _ClientLeft(self, client, server):
        print("[!] Client disconnected!")

    def _MessageReceived(self, client, server, message):
        print(f"[x] Message recieved: {message}")
