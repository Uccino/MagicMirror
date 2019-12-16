from Modules.MirrorModule import MirrorModule
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dateutil import parser
import os.path
import datetime
import pickle


class CalendarModule(MirrorModule):
    def __init__(self, mirrorConfig, pageBuilder):
        self.ApiSource = CalendarRequester()
        self.PageBuilder = pageBuilder
        self.PageMarkup = None
        self.PageData = None
        self.PageNotifications = []
    
    def ZoomIn(self):
        pass

    def ZoomOut(self):
        pass

    def BuildPageMarkup(self):
        pageData = self.GetPageData()
        self.PageMarkup = self.PageBuilder.BuildTemplate("calendar_page.html", pageData)

    def GetPageMarkup(self):
        return self.PageMarkup

    def GetPageData(self):
        self.PageData = self.ApiSource.GetEvents(10)
        return self.PageData
    
    def BuildPageNotifications(self):
        self.PageNotifications = []
        upcommingEvents = self._GetUpcommingEvents()
        for i in range(0, len(upcommingEvents)):
            event = upcommingEvents[i]            
            eventDate = parser.parse(event["start_date"]).date()
            nowDate = datetime.datetime.now().date()
            timeDelta = eventDate - nowDate

            eventSummary = event["summary"]

            event_notification = f"{eventSummary} is in {timeDelta.days} days!"
            self.PageNotifications.append(event_notification)
        
    def GetPageNotifications(self):
        notifications = []
        for i in range(0, len(self.PageNotifications)):
            notification = self.PageNotifications[i]
            notifications.append(f"<p> {notification} </p>")
        return notifications
    
    def _GetUpcommingEvents(self):
        """Parses the current events to check if there are any within 11 days
        
        Returns:

            [list] -- [List of upcomming events]

        """        
        upcomingEvents = []
        dateNow = datetime.datetime.utcnow()        
        for i in range(0, len(self.PageData)):
            eventDate = self.PageData[i]['start_date']
            eventDateTime = parser.parse(eventDate)
            if dateNow.date() + datetime.timedelta(days=11) >= eventDateTime.date():
                upcomingEvents.append(self.PageData[i])        
        return upcomingEvents

class CalendarRequester():
    def __init__(self):
        self.CalendarApi = self.InitializeApi()

    def InitializeApi(self):
        """[Initializes the google calendar API]
        
        Raises:
            Exception: [Raises if the config.json wasn't found]
        
        Returns:

            [Resource] -- [Google calendar API]
        """        
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = None

        # Check if there already is an authentication token
        if os.path.exists("./token.pickle"):
            with open("./token.pickle", 'rb') as token:
                creds = pickle.load(token)

        if not os.path.exists("./config.json"):
            raise Exception("Unable to find config.json")
        
        # If the credentials are not valid, ask for new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "./config.json",
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open('./token.pickle','wb') as token:
                pickle.dump(creds, token)       
        service = build('calendar', 'v3', credentials=creds)
        return service

    def GetEvents(self, amount):
        """Gets the next x events
        
        Arguments:
            amount int -- amount of events to return
        
        Returns:
            Dictionary -- dictionary of events
        """        
        now = datetime.datetime.utcnow().isoformat() + 'Z' # Get UTC time
        events_results = self.CalendarApi.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=amount, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_results.get('items', [])
        if not events:
            return None
        else:
            return self._ParseEventData(events)
    
    def _ParseEventData(self, data):
        """Parses the events for their summary and start_date
        
        Arguments:
            data dictionary -- dictionary which contains events
        
        Returns:
            [type] -- [description]
        """        
        events = []
        for i in range(0, len(data)):
            eventStart = data[i]["start"]
            if "dateTime" in eventStart:
                start = self._GetDateTime(data[i]["start"]["dateTime"])               
            else:
                start = data[i]["start"]["date"]
            event = {
                    "summary": data[i]["summary"],
                    "start_date": start
                }
            events.append(event)
        return events
    
    def _GetDateTime(self, dateFormat):
        """Formats the datetime
        
        Arguments:
            dateFormat string -- string which contains a datetime
        
        Returns:
            str -- String formatted datetime
        """        
        dateTimeObject = parser.parse(dateFormat)
        dateTimeString = dateTimeObject.strftime('%Y-%m-%d, %H:%M')
        return dateTimeString