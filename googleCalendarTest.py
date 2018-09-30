from __future__ import print_function
import httplib2
import os

import datetime
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES ='https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SCOPE_FILE = 'client_secret.json'
APPLICATION_NAME = 'Study# google API test'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SCOPE_FILE, SCOPES)
        flow.user_agent=APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow,store,flags)
        else:
            credentials = tools.run(flow,store)
        print('Storing credentials to '+credential_path)
    return credentials

def main():
    path = 'data/src/'
    fr=open((path+'report.txt'),mode='r+')
    ft=open((path+'test.txt'),mode='r+')
    fg=open((path+'goods.txt'),mode='r+')
    fe=open((path+'allevent.txt'),mode='r+')


    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service=discovery.build('calendar','v3',http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Getting the upcoming 20 events')
    eventsResult = service.events().list(
        calendarId='primary',timeMin=now,maxResults=20,singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items',[])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime',event['start'].get('date'))
        str = event['summary']
        if(str[0:2]=='SS'):
            print(start,str[6:])
            fr.writeines(start,str)

    fr.close()
    ft.close()
    fg.close()
    fe.close()

def string2datetime(str_time):
    int_year = int(str_time[0:4])
    int_month= int(str_time[5:7])
    int_day  = int(str_time[8:10])
    int_hour = int(str_time[11:13])
    int_min  = int(str_time[14:16])
    int_sec  = int(str_time[17:19])
    dt_time  = datetime.datetime(int_year,int_month,int_day,int_hour,int_min,int_sec,int_sec)

def deleteOldEvent():
    return

def addNewEvent():
    return

def updateEvent():
    return

if __name__ =='__main__':
    main()
