import serial
ser = serial.Serial("/dev/ttyUSB0",9600)
ser.flushInput()

while True:
    data = ser.readline()
    print(data)

