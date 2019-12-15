from Modules.MirrorPage import MirrorPage
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dateutil import parser
import datetime
import pickle
import os.path

class CalendarPage(MirrorPage):
    def __init__(self, mirrorConfig, pageBuilder):
        self.ApiSource = CalendarRequester()
        self.PageBuilder = pageBuilder
        self.PageMarkup = None
    
    def BuildPageMarkup(self):
        pageData = self.GetPageData()
        self.PageMarkup = self.PageBuilder.BuildTemplate("calendar_page.html", pageData)

    def GetPageMarkup(self):
        return self.PageMarkup

    def ZoomIn(self):
        pass

    def ZoomOut(self):
        pass

    def GetPageData(self):
        return self.ApiSource.GetEvents(10)
    
class CalendarRequester():
    def __init__(self):
        self.CalendarApi = self.InitializeApi()

    def InitializeApi(self):
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
        dateTimeObject = parser.parse(dateFormat)
        dateTimeString = dateTimeObject.strftime('%Y-%m-%d, %H:%M')
        return dateTimeString