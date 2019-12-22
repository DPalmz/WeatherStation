from serial import *                                #import serial library functions
from sys import exit                                #import exit from sys library

#determine 
def getVoltage(an):
    if an > 925:
        status = "Battery charging"
    elif an > 700: 
                return status

#determine 
def getLight(an):
    return 

#multiply ticks by rotation factor in MPH
def getWindSpeed(ticks):
    return ticks * 1.492

#multiple ticks by volume factor in inches
def getRainVolume(ticks):
    return ticks * .011

def getWindDirection(an):
    #python has no switch. Dictionary acts as switch statement
    #create dictionary with calibrated direction values
    directions = {
        788:    "N",
        407:    "NNE",
        462:    "NE",
        82:     "ENE",
        91:     "E",
        64:     "ESE",
        183:    "SE",
        125:    "SSE",
        287:    "S",
        244:    "SSW",
        631:    "SW",
        600:    "WSW",
        945:    "W",
        828:    "WNW",
        887:    "NW",
        704:    "NNW"
    }
    return directions.get(an)   #get direction

#does comparisons for snow estimation
def getSnow(an, temp, hum):
    if an > 680 and temp < 0:                                   #sensor and temp comp
        reading = "freezing, possible sleet"                    #corresponding message
    elif an > 680 and temp < 13:                                #sensor and temp comp
        reading = "dry and cold"                                #corresponding message
    elif an < 680 and ((temp < 0 and hum < 30) or temp < -6):   #sensor and temp comp
        reading = "possible snow"                               #corresponding message
    else:                                                       #otherwise
        reading = "no snow, not cold"                           #corresponding message
    return reading                                              #return message

#read a set of values from the arduino
def readSerial(connection, name):
    if name == "Moteino":                               #for Moteino connection
        values = []                                     #create an empty list
        for i in range(0,7):                    #loop n-1 times for most data
            values.append(connection.readline())        #read data from the connection
            values[i] = values[i].decode()              #translate bytes to string
            values[i] = int(values[i])                  #convert to int
        values.append(connection.readline())            #read data from the connection
        values[i] = values[i].decode()                  #translate bytes to string
        values[i] = float(values[LAST])                 #convert to float (battery Voltage)
    elif name == "CC1101":                              #for CC1101 connection
        values = connection.readline()                  #read a byte from the connection
    else:                                               #all other cases
        values = None                                   #set to null
    return values                                       #return values

#read a line from the serial connection and convert it from bytes
def connectSerial():
    port = "/dev/ttyUSB{}" #windows: "com{}", linux:    #create port string
    i = 0                                               #create a counter
    while True:                                         #loop forever
        try:                                            #try the following code
            connection = Serial(port.format(i), 9600)   #open serial connection at 9600 baud
            break                                       #break out of the while loop
        except SerialException:                         #catch exception
            i += 1                                      #increment counter
            if i > 256:                                 #check for com port limit
                return (None, None)                             #no port opened
    name = connection.readline()                        #read data from the connection
    name = name.decode()                                #decode the message
    if name == "Moteino\r\n":                #execute on "moteino"
        name = "Moteino"                                #set to simpler string
    elif name == "CC1101\r\n":                 #execute on "cc1101" 
        name = "CC1101"                                 #set to simpler string
    else:                                               #execute for other cases
        name = None                                     #no device name given
    return (connection, name)                           #return connection and device name
    
