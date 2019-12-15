import base64, json
import time

class PageManager():

    # Constructor
    def __init__(self, pages):
        self.PageCount = len(pages)
        self.PageIndex = 0 

        self.Pages = []
        for i in range(0, len(pages)):
            page = pages[i]
            mirrorPage = page
            self.Pages.append(mirrorPage)
        
        self.CurrentPage = self.Pages[self.PageIndex]
        

    # Function gets called when the zoom in gesture is made
    def ZoomIn(self):
        self.CurrentPage.ZoomIn()

    # Function gets called when the zoom out gesture is made
    def ZoomOut(self):
        self.CurrentPage.ZoomOut()

    # Function gets called when we swipe right
    def NextPage(self):        
        if self.PageIndex + 1 == self.PageCount:
            pass
        else:
            self.PageIndex += 1
            self.CurrentPage = self.Pages[self.PageIndex]

    # Function gets called when we swipe left
    def PreviousPage(self):
        if self.PageIndex - 1 == -1:
            pass
        else:
            self.PageIndex -= 1
            self.CurrentPage = self.Pages[self.PageIndex]

    # Returns the HTML of the currently displayed page
    def GetPageMarkup(self):
        mirrorPage = self.CurrentPage
        return mirrorPage.GetPageMarkup()
    
    # Gets all the data from each page
    def UpdatePageData(self):
        for i in range(0, len(self.Pages)):
            self.Pages[i].BuildPageMarkup()
    
    # Updates the notifications from each page
    def UpdatePageNotifications(self):
        for i in range(0, len(self.Pages)):
            self.Pages[i].BuildPageNotification()
    
    def GetNotifications(self):
        notifications = []
        for i in range(0, len(self.Pages)):
            page_notifications = self.Pages[i].GetNotifications()
            notifications.append(page_notifications)
        
        return notifications
