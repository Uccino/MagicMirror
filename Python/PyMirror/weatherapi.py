import requests
from datetime import datetime


class OpenWeatherMap():

    def __init__(self, api_key, language, latitude, longitude, locationName):
        self.ApiKey = api_key
        self.Language = language
        self.Lat = latitude
        self.Long = longitude
        self.Name = locationName

        self.ContactUrl = self._BuildUrl(api_key)

    # Gets the weather forecast
    def GetWeatherInfo(self):
        contactUrl = self.ContactUrl
        try:
            response = requests.get(contactUrl)
            if response.status_code == 200:
                responseData = response.json()
                return responseData
            else:
                return None
        except Exception as generalException:
            print("[!] Undefined error!")
            print(generalException)
            return None

    # Parses the weather forecast to get the current weather
    def GetCurrentWeatherForecast(self, weatherInfo):
        currentForecast = weatherInfo["currently"]        
        forecastDict = {
            "location": self.Name,
            "summary": currentForecast["summary"],
            "temperature": currentForecast["temperature"],
            "icon": currentForecast["icon"]
        }
        forecast = {
            "data": forecastDict
        }
        return forecast

    # Parses the weather forecast to get the hourly forecast for the next day
    def GetHourlyWeatherForecast(self, weatherInfo):
        hourlyForecast = weatherInfo["hourly"]["data"]
        forecastList = []
        for i in range(0, 13):
            forecastHour = self._ConvertUnixToDate(hourlyForecast[i]["time"])
            forecast = {
                    "time": forecastHour,
                    "summary": hourlyForecast[i]["summary"],
                    "temperature": hourlyForecast[i]["temperature"]
                }
        
            forecastList.append(forecast)
        hourlyForecastDict = {"data": forecastList}
        return hourlyForecastDict

    # Parses the weather forecast to get the daily forecast
    def GetDailyForecast(self, weatherInfo):
        pass

    # Converts the unix timestamp to human readable datetime
    def _ConvertUnixToDate(self, unixTime):
        timestamp = datetime.fromtimestamp(unixTime)
        hour = timestamp.hour 
        return hour

    # Builds the request url
    def _BuildUrl(self, apiKEy):
        url = f'https://api.darksky.net/forecast/{apiKEy}/{self.Lat},{self.Long}?lang={self.Language}&units=si'
        return url
