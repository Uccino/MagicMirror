
import requests

class NewsPage():

    def __init__(self, mirrorConfig, htmlBuilder):

        self.NewsHost = mirrorConfig["news"]["url"]
        self.ApiSource = NewsRequester(self.NewsHost)
        self.PageBuilder = htmlBuilder

    def ZoomIn(self):
        pass
    
    def ZoomOut(self):
        pass
    
    def GetPageData(self):        
        return self.ApiSource.GetNews()

    def BuildPageMarkup(self, data):
        return self.PageBuilder.BuildTemplate("news_page.html", data)

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