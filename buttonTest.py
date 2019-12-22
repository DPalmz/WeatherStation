import ArduinoFunctions

connection, name = ArduinoFunctions.connectSerial()
data = ArduinoFunctions.readSerial(connection, name)

if(0x1 & data)

    print("sun ")

if(0x2 & data)

    print("rain ")

if(0x4 & data)

    print("cloud ")

if(0x8 & data)

    print("snow ")

if(0x10 & data)

    print("view ")