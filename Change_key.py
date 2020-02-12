import signal
import time
import sys
import RPi.GPIO as GPIO
from pirc522 import RFID


rdr = RFID()
util = rdr.util()
util.debug = True
# Disable warning information.
GPIO.setwarnings(False)


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
    #util.auth(rdr.auth_a, [255, 255, 255, 255, 255, 255])
    #util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
    util.auth(rdr.auth_b, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
    
    # Determine whether to give arguments.
    # One argument is sector numeric. 
    if len(sys.argv) > 1 and len(sys.argv) <=2:
        sector = int(sys.argv[1])
        
        # Calculate block numeric.
        block_numeric = sector * 4 + 3
        util.read_out(block_numeric)

        # Change Key-A and Key-B and access bits.
        util.write_trailer(sector, (255, 255, 255, 255, 255, 255), (255, 7, 128), 0, (255, 255, 255, 255, 255, 255))
        util.read_out(block_numeric)
        
        
    # Two arguments is sector start and end.
    elif len(sys.argv) > 2 and len(sys.argv) <=3:
        sector_start = int(sys.argv[1])
        sector_end = int(sys.argv[2])
        
        for sector in range(sector_start, sector_end+1):
            rdr.wait_for_tag()
            (error, data) = rdr.request()
            (error, uid) = rdr.anticoll()
            if not error:
                util.set_tag(uid)
                #util.auth(rdr.auth_a, [255, 255, 255, 255, 255, 255])
                util.auth(rdr.auth_b, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
                #util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
                # Calculate block numeric.
                block_numeric = sector * 4 + 3
                util.read_out(block_numeric)
                # Change Key-A and Key-B and access bits.
                util.write_trailer(sector, (255, 255, 255, 255, 255, 255), (255, 7, 128), 0, (255, 255, 255, 255, 255, 255))
                util.read_out(block_numeric)
                time.sleep(1)
    else:
        util.read_out(7)
        # Change Key-A and Key-B and access bits.
        util.write_trailer(1, (255, 255, 255, 255, 255, 255), (255, 7, 128), 0, (255, 255, 255, 255, 255, 255))
        util.read_out(7)
    
    print("[RFID] Deauthorizing")
    util.deauth()

    # Clean GPIO PIN state.
    rdr.cleanup()
