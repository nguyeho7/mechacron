from __future__ import print_function
from decepticalls.Decepticall import Decepticall
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from dateutil import parser
import datetime

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json

class Googletron(Decepticall):

    def __get_credentials__(self):
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'Mechacron'
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Shamelessly stolen from the google calendar API quickstart
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def __get_events__(self, weekly: bool) -> str:
        credentials = self.__get_credentials__()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        current = datetime.datetime.utcnow()
        now = current.isoformat() + 'Z'# 'Z' indicates UTC time
        if weekly:
            limit = (current + datetime.timedelta(weeks=7)).isoformat() + 'Z'
        else:
            limit = datetime.datetime(current.year, current.month, current.day, 0,0).isoformat() +'Z'
        eventsResult = service.events().list(
                calendarId='primary', timeMin=now, timeMax=limit, maxResults=10, singleEvents=True,
                orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        return events

    def __format_events__(self, events, timeformat):
        result = []
        if not events:
            return ""
        for event in events:
            name = event['summary']
            date = parser.parse(event['start']['dateTime'])
            time = date.strftime(timeformat)
            result.append("{}\n{}".format(time, name))
        return "\n\n".join(result)

    def daily_report(self):
        events = self.__get_events__(weekly=False)
        return self.__format_events__(events, "%H:%M")


    def weekly_report(self):
        events = self.__get_events__(weekly=True)
        return self.__format_events__(events, "%A %H:%M")

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    current = datetime.datetime.utcnow()
    now = current.isoformat() + 'Z'# 'Z' indicates UTC time
    week = (current + datetime.timedelta(weeks=7)).isoformat() + 'Z'

    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, timeMax=week, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

