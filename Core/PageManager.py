import base64, json

class PageManager():

    # Constructor
    def __init__(self, pages, websocketServer):
        self.PageCount = len(pages)
        self.PageIndex = 0 

        self.Pages = []
        for i in range(0, len(pages)):
            page = pages[i]
            mirrorPage = page
            self.Pages.append(mirrorPage)
        
        self.CurrentPage = self.Pages[self.PageIndex]
        self.WebsocketServer = websocketServer

    # Displays the page
    def DisplayMirrorPage(self):
        mirrorPage = self.CurrentPage
        pageData = mirrorPage.GetPageData()
        pageMarkup = mirrorPage.BuildPageMarkup(pageData)
        self._SendMirrorPage(pageMarkup)
    
    def _SendMirrorPage(self, data):

        pageData = {
            "type": "mirror_page",
            "data":data
        }
        b64data = base64.b64encode(json.dumps(pageData).encode('utf-8'))
        self.WebsocketServer.SendMessage(b64data)

    # Function gets called when the zoom in gesture is made
    def ZoomIn(self):
        self.CurrentPage.ZoomIn()

    # Function gets called when the zoom out gesture is made
    def ZoomOut(self):
        self.CurrentPage.ZoomOut()

    # Function gets called when we swipe right
    def NextPage(self):
        print("NextPage!")
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

    # # Gets the page data 
    # def _GetPageData(self):
    #     mirrorPage = self.CurrentPage
    #     pageData = mirrorPage.GetPageData()
    #     return pageData
    
    # # Builds the page markup
    # def _GetPageMarkup(self, pageData):
    #     mirrorPage = self.CurrentPage
    #     return mirrorPage.BuildPageMarkup(pageData)