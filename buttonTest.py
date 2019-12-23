import ArduinoFunctions

connection, name = ArduinoFunctions.connectSerial()
while(1):
    data = ArduinoFunctions.readSerial(connection, name)
    if data is not None:
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
