from websocket_server import WebsocketServer as wsServer
import base64
import json


class MirrorConnectionHandler():
    def __init__(self, websocketServer):
        if websocketServer.IsRunning():
            self.SocketServer = websocketServer
        else:
            raise Exception(
                "Mirror connection is not running. Make sure that you start the websocket server before creating a MirrorConnection")

    def SendMirrorPage(self, data):
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
        self.SocketServer.SendMessage(b64data)

    def SendMirrorNotifications(self, data):
        """[Sends the HTML markup as a mirror page to all clients]

        Arguments:

            websocketServer {[WebsocketServer]} -- [Websocket server with the clients]
            data {[str]} -- [HTML markup to be send to the mirror]
        """
        pageData = {
            "type": "mirror_notification",
            "data": data
        }
        b64data = base64.b64encode(json.dumps(pageData).encode('utf-8'))
        self.SocketServer.SendMessage(b64data)


class WebSocketServer():
    def __init__(self, ip, port):
        self.ServerIp = ip
        self.ServerPort = port
        self.Server = wsServer(port, ip)
        self.SetupServer()
        self.Running = False

    def IsRunning(self):
        return self.Running

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
            self.Running = True
            self.Server.run_forever()
        except BaseException:
            print("[!] Unable to run the server.")

    def SendMessage(self, data):
        """Sends a message to all clients

        Arguments:
            data {String} -- [String of text to be send]
        """
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
