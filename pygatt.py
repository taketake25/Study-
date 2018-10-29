from __future__ import print_function
import logging

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.ERROR)

import time
import binascii
import pygatt
import os
import sys

ADDRESS = '30:AE:A4:07:B6:26'
ADDRESS_TYPE = pygatt.BLEAddressType.random
read_characteristic = "00000c19-0000-1000-8000-00805f9b34fb"
write_characteristic= "00000c19-0000-1000-8000-00805f9b34fb"
notify_characteristic = "00000c19-0000-1000-8000-00805f9b34fb"

address = ADDRESS
adapter = pygatt.GATTToolBackend(hci_device="hci1")

adapter.start()

devices = adapter.scan(run_as_root=True,timeout=3)
for device in devices:
    address = device['address']

    try:
        print("connecting")
        device = adapter.connect(ADDRESS)


        # device.char_write(write_characteristic,bytearray("world"))
        # time.sleep(0.1)
        # getstr = device.char_read(read_characteristic)


        for uuid in device.discover_characteristics().keys():
            print(uuid)
            if(str(uuid)==read_characteristic):
                try:
                    sendstr = "hello"
                    device.char_write(uuid,bytearray(sendstr))
                    print("char_write  \"%s\"" % sendstr)
                    time.sleep(1)

                    getstr = device.char_read(uuid)
                    print("char_read  \"", end='')

                    for word in getstr:
                        print(chr(word), end='')
                    print("\"")

                except:
                    continue
                else:
                    break

        device.disconnect()

    except pygatt.exceptions.NotConnectedError:
        print("failed to connect to %s" % address)
        continue
    else:
        break
else:
    print("failed to connect and read from any device")
    sys.exit(1)
