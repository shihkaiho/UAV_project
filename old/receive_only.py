import time
import json
from pymavlink import mavutil
import serial
# Create the connection
#master = mavutil.mavlink_connection('/dev/ttyACM1',baud=57600)
#msg = master.recv_match(type="GPS_RAW_INT",blocking=True)
#d = msg.to_dict()
#lat = d['lat']
#lon = d['lon']
#alt = d['alt']
#satellites_visible = d['satellites_visible']
#transmit_data = json.dumps({'lat':lat,'lon':lon,'alt':alt,'satellites_visible':satellites_visible})
#a = json.loads(transmit_data)
#print(a['lat'])
#print(a['lon'])
#print(a['alt'])
#print(a['satellites_visible'])
ser = serial.Serial('/dev/ttyACM0',9600)
#counter = 1
while True:
    #ser.write((str(counter)+"\n").encode())
    #print("transmitted: "+str(counter))
    if(ser.in_waiting):
        line = ser.readline().decode().rstrip()
        print("received: "+line)
    #counter = counter+1
    #time.sleep(0.5)
