from abc import ABC, abstractmethod


class MirrorModule(ABC):

    @abstractmethod
    # Your page constructor should accept neccecary information
    # for the page requester to run properly.
    # It should also accept a htmlbuilder.
    def __init__(self):
        pass

    @abstractmethod
    def ZoomIn(self):
        pass

    @abstractmethod
    def ZoomOut(self):
        pass

    @abstractmethod
    def GetPageData(self):
        pass

    @abstractmethod
    def BuildPageMarkup(self):
        pass

    @abstractmethod
    def GetPageMarkup(self):
        pass

    @abstractmethod
    def BuildPageNotifications(self):
        pass

    @abstractmethod
    def GetPageNotifications(self):
        pass
