import googleCalendar as gct
import studygatt as sg
import time


def cvtString(event):
    c=0
    count=0
    # send=""
    send=event[4:8]+" "
    for chara in event[11:-1]:
        count+=1
        i=ord(chara)
        # print("%d"%i),
        if(count==1):
            if(i>=32 and i<=127):
                count=0
                send=send+chara
                c=0
            elif(i==239):
                send=send+chr(127)
                c=0
        else:
            if(i==190 and count==2):
                c+=64
            elif(i==189 and count==2):
                c+=0
            else:
                c+=i
                # print("%d"%(c-127))
                send=send+chr(c-127)
                c=0
                count=0
    return send


def sendTextData(schedule):
    for event in schedules:
        send=cvtString(event)
        print(bytearray(event[11:-1])),
        if len(send) > 20:
            esp1.write(bytearray(send[:19]+'%'))
            esp1.write(bytearray(send[19:]))
        else:
            esp1.write(bytearray(send))


def sendAllNewData(schedule):
    for event in schedules:
        if event[0]=='r':
            esp1.write(bytearray('r'))
        elif event[0]=='t':
            esp1.write(bytearray('t'))
        elif event[0]=='g':
            esp1.write(bytearray('g'))
        elif event[0]=='e':
            esp1.write(bytearray('e'))

        send=cvtString(event[1:])
        print(bytearray(event[12:-1])),
        if len(send) > 20:
            esp1.write(bytearray(send[:19]+'%'))
            esp1.write(bytearray(send[19:]))
        else:
            esp1.write(bytearray(send))


if __name__=="__main__":
    path='data/src/'
    # esp1 = sg.espServer("30:AE:A4:07:B6:26","00000c19-0000-1000-8000-00805f9b34fb")
    esp1 = sg.espServer("30:AE:A4:CA:F0:02","00000c19-0000-1000-8000-00805f9b34fb")
    calendar = gct.googleCalendar(path)
    calendar.loadAllSchedules()

    # schedules = calendar.getEvent('r')
    # esp1.write(bytearray('r'))
    # sendTextData(schedules)
    #
    # schedules = calendar.getEvent('t')
    # esp1.write(bytearray('t'))
    # sendTextData(schedules)
    #
    # schedules = calendar.getEvent('g')
    # esp1.write(bytearray('g'))
    # sendTextData(schedules)
    #
    # schedules = calendar.getEvent('e')
    # esp1.write(bytearray('e'))
    # sendTextData(schedules)

    schedules = calendar.getEvent('a')
    sendAllNewData(schedules)


    reading = esp1.read()
