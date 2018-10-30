from __future__ import print_function
import logging
# logging.basicConfig()
# logging.getLogger('pygatt').setLevel(logging.ERROR)
import time
import binascii
import pygatt
import os
import sys

ADDRESS_TYPE = pygatt.BLEAddressType.random

class espServer:
    address = '30:AE:A4:07:B6:26'
    read_characteristic = "00000c19-0000-1000-8000-00805f9b34fb"
    write_characteristic= "00000c19-0000-1000-8000-00805f9b34fb"
    notify_characteristic = "00000c19-0000-1000-8000-00805f9b34fb"

    def __init__(self,addr,uuid):
        self.address = addr
        self.read_characteristic = uuid
        self.write_characteristic = uuid
        self.notify_characteristic = uuid

        self.adapter = pygatt.GATTToolBackend(hci_device="hci1")

        self.adapter.start()
        self.device = self.adapter.connect(self.address)

    def scan(self,timeout=3):
        return
        # for device in .self.devices:
        #     address = device['address']
        #
        #     try:
        #         print("connecting")
        #         device = adapter.connect(ADDRESS)
        # device.char_write(write_characteristic,bytearray("world"))
        #         # time.sleep(0.1)
        #         # getstr = device.char_read(read_characteristic)
        #         for uuid in device.discover_characteristics().keys():
        #             print(uuid)
        #             if(str(uuid)==read_characteristic):
        #                 try:
        #                     sendstr = "hello"
        #                     device.char_write(uuid,bytearray(sendstr))
        #                     print("char_write  \"%s\"" % sendstr)
        #                     time.sleep(1)
        #                 except:
        #                     continue
        #                 else:
        #                     break
        #         device.disconnect()
        #     except pygatt.exceptions.NotConnectedError:
        #         print("failed to connect to %s" % address)
        #         continue
        #     else:
        #         break
        # else: #for
        #     print("failed to connect and read from any device")
        #     sys.exit(1)
    def write(self,words):
        self.device.char_write(self.write_characteristic,bytearray(words))
        print("char_write  \"%s\"" % words)
        time.sleep(0.1)


    def read(self):
        getstr = self.device.char_read(self.read_characteristic)
        print("char_read   \"", end='')

        for word in getstr:
            print(chr(word), end='')
        print("\"")

        return getstr

if __name__ == '__main__':
    server = espServer('30:AE:A4:07:B6:26',"00000c19-0000-1000-8000-00805f9b34fb")
    # server.scan()
    server.write("takepi!")
    reading = server.read()
