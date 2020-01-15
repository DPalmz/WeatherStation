import serial
ser = serial.Serial("/dev/ttyUSB0",9600)
ser.flushInput()

while True:
    if(ser.in_waiting >0):
        data = ser.readline()
        print(data)

