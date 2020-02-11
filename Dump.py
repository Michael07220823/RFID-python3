#!/usr/bin/env python

import signal
import time
import sys
from pirc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
# Set util debug to true - it will print what's going on
util.debug = True

def end_read(signal,frame):
    print("\n[RFID] Ctrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

while run:
    print("\n[RFID] Start detect:")
    # Wait for tag
    rdr.wait_for_tag()

    # Request tag
    (error, data) = rdr.request()
    if not error:
        print("[RFID] Detected")

        (error, uid) = rdr.anticoll()
        if not error:
            # Print UID
            print("[RFID] Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

            # Set tag as used in util. This will call RFID.select_tag(uid)
            util.set_tag(uid)

            # Authenticate by key-a
            util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
            
            # Dump all blocks contents.
            util.dump()

            # Clean auth state.
            util.deauth()

            time.sleep(1)
