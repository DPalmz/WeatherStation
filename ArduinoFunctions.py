from serial import *	#import serial library functions
from sys import exit	#import exit from sys library

#python has no switch. Dictionary acts as switch statement
#create dictionary with calibrated direction values
directions = {
	788:	"N ",
	462:	"NE",
	91:		"E ",
	183:	"SE",
	287:	"S ",
	631:	"SW",
	945:	"W ",
	887:	"NW"
}

#determine aproximate state of battery
def getBatStatus(an):
	status = "0"
	#convert ADC reading to voltage
	#calculate battry voltage from ADC voltage
	#resistor values: 680k and 220k 
	an = (an*(3.3/1023))*(677+215)/215
	if an > 14.4:
		status = "Overcharged"
	elif an > 13:
		status = "100%"
	elif an > 12.5:
		status = "80%"
	elif an > 12:
		status = "50%"
	elif an > 11.4:
		status = "20%"
	else:
		status = "Dead"
	return status

#multiply ticks by rotation factor in MPH
def getWindSpeed(ticks):
	return ticks * 1.492

#multiple ticks by volume factor in inches
def getRainVolume(ticks):
	return ticks * .011

#return corresponding direction given reading
def getWindDirection(an):
	return directions.get(an)

#does comparisons for snow estimation
def getSnow(an, temp, hum):
	if an > 680 and temp < 0:									#sensor and temp comp
		reading = "freezing, possible sleet"					#corresponding message
	elif an > 680 and temp < 13:								#sensor and temp comp
		reading = "dry and cold"								#corresponding message
	elif an < 680 and ((temp < 0 and hum < 30) or temp < -6):	#sensor and temp comp
		reading = "possible snow"								#corresponding message
	else:														#otherwise
		reading = "no snow, not cold"							#corresponding message
	return reading												#return message

#read a set of values from the arduino
def readSerial(connection, name):
	values = ['-1']											#default return value
	if name == "Moteino":									#handle moteino data
		if(connection.in_waiting>0):						#check for data in buffer
			values = connection.readline().decode().split()	#read line and decode data
		else:												#otherwise
			values = ["-1"]									#set variable to default list
	elif name == "CC1101":									#handle for CC1101 data
		if(connection.in_waiting>0):						#check for data in buffer
			values = connection.readline()					#read line
			values = values.decode()[:-2]					#decode data and remove 2 end chars
		else:												#otherwise
			values = '-1'									#set variable to default value
	return values											#return values
	
#read a line from the serial connection and convert it from bytes
def connectSerial(counter):
	port = "/dev/ttyUSB{}"								#create port string
	i = counter											#create a counter
	while True:											#loop forever
		try:											#try the following code
			connection = Serial(port.format(i), 38400)	#open serial connection at 9600 baud (38400 now)
			break										#break out of the while loop
		except SerialException:							#catch exception
			i += 1										#increment counter
			if i > 256:									#check for com port limit
				return ("error", "error")				#no port opened
	connection.flushInput()								#get rid of anything left over?
	while True:											#loop forever
		data = connection.readline()					#read data from the connection
		try:											#try the following code
			data = data.decode()						#decode the message
		except UnicodeDecodeError:						#catch decoding error
			continue									#go to beginning of loop
		if data == "Moteino\r\n":						#execute on "moteino"
			name = "Moteino"							#set to simpler string
			break										#exit loop
		elif data == "CC1101\r\n":						#execute on "cc1101" 
			name = "CC1101"								#set to simpler string
			break										#exit loop
	garbage =  connection.readline().decode()			#decode received data
	while garbage != "Good!\r\n":						#wait for
		connection.write(bytes([254]))					#send 0xFE
		garbage = connection.readline().decode()		#decode received data
	return (connection, name)							#return port and device name
