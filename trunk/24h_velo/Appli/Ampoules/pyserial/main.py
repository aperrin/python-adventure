import serial
import binascii
import struct

ser = serial.Serial('COM1', 9600, timeout = 1)
print ser.portstr

while 1:
    data=ser.readline()
    data = data.strip('0').strip()
    if data :
        print len(data)
        print struct.unpack("I", data)[0]