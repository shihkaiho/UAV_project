import time
import json
from pymavlink import mavutil
import serial
# Create the connection
master = mavutil.mavlink_connection('/dev/ttyACM0',baud=57600)
msg = master.recv_match(type="GPS_RAW_INT",blocking=True)
d = msg.to_dict()
lat = d['lat']
lon = d['lon']
alt = d['alt']
satellites_visible = d['satellites_visible']
transmit_data = json.dumps({'lat':lat,'lon':lon,'alt':alt,'satellites_visible':satellites_visible})
a = json.loads(transmit_data)
print(lat)
print(lon)
print(alt)
print(a['satellites_visible'])
msg = master.recv_match(type="AHRS3",blocking=True)
d = msg.to_dict()
print(d['lat'])
print(d['lng'])
print(d['altitude'])
