import time
import json
from pymavlink import mavutil
import serial
# Create the connection
master = mavutil.mavlink_connection('/dev/ttyACM0',baud=57600)
msg1 = master.recv_match(type="GPS_RAW_INT",blocking=True)
msg2 = master.recv_match(type="AHRS3",blocking=True)
d = msg1.to_dict()
print(d)
d = msg2.to_dict()
print(d)
