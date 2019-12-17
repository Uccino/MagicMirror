from websocket_server import WebsocketServer as wsServer


class WebSocketServer():
    def __init__(self, ip, port):
        self.ServerIp = ip
        self.ServerPort = port
        self.Server = wsServer(port, ip)
        self.SetupServer()

    def SetupServer(self):
        """ Sets the websocket_server event handlers
        """
        self.Server.set_fn_client_left(self._ClientLeft)
        self.Server.set_fn_message_received(self._MessageReceived)
        self.Server.set_fn_new_client(self._ClientConnected)

    def StartServer(self):
        """Starts the websocket_server forever
        """
        try:
            print("[x] Starting websocket server.")
            self.Server.run_forever()
        except BaseException:
            print("[!] Unable to run the server.")

    def SendMessage(self, data):
        """Sends a message to all clients

        Arguments:
            data {String} -- [String of text to be send]
        """
        # print("[x] Sending message to all the clients.")
        self.Server.send_message_to_all(data)        

    def CloseServer(self):
        """Closes the websocket server
        """
        self.Server.server_close()

    def _ClientLeft(self, client, server):
        """Event handler for when a client disconnects from the server
        """
        print("[!] Client disconnected!")

    def _ClientConnected(self, client, server):
        """Event handler for when a client connects to the server
        """
        print("[x] Client connected!")

    def _MessageReceived(self, client, server, message):
        """Event handler for when the server recieves a message from the client
        """
        print(f"[x] Message recieved: {message}")
