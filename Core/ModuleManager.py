import base64
import json
import time


class ModuleDataManager():

    def __init__(self, positionManager):
        self.Position_manager = positionManager

    def StartUpdatingMirrorData(self, update_interval):
        while 1:
            self.UpdateModuleData()
            time.sleep(update_interval)

    def UpdateModuleData(self):
        mirror_modules = self.Position_manager.GetMirrorModules()
        for i in range(0, len(mirror_modules)):
            module = mirror_modules[i]
            module_data = module.GetPageData()
            if module_data is not None:
                module.BuildPageMarkup(module_data)
        self.Position_manager.SetMirrorModules(mirror_modules)

    def GetModuleData(self):
        current_module = self.Position_manager.GetCurrentModule()
        return current_module.GetPageMarkup()


class ModulePositionManager():

    def __init__(self, pages):
        """Class which provides functions to manage the modules their position and data

        Arguments:
            pages {MirrorPages array} -- array with mirror pages
        """
        self.PageCount = len(pages)
        self.PageIndex = 0

        self.Modules = []
        for i in range(0, len(pages)):
            page = pages[i]
            self.Modules.append(page)

        self.CurrentPage = self.Modules[self.PageIndex]

    def SetMirrorModules(self, modules):
        self.Modules = modules

    def GetMirrorModules(self):
        return self.Modules

    def GetCurrentModule(self):
        return self.CurrentPage

    def ZoomIn(self):
        """ Switches info on the current page. Should be bound to a zoom in gesture.
            Check the Modules/Weather.py for more info
        """
        self.CurrentPage.ZoomIn()

    def ZoomOut(self):
        """ Switches info on the current page. Should be bound to a zoom out gesture.
            Check the Modules/Weather.py for more info 
        """
        self.CurrentPage.ZoomOut()

    def NextPage(self):
        """Moves to the next page in the array
        """
        if self.PageIndex + 1 == self.PageCount:
            pass
        else:
            self.PageIndex += 1
            self.CurrentPage = self.Modules[self.PageIndex]

    def PreviousPage(self):
        """Moves to the previous page in the array
        """
        if self.PageIndex - 1 == -1:
            pass
        else:
            self.PageIndex -= 1
            self.CurrentPage = self.Modules[self.PageIndex]
