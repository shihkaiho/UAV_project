import time
import json
import serial
import pynmea2
# Create the connection
ser_lora = serial.Serial('/dev/ttyACM0',9600)
ser_gps = serial.Serial('/dev/serial0',9600)
for i in [3,2,1]:
    print("starting in "+str(i)+"...")
    time.sleep(1)
counter = 0
average = 2.
start_time = time.time()
send_period = 1
lat = 0.
lon = 0.
alt = 0.
while(1):
    try:
        msg = ser_gps.readline().decode().rstrip()
        if msg[0:6] == '$GNGGA':
            print(counter)
            counter = counter + 1
            msg = pynmea2.parse(msg)
            lat = lat + (float(msg.lat[0:2])+float(msg.lat[2:])/60.)/average
            lon = lon + (float(msg.lon[0:3])+float(msg.lon[3:])/60.)/average
            alt = alt + (float(msg.altitude)+float(msg.geo_sep))/average
            if counter == average:
                counter = 0
                lat_str = str(lat)[0:14]
                lon_str = str(lon)[0:14]
                alt_str = str(alt)[0:14]
                lat = 0.
                lon = 0.
                alt = 0.
                transmit_data = json.dumps({'lat':lat_str,'lon':lon_str,'alt':alt_str})
                ser_lora.write((transmit_data+"\n").encode())
                print("transmit: "+transmit_data)
                tick = time.time()
                while(True):
                    if(ser_lora.in_waiting):
                        line = ser_lora.readline().decode().rstrip()
                        print("received: "+line)
                        break
                    if(time.time()-tick>5):
                        break
        
    except:
        break

