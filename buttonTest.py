from ArduinoFunctions import *

connection, name = connectSerial()

print("made connection " + name)
data = readSerial(connection, name)


print(data)

while(1):
    
    data = readSerial(connection, name)
    #data = int(data[:-2])
    print(data)
    print(data[0])
    '''if data is not None:
        if(0X1 & data):

            print("sun ")

        if(0X2 & data):

            print("rain ")

        if(0X4 & data):

            print("cloud ")

        if(0X8 & data):

            print("snow ")

        if(0X10 & data):

            print("view ")
'''