from Core import grove_gesture_sensor
import time

class InputHandler():

    def __init__(self, moduleManager, mirrorManager):
        self.Grove = grove_gesture_sensor.gesture()
        self.Grove.init()
        self.ModuleManager = moduleManager
        self.MirrorManager = mirrorManager

    def GetGestureInput(self):
        while 1:
            gesture = self.Grove.return_gesture()
            
            #Match the gesture           
            if gesture==self.Grove.RIGHT:
                self.ModuleManager.NextPage()
                self._UpdateMirror()
            elif gesture==self.Grove.LEFT:
                self.ModuleManager.PreviousPage()
                self._UpdateMirror()
            elif gesture==self.Grove.UP:
                self.ModuleManager.ZoomIn()
                self._UpdateMirror()
            elif gesture==self.Grove.DOWN:
                self.ModuleManager.ZoomOut()
                self._UpdateMirror()
            else:
                print("Unused gesture")
            
            time.sleep(.1)
    
    def _UpdateMirror(self):
        self.MirrorManager.UpdateMirrorPage()