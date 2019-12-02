from datetime import datetime
from Modules.MirrorPage import MirrorPage
from enum import Enum
import requests

class WeatherPage(MirrorPage):
    
    class Page(Enum):
        Hourly = 0
        Daily = 1
        Weekly = 2

    def __init__(self, mirrorConfig, htmlBuilder):

        self.ApiKey = mirrorConfig["weather"]["key"]
        self.Language = mirrorConfig["weather"]["language"]
        self.LocName = mirrorConfig["weather"]["location"]["name"]
        self.LocLatitude = mirrorConfig["weather"]["location"]["latitude"]
        self.LocLongitude = mirrorConfig["weather"]["location"]["longitude"]

        self.ApiSource = DarkSkyWeather(self.ApiKey, self.Language,self.LocLatitude, self.LocLongitude, self.LocName)
        self.CurrentPage = self.Page.Weekly
        self.PageBuilder = htmlBuilder

    def ZoomIn(self):
        if self.currentPage == self.Page.Daily:
            self.currentPage = self.Page.Hourly            
        elif self.currentPage == self.Page.Weekly:
            self.currentPage = self.Page.Daily           
        elif self.currentPage == self.Page.Hourly:
            pass  
        
    def ZoomOut(self):
        if self.currentPage == self.Page.Daily:
            self.currentPage = self.Page.Weekly            
        elif self.currentPage == self.Page.Weekly:
            pass
        elif self.currentPage ==self. Page.Hourly:
            self.currentPage = self.Page.Daily
    
    def GetPageData(self):
        weatherInfo = self.ApiSource.GetWeatherInfo()
        if self.CurrentPage == self.Page.Daily:
            return self.ApiSource.GetCurrentWeatherForecast(weatherInfo)
        elif self.CurrentPage == self.Page.Weekly:
            return self.ApiSource.GetDailyForecast(weatherInfo)
        elif self.CurrentPage == self.Page.Hourly:
            return self.ApiSource.GetHourlyWeatherForecast(weatherInfo)

    def BuildPageMarkup(self, pageData):
        if self.CurrentPage == self.Page.Hourly:
            return self.PageBuilder.BuildTemplate("weather_hourly.html", pageData)
        elif self.CurrentPage == self.Page.Daily:
            return self.PageBuilder.BuildTemplate("weather_daily.html", pageData)
        elif self.CurrentPage == self.Page.Weekly:
            return self.PageBuilder.BuildTemplate("weather_weekly.html", pageData)

class DarkSkyWeather():    

    # Constructor
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
            "icon": self._GetWeatherIcon(self.currentForecast["icon"])
        }
        forecast = {
            "location": self.Name,
            "data": forecastDict
        }
        return forecast

    # Parses the weather forecast to get the hourly forecast for the next day
    def GetHourlyWeatherForecast(self, weatherInfo):
        hourlyForecast = weatherInfo["hourly"]["data"]
        forecastList = []
        for i in range(0, 13):
            forecastHour = self._GetHourFromUnixDate(hourlyForecast[i]["time"])
            forecast = {
                    "time": forecastHour,
                    "icon": self._GetWeatherIcon(hourlyForecast[i]["icon"]),
                    "temperature": hourlyForecast[i]["temperature"]
                }
        
            forecastList.append(forecast)
        forecast = {
            "location": self.Name,
            "data":forecastList
            }
        return forecast

    # Parses the weather forecast to get the daily forecast
    def GetDailyForecast(self, weatherInfo):
        dailyForecast = weatherInfo["daily"]["data"]
        forecastList = []
        for i in range(0,7):
            forecastTimeStamp = self._GetDateFromUnixStamp(dailyForecast[i]["time"])
            weekString = self._GetDayNameFromDate(forecastTimeStamp)
            forecast = {
                "day":weekString,
                "minTemp": dailyForecast[i]["temperatureMin"],
                "maxTemp": dailyForecast[i]["temperatureMax"],
                "icon": self._GetWeatherIcon(dailyForecast[i]["icon"])
            }
            forecastList.append(forecast)
        forecast = {
            "location": self.Name,
            "data": forecastList
        }
        return forecast

    # Converts the unix timestamp to human readable datetime
    def _GetHourFromUnixDate(self, unixTime):
        timestamp = datetime.fromtimestamp(unixTime)
        hour = timestamp.hour 
        return hour
    
    # Converts the unix timestamp to a day ( 1 - 31 )
    def _GetDateFromUnixStamp(self, unixTime):
        timestamp = datetime.fromtimestamp(unixTime)
        return timestamp

    # Returns the weekday as a string given a timestamp
    def _GetDayNameFromDate(self, timestamp):
        if(type(timestamp) == datetime):
            return timestamp.strftime("%a")
        else:
            raise ValueError("Timestamp given was not in the correct format")

    # Returns a font awesome weather icon based on the current condition
    def _GetWeatherIcon(self, condition):
        if condition == "clear-day":
            return "wi-day-sunny"
        elif condition == "clear-night":
            return "wi-night-clear"
        elif condition == "rain":
            return "wi-day-rain"
        elif condition == "snow":
            return "wi-day-snow"
        elif condition == "sleet":
            return "wi-day-sleet"
        elif condition == "wind":
            return "wi-day-windy"
        elif condition == "fog":
            return "wi-fog"
        elif condition == "cloudy":
            return "wi-cloudy"
        elif condition =="partly-cloudy-day":
            return "wi-day-cloudy"
        elif condition == "partly-cloudy-night":
            return "wi-night-alt-cloudy"
        else:
            return "wi-alien"

    # Builds the request url
    def _BuildUrl(self, apiKey):
        url = f'https://api.darksky.net/forecast/{apiKey}/{self.Lat},{self.Long}?lang={self.Language}&units=si'
        return url