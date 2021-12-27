# read GPS
import serial
import pynmea2
ser = serial.Serial()
ser.baudrate = 9600
#ser.port = '/dev/tty.usbmodem141401'
ser.port = '/dev/tty.usbmodem142301'
ser.open()
R = 6378137
while True:
    msg = ser.readline().decode().rstrip()
    if msg[0:6] == '$GNGGA':
        msg = pynmea2.parse(msg)
        if msg.lat=='' or msg.lon=='':
            print("no GPS data")
            continue
        lat = float(msg.lat[0:2])+float(msg.lat[2:])/60.
        lon = float(msg.lon[0:3])+float(msg.lon[3:])/60.
        alt = float(msg.altitude)+float(msg.geo_sep)
        lat = str(lat)[0:14]
        lon = str(lon)[0:14]
        alt = str(alt)[0:14]
        print(lat)
        print(lon)
        print(alt)