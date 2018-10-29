from __future__ import print_function
import logging

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.INFO)

import binascii
import pygatt

import os
import sys

ADDRESS = '30:AE:A4:07:B6:26'
ADDRESS_TYPE = pygatt.BLEAddressType.random
read_characteristic = "0000ee01-0000-1000-8000-00805f9b34fb"
write_characteristic= "0000ee01-0000-1000-8000-00805f9b34fb"
notify_characteristic = "0000ee01-0000-1000-8000-00805f9b34fb"

address = ADDRESS
adapter = pygatt.GATTToolBackend(hci_device="hci1")

# def handle_data(handle, value):
#     print("Received data: %s" % hexlify(value))
adapter.start()
data = u"1234567890abcdef"
data = data.encode("ascii")

devices = adapter.scan(run_as_root=True,timeout=3)
for device in devices:
    address = device['address']

    try:
        print("connecting")
        #device = adapter.connect(address,address_type=ADDRESS_TYPE)
        device = adapter.connect(ADDRESS)
        print("connected")
        for uuid in device.discover_characteristics().keys():
            if str(uuid)=="adabfb00-6e7d-4601-bda2-bffaa68956ba":
                print("skip")
                continue
            try:
                print("Read UUID %s: %s" % (uuid,binascii.hexlify(device.char_read(uuid))))
                #device.char_write(uuid,binascii.unhexlify(data))
                device.char_write(uuid,bytearray([0x00,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xaa]))
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
        # device = adapter.connect()
        # value = device.char_read("0000ff01-0000-1000-8000-00805f9b34fb")
    #device.subscribe("0000ff01-0000-1000-8000-00805f9b34fb",callback=handle_data)

# finally
#     adapter.stop()
