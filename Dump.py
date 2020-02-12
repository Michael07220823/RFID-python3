import signal
import time
import sys
import RPi.GPIO as GPIO
from pirc522 import RFID


rdr = RFID()
util = rdr.util()
# Set util debug to true - it will print what's going on
util.debug = True
# Disable warning information.
GPIO.setwarnings(False)


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
        util.auth(rdr.auth_a, [255, 255, 255, 255, 255, 255])
        
        # Dump all blocks contents.
        util.dump()

        # Clean auth state.
        util.deauth()

        # Clean GPIO PIN state.
        rdr.cleanup()
