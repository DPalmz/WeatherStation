from ArduinoFunctions import *

connection, name = connectSerial()

data = readSerial(connection, name)
data = data.decode()[:-2]
print(data)

while(1):
    #print("potat")
    data = readSerial(connection, name)
    data = data.decode()
    data = int(data[:-2])
    print(data)
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