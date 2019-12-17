import base64
import json
import threading


class MirrorManager():

    def __init__(self, websocketServer, moduleManager):
        self.Websockets = websocketServer
        self.Modules = moduleManager

    def StartUpdatingData(self):
        self._UpdateModuleData()
        # self._UpdateModuleNotifications()

    def UpdateMirrorPage(self):
        moduleMarkup = self.Modules.GetPageMarkup()
        self.__SendMirrorPage(moduleMarkup)

    def _UpdateModuleData(self):
        modManager = self.Modules
        updateThread = threading.Thread(target=modManager.UpdatePageData)
        updateThread.daemon = True
        updateThread.start()

    def _UpdateModuleNotifications(self):
        modManager = self.Modules
        updateThread = threading.Thread(
            target=modManager.UpdatePageNotifications)
        updateThread.daemon = True
        updateThread.start()

    def __SendMirrorPage(self, data):
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
        self.Websockets.SendMessage(b64data)

    def __SendMirrorNotification(self, data):
        """[Sends the HTML markup as notifications to all clients]

        Arguments:
            data {[list]} -- [List containing all the notifications as markup]
        """
        pageData = {
            "type": "mirror_notification",
            "data": data
        }
        b64data = base64.b64encode(json.dumps(pageData).encode('utf-8'))
        self.Websockets.SendMessage(b64data)
