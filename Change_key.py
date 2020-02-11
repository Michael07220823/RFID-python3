import signal
import time
import sys
from pirc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def end_read(signal,frame):
    global run
    print("\n[RFID]Ctrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

while run:
    print("\n[RFID] Starting")
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    if not error:
        print("[RFID] Detected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print("[RFID] Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        print("[RFID] Setting tag")
        util.set_tag(uid)

        print("[RFID] Authorizing")
        util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

        print("[RFID] Writing modified bytes")
        util.rewrite(4, [None, None, 0x69, 0x24, 0x40])
        util.read_out(4)
	
	    # Change Key-A and Key-B and access bits.
        util.write_trailer(1, (0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF), (0xFF, 0x07, 0x80), 105, (0x74, 0x00, 0x52, 0x35, 0x00, 0xFF))
        util.deauth()

        time.sleep(1)
