import time
import json
import serial
from dronekit import connect
import numpy as np
import adi
#import pynmea2
# Create the connection
ser_lora = serial.Serial('/dev/ttyACM0',9600)
sdr = adi.Pluto("ip:192.168.2.1")
vehicle = connect("/dev/ttyACM1", wait_ready=True)
for i in [3,2,1]:
    print("starting in "+str(i)+"...")
    time.sleep(1)

sample_rate = 1e6 # Hz
center_freq = 3.1e9 # Hz
num_samps = 100000 # number of samples per call to rx()
sdr.sample_rate = int(sample_rate)
# Config Rx
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 50.0 # dB, increase to increase the receive gain, but be careful not to saturate the ADC


counter = 0
average = 2.
start_time = time.time()
send_period = 1
lat = 0.
lon = 0.
alt = 0.
pitch = vehicle.attitude.pitch
yaw = vehicle.attitude.yaw
roll = vehicle.attitude.roll
amp = 0.
while(1):
    print("counter: "+str(counter))
    counter = counter + 1
    gps = vehicle.location.global_frame
    #lat = lat + (float(msg.lat[0:2])+float(msg.lat[2:])/60.)/2
    #lon = lon + (float(msg.lon[0:3])+float(msg.lon[3:])/60.)/2
    #alt = alt + (float(msg.altitude)+float(msg.geo_sep))/2
    gps = vehicle.location.global_frame
    #lat = lat + (float(msg.lat[0:2])+float(msg.lat[2:])/60.)/2
    #lon = lon + (float(msg.lon[0:3])+float(msg.lon[3:])/60.)/2
    #alt = alt + (float(msg.altitude)+float(msg.geo_sep))/2
    lat_str = str(lat)[0:14]
    lon_str = str(lon)[0:14]
    alt_str = str(alt)[0:14]
    lat = 0.
    lon = 0.
    alt = 0.
    pitch = vehicle.attitude.pitch
    yaw = vehicle.attitude.yaw
    roll = vehicle.attitude.roll
    for i in range (0, 10):
        raw_data = sdr.rx()
    rx_samples = sdr.rx()
    # Calculate power spectral density (frequency domain version of signal)
    psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2
    psd_dB = 10*np.log10(psd)
    f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))
    amp = max(psd_dB[52700:55000])
    print(amp)
    transmit_data = json.dumps({'index':counter,'lat':lat_str,'lon':lon_str,'alt':alt_str,'pitch':str(pitch),'yaw':str(yaw),'roll':str(roll),'amp':str(amp)})
    ser_lora.write((transmit_data+"\n").encode())
    #print("transmit: "+transmit_data)
    tick = time.time()
    while(True):
        if(ser_lora.in_waiting):
            line = ser_lora.readline().decode().rstrip()
            print("received: "+line)
            break
        if(time.time()-tick>0.5):
            break
