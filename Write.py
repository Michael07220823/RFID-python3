import signal
import time
import sys
import RPi.GPIO as GPIO
from pirc522 import RFID

rdr = RFID()
util = rdr.util()
# Disable warning information.
GPIO.setwarnings(False)

def end_read(signal, frame):
    global run
    print("\n[RFID] Ctrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

def write_rfid():
    signal.signal(signal.SIGINT, end_read)

    while True:
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

            # Print specify block data
            util.read_out(1)

            # Wrute data to rfid card
            rdr.write(1, [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10])

            # Print specify block data
            util.read_out(1)
            
        print("[RFID] Deauthorizing")
        # Deauthorize, and clean authorize state.
        util.deauth()
        time.sleep(1)

if __name__ == "__main__":
    write_rfid()
