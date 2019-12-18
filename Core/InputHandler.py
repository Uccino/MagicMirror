import time
import sys

__PLATFORM = sys.platform
if __PLATFORM == 'linux':
    from Core import grove_gesture_sensor


class InputHandler():

    def __init__(self, position_manager, data_manager, connection_handler):

        self.Position_manager = position_manager
        self.DataHandler = data_manager
        self.Connection_handler = connection_handler

    def GetUserInput(self):
        if sys.platform == 'linux':
            self._GetGestureInput()
        else:
            self._GetKeyboardInput()

    def _GetGestureInput(self):
        grove = grove_gesture_sensor.gesture()
        grove.init()
        while 1:
            gesture = grove.return_gesture()
            # Match the gesture
            if gesture == grove.RIGHT:
                self.Position_manager.NextPage()
                self._UpdateMirror()
            elif gesture == grove.LEFT:
                self.Position_manager.PreviousPage()
                self._UpdateMirror()
            elif gesture == grove.UP:
                self.Position_manager.ZoomIn()
                self._UpdateMirror()
            elif gesture == grove.DOWN:
                self.Position_manager.ZoomOut()
                self._UpdateMirror()
            else:
                pass
            time.sleep(.1)

    def _GetKeyboardInput(self):
        while 1:
            inputKey = input("Give input: ")

            if inputKey == 'd':

                self.Position_manager.NextPage()
                self._UpdateMirror()
            elif inputKey == 'a':

                self.Position_manager.PreviousPage()
                self._UpdateMirror()
            elif inputKey == 'w':

                self.Position_manager.ZoomIn()
                self._UpdateMirror()
            elif inputKey == 's':

                self.Position_manager.ZoomOut()
                self._UpdateMirror()
            else:
                pass
            time.sleep(.1)

    def _UpdateMirror(self):
        mirrorData = self.DataHandler.GetModuleData()
        self.Connection_handler.SendMirrorPage(mirrorData)
