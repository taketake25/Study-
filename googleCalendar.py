# coding: utf-8
from __future__ import print_function
import httplib2
import os
from pykakasi import kakasi
import mojimoji

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

class googleCalendar:
    SCOPES ='https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SCOPE_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Study# google API test'
    filePath="data/src/"

    def __init__(self,path):
        self.filePath=path
        self.initFiles()
        #google API init
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar','v3',http=http)
        return

    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SCOPE_FILE, self.SCOPES)
            flow.user_agent=self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow,store,flags)
            else:
                credentials = tools.run(flow,store)
            print('Storing credentials to '+credential_path)
        return credentials

    def loadAllSchedules(self):
        path = self.filePath

        now = datetime.datetime.utcnow().isoformat() + 'Z'

        print('Loading the upcoming 40 events')
        eventsResult = self.service.events().list(
            calendarId='primary',timeMin=now,maxResults=40,singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items',[])

        if not events:
            print('No upcoming events found.')

        self.addNewEvent(events)

    def string2datetime(self,str_time):
        int_year = int(str_time[0:4])
        int_month= int(str_time[5:7])
        int_day  = int(str_time[8:10])
        int_hour = int(str_time[11:13])
        int_min  = int(str_time[14:16])
        int_sec  = int(str_time[17:19])
        dt_time  = datetime.datetime(int_year,int_month,int_day,int_hour,int_min,int_sec,int_sec)
        return dt_time

    def initFiles(self):
        path = self.filePath
        try:
            with open((path+'report.txt'),mode='r'):
                pass
            with open((path+'test.txt'),mode='r'):
                pass
            with open((path+'goods.txt'),mode='r'):
                pass
            with open((path+'event.txt'),mode='r'):
                pass
            with open((path+'allevent.txt'),mode='r'):
                pass
            with open((path+'kanaevent.txt'),mode='r'):
                pass
        except IOError as e:
            with open((path+'report.txt'),mode='w'):
                pass
            with open((path+'test.txt'),mode='w'):
                pass
            with open((path+'goods.txt'),mode='w'):
                pass
            with open((path+'event.txt'),mode='w'):
                pass
            with open((path+'allevent.txt'),mode='w'):
                pass
            with open((path+'kanaevent.txt'),mode='w'):
                pass
        return

    def deleteOldEvent(self):
        return

    def addNewEvent(self,events):
        path = self.filePath
        with open((path+"report.txt")) as fr:
            lr=fr.readlines()
        with open((path+"test.txt")) as ft:
            lt=ft.readlines()
        with open((path+"goods.txt")) as fg:
            lg=fg.readlines()
        with open((path+"event.txt")) as fe:
            le=fe.readlines()
        with open((path+"allevent.txt")) as fa:
            la=fa.readlines()
        with open((path+"kanaevent.txt")) as fk:
            # lk=fk.readlines()
            lk=[]

        fr=open((path+'report.txt'),mode='w')
        ft=open((path+'test.txt'),mode='w')
        fg=open((path+'goods.txt'),mode='w')
        fe=open((path+'event.txt'),mode='w')
        fa=open((path+'allevent.txt'),mode='w')
        fk=open((path+'kanaevent.txt'),mode='w')

        for event in events:
            start = event['start'].get('dateTime',event['start'].get('date'))
            eventName = event['summary'].encode('utf-8')
            dates = self.string2datetime(start)
            eventTime = "{:04d}{:02d}{:02d}{:02d}".format(dates.year,dates.month,dates.day,dates.hour)

            if(eventName[0:2]=='SS'):
                flag = True
                for word in la:
                    if(eventTime==word[0:10] and eventName[6:]==word[16:-1]):
                    # if(eventName[6:]==word[16:-1]):
                        flag = False
                        break
                if(not flag):
                    continue

                kks = kakasi()
                kks.setMode('H','K')
                # kks.setMode('K','K')
                kks.setMode("J","K")
                conv = kks.getConverter()
                onlyKana = conv.do(eventName[6:].decode('utf-8'))
                onlyKana = mojimoji.zen_to_han(onlyKana)

                onlyKana = onlyKana.encode('utf-8')

                la.insert(0,eventTime+","+eventName[2:6]+","+eventName[6:]+'\n') #write all events
                # lk.insert(0,eventTime+","+eventName[2:6]+","+onlyKana+'\n') #write all events in Kana
                if(eventName[2]=='R'):
                    print(start, "report" ,onlyKana)
                    # lr.insert(0,eventTime+","+eventName[6:]+'\n')
                    lk.insert(0,'r'+eventTime+","+onlyKana+'\n') #write all events in Kana
                    lr.insert(0,eventTime+","+onlyKana+'\n')
                if(eventName[3]=='T'):
                    print(start, "test  " ,onlyKana)
                    # lt.insert(0,eventTime+","+eventName[6:]+'\n')
                    lk.insert(0,'t'+eventTime+","+onlyKana+'\n') #write all events in Kana
                    lt.insert(0,eventTime+","+onlyKana+'\n')
                if(eventName[4]=='G'):
                    print(start, "goods " ,onlyKana)
                    # lg.insert(0,eventTime+","+eventName[6:]+'\n')
                    lk.insert(0,'g'+eventTime+","+onlyKana+'\n') #write all events in Kana
                    lg.insert(0,eventTime+","+onlyKana+'\n')
                if(eventName[5]=='E'):
                    print(start, "event " ,onlyKana)
                    # le.insert(0,eventTime+","+eventName[6:]+'\n')
                    lk.insert(0,'e'+eventTime+","+onlyKana+'\n') #write all events in Kana
                    le.insert(0,eventTime+","+onlyKana+'\n')

        fr.writelines(lr)
        ft.writelines(lt)
        fg.writelines(lg)
        fe.writelines(le)
        fa.writelines(la)
        fk.writelines(lk)
        fr.close()
        ft.close()
        fg.close()
        fe.close()
        fa.close()
        fk.close()

    def updateEvent(self):
        return

    def getEvent(self,kind):
        path = self.filePath
        if(kind=='r'):
            with open((path+"report.txt")) as f:
                l=f.readlines()
        elif(kind=='t'):
            with open((path+"test.txt")) as f:
                l=f.readlines()
        elif(kind=='g'):
            with open((path+"goods.txt")) as f:
                l=f.readlines()
        elif(kind=='e'):
            with open((path+"event.txt")) as f:
                l=f.readlines()
        elif(kind=='a'):
            with open((path+"kanaevent.txt")) as f:
                l=f.readlines()

        else:
            l=0

        return l


if __name__ =='__main__':
    #make files
    path = 'data/src/'

    calendar = googleCalendar(path)
    calendar.loadAllSchedules()

    print("report")
    schedules = calendar.getEvent('r')
    for word in schedules:
        print(word[:-1])

    print("test")
    schedules = calendar.getEvent('t')
    for word in schedules:
        print(bytearray(word[:-1]))

    print("goods")
    schedules = calendar.getEvent('g')
    for word in schedules:
        print(word[:-1])

    print("event")
    schedules = calendar.getEvent('e')
    for word in schedules:
        print(word[:-1])
