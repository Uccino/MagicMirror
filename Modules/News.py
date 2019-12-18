from Modules.MirrorModule import MirrorModule
import requests


class NewsModule(MirrorModule):

    def __init__(self, mirrorConfig, htmlBuilder):

        self.NewsHost = mirrorConfig["news"]["url"]
        self.ApiSource = NewsRequester(self.NewsHost)
        self.PageBuilder = htmlBuilder
        self.PageMarkup = None

    def ZoomIn(self):
        pass

    def ZoomOut(self):
        pass

    def BuildPageMarkup(self, pageData):
        self.PageMarkup = self.PageBuilder.BuildTemplate(
            "news_page.html", pageData)

    def GetPageMarkup(self):
        return self.PageMarkup

    def BuildPageNotifications(self):
        pass

    def GetPageNotifications(self):
        pass

    def GetPageData(self):
        return self.ApiSource.GetNews()


class NewsRequester():

    def __init__(self, url):
        self.Url = url

    # Gets the latest news from the webserver
    def GetNews(self):
        try:
            response = requests.get(self.Url)
            if response.status_code == 200:
                responseData = response.json()
                return responseData
            else:
                return None
        except Exception as generalException:
            return None
