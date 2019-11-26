import requests

class NewsRequester():

    def __init__(self, amount, ip, port):
        self.Amount = amount
        self.Host = ip
        self.Port = port
    
    def GetNews(self):
        url = self._BuildUrl()
        try:
            response = requests.get(url)
            if response.status_code == 200:
                responseData = response.json()
                return responseData
            else:
                return None
        except Exception as generalException:        
            return None
    
    def _BuildUrl(self):
        contactUrl = f"http://{self.Host}:{self.Port}/getnews"
