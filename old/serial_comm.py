import time
import json
from pymavlink import mavutil
import serial
# Create the connection
master = mavutil.mavlink_connection('/dev/ttyACM0',baud=57600)
msg = master.recv_match(type="GPS_RAW_INT",blocking=True)
d = msg.to_dict()
satellites_visible = d['satellites_visible']
msg = master.recv_match(type="AHRS3",blocking=True)
d = msg.to_dict()
lat = str(d['lat'])
lon = str(d['lng'])
alt = str(d['altitude'])
transmit_data = json.dumps({'lat':lat,'lon':lon,'alt':alt,'satellites_visible':satellites_visible})
a = json.loads(transmit_data)
print(a['lat'])
print(a['lon'])
print(a['alt'])
print(a['satellites_visible'])
ser = serial.Serial('/dev/ttyACM1',9600)
time.sleep(3)
ser.write((transmit_data+"\n").encode())
print("transmit: "+transmit_data)
while(True):
    if(ser.in_waiting):
        line = ser.readline().decode().rstrip()
        print("received: "+line)
        break

