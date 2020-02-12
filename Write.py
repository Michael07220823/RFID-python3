import signal
import time
import sys
import RPi.GPIO as GPIO
from pirc522 import RFID

rdr = RFID()
util = rdr.util()
# Disable warning information.
GPIO.setwarnings(False)

def write_to_block(block=int(), data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]):
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
        util.auth(rdr.auth_a, [255, 255, 255, 255, 255, 255])

        # Print specify block data
        util.read_out(block)

        # Wrute data to rfid card
        rdr.write(block, data)

        # Print specify block data
        util.read_out(block)
        
    print("[RFID] Deauthorizing")
    # Deauthorize, and clean authorize state.
    util.deauth()

    # Clean GPIO PIN state.
    rdr.cleanup()
    
if __name__ == "__main__":
    write_to_block(block=int(sys.argv[1]))
