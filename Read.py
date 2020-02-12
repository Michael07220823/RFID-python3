# Usage: python3 Read.py 5[blocks value] 

import signal
import time
import sys
import RPi.GPIO as GPIO
from pirc522 import RFID

rdr = RFID()
util = rdr.util()
# Disable warning information.
GPIO.setwarnings(False)


print("[RFID] Detecting RFID Card...")
# Watting rfid card detect.
rdr.wait_for_tag()

# Request rfid card type
(error, data) = rdr.request()

if not error:
    # Anti-collision of rfid card.
    (error, uid) = rdr.anticoll()

    # Print rfid card uid
    rfid_uid = str()
    for numeric in uid:
        if numeric < 100:
            numeric = str(numeric)
            numeric = "0" + numeric
            rfid_uid += numeric
        else:
            numeric = str(numeric)
            rfid_uid += numeric
    print("[RFID] RFID UID: %s" % rfid_uid)


if not error:
    # Setting uid to reader.
    util.set_tag(uid)

    print("[RFID] Authorizing")
    # Authorize by auth_a key.
    util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
     
    
    if sys.argv[1] == "all":
        for i in range(64):
            rdr.wait_for_tag()
            # Request rfid card type
            (error, data) = rdr.request()

            if not error:
                # Anti-collision of rfid card.
                (error, uid) = rdr.anticoll()
            if not error:
                util.set_tag(uid)
                util.auth(rdr.auth_a, [255, 255, 255, 255, 255, 255])
                #util.auth(rdr.auth_b, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
                util.read_out(i)
    elif len(sys.argv) > 1:
        util.read_out(int(sys.argv[1]))
    else:
        # Print specify block data
        util.read_out(1)

print("[RFID] Deauthorizing")
# Deauthorize, and clean authorize state.
util.deauth()

# Clean GPIO PIN state.
rdr.cleanup()
