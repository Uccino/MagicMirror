import base64
import json
import time


class PageManager():

    def __init__(self, pages):
        """Class which provides functions to manage the modules their position and data

        Arguments:
            pages {MirrorPages array} -- array with mirror pages
        """
        self.PageCount = len(pages)
        self.PageIndex = 0

        self.Pages = []
        for i in range(0, len(pages)):
            page = pages[i]
            mirrorPage = page
            self.Pages.append(mirrorPage)

        self.CurrentPage = self.Pages[self.PageIndex]

    def ZoomIn(self):
        """ Switches info on the current page. Should be bound to a zoom in gesture.
            Check the Modules/Weather.py for more info


        Returns:
        [None]
        """
        self.CurrentPage.ZoomIn()

    def ZoomOut(self):
        """ Switches info on the current page. Should be bound to a zoom out gesture.
            Check the Modules/Weather.py for more info


        Returns:
        [None]
        """
        self.CurrentPage.ZoomOut()

    def NextPage(self):
        """Moves to the next page in the array
        """
        if self.PageIndex + 1 == self.PageCount:
            pass
        else:
            self.PageIndex += 1
            self.CurrentPage = self.Pages[self.PageIndex]

    def PreviousPage(self):
        """Moves to the previous page in the array
        """
        if self.PageIndex - 1 == -1:
            pass
        else:
            self.PageIndex -= 1
            self.CurrentPage = self.Pages[self.PageIndex]

    def GetPageMarkup(self):
        """Gets the current mirror page's HTML markup

        Returns:
            String -- HTML markup of the page
        """
        mirrorPage = self.CurrentPage
        return mirrorPage.GetPageMarkup()

    def UpdatePageData(self):
        """Updates all the data in the mirror pages
        """
        for i in range(0, len(self.Pages)):
            self.Pages[i].BuildPageMarkup()

    def UpdatePageNotifications(self):
        """Updates all the notifications in the mirror pages
        """
        for i in range(0, len(self.Pages)):
            self.Pages[i].BuildPageNotification()

    def GetNotifications(self):
        """Gets all the notifications from the loaded pages

        Returns:
            [String array] -- [HTML markup of the notifications]
        """
        notifications = []
        for i in range(0, len(self.Pages)):
            page_notifications = self.Pages[i].GetNotifications()
            notifications.append(page_notifications)

        return notifications
