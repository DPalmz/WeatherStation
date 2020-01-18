from tkinter import *
from PIL import ImageTk,Image
from datetime import date
import sys
import os
sys.path.append(os.path.abspath(r"\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master"))
import ArduinoFunctions

# *** Establish connection
connection1, name1 = ArduinoFunctions.connectSerial() #open serial ports
connection2, name2 = ArduinoFunctions.connectSerial()
data1 = ArduinoFunctions.readSerial(connection1, name1)
data2 = ArduinoFunctions.readSerial(connection2, name2)

# *** Window setup
MainWindow = Tk()
MainWindow.attributes("-fullscreen", True)
MainWindow.title("Coastal Connections Weather Station") 					# the name of the window
width_value = MainWindow.winfo_screenwidth()   								# automatically sets the window fullsize based on the resolution of the screen used
height_value = MainWindow.winfo_screenheight()
##width_value=1920
##height_value=1080
MainWindow.geometry("%dx%d+0+0" %(width_value,height_value))

Can=Canvas(MainWindow, width=width_value, height=height_value, bg="blue")	# base window
Can.place(x=0, y=0)
img = Image.open(r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\BGW.gif").resize((width_value+10,height_value+10),Image.ANTIALIAS)
pic = ImageTk.PhotoImage(img)												# background image
Can.create_image(-5, -5, image=pic, anchor=NW)


# *** Coastal Connections logo
coast = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\coast.gif")
coast1 = Label(MainWindow, image=coast)
coast1.grid(sticky="n") 


# *** Title
label0 = Label(MainWindow,  text="Weather Station", bd=8, relief="flat", font="HelveticaNeue 100 bold",bg="royalblue4", fg="deepskyblue")
label0.grid(row=0, column=1, columnspan=2, sticky="n")


# *** Battery status

if(name1=="Moteino"):
	BATst = ArduinoFunctions.getBatStatus(data1[6])							# passes battery level to get percentage
elif(name2=="Moteino"):
	BATst = ArduinoFunctions.getBatStatus(data2[6])	
else:
	BATst = ""

if(BATst == "100"):
	battPic = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\Batt_Full.gif")
elif(BATst == "80"):
	battPic = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\Batt_75.gif")
elif(BATst == "50"):
	battPic = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\Batt_50.gif")
elif(BATst == "20"):
	battPic = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\Batt_25.gif")
elif(BATst == "Dead"):
	battPic = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\Batt_0.gif")
elif(BATst == "Overcharged"):
	battPic = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\Batt_Ovr.gif")
else:
	battPic = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\Batt_Unk.gif")

statuslabel = Label(MainWindow, image=battPic)  	   				 		# display battery level on top right of screen
statuslabel.place(x=width_value-130, y=0)                		    


# *** Clock/Date
# *** this function calls the time libary which will be used to create a dyanmic digital clock
# *** Creates a frame to add a grid within the cell - this allows for date/time to be in single cell (w/out overlapping)
f1 = Frame(MainWindow)
f1.grid(row=1, column=1, columnspan=2)

import time as tm
def display_time():
    current_time= tm.strftime('%I:%M:%S:%p')
    labelTime['text'] = current_time
    MainWindow.after(1000,display_time)
labelTime= Label(f1,bd=4, relief="sunken", font="HelveticaNeue 80 bold", bg="royalblue4", fg ="deepskyblue", text= display_time, anchor=CENTER, width= 15)
labelTime.grid(row=0, column=0, columnspan=2, sticky="nwse")
display_time()
# *** this function is used to get and display the current date

def display_date():
    today=date.today()
    cdate=today.strftime("%b %d, %Y")
    DateLabel['text']=cdate
    MainWindow.after(1000,display_date)
DateLabel = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 80 bold", bg="royalblue4",  fg="deepskyblue", text=display_date, anchor=CENTER, width=15)
DateLabel.grid(row=1, column=0, columnspan=2, sticky="nwse")
display_date()

# *** Weather Station data handling
photoresistor = 0												#Default values
rainy = 0
temp = 0
hum = 0
pres = 0
precipitation = 0
windD = "??"
windSpeed = 0
windy = (windD,windSpeed,"mi/hr")

if(name1=="Moteino"):
		hum = ArduinoFunctions.data1[1]								#humidity
		photoresistor = data1[7]									#photoresistor
		rainy = ArduinoFunctions.getRainVolume(data1[2])			#precipitation
		temp = ArduinoFunctions.data1[0]							#temperature
		pres = 0													#air pressure
		precipitation = ArduinoFunctions.getSnow(data1[5])			#snow fall
		windD = ArduinoFunctions.getWindDirection(data1[4])			#wind direction
		windSpeed = ArduinoFunctions.getWindSpeed(data1[3])			#wind speed
	
		windy = (windD,windSpeed,"mi/hr")							#format for output

elif(name2=="Moteino"):
		hum = ArduinoFunctions.data2[1]								#humidity
		photoresistor = data2[7]									#photoresistor
		rainy = ArduinoFunctions.getRainVolume(data2[2])			#precipitation
		temp = ArduinoFunctions.data2[0]							#temperature
		pres = 0													#air pressure
		precipitation = ArduinoFunctions.getSnow(data2[5])			#snow fall
		windD = ArduinoFunctions.getWindDirection(data2[4])			#wind direction
		windSpeed = ArduinoFunctions.getWindSpeed(data2[3])			#wind speed
	
		windy = (windD,windSpeed,"mi/hr")							#format for output

# *** puts corresponding icon on left and aligns the text under the cell holding the date/time
if photoresistor > 1000:
        photo1 = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\sunnyicon2.gif")
        label1 = Label(MainWindow, image=photo1)
        label1.grid(row=1, sticky="sw")
        labelS = Label(f1, bd=4, relief="flat", font="HelveticaNeue 80 bold", bg="royalblue4", fg="deepskyblue", text="Sunny" )
        labelS.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
elif photoresistor < 1000 and rainy == 0:
		photo3 = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\cloudyicon.gif")
		label3 = Label(MainWindow, image=photo3)
		label3.grid(row=1, sticky="sw")
		labelC = Label(f1, bd=4, relief="sunken", font="HeLveticaNeue 80 bold", bg="royalblue4", fg="deepskyblue", text="Cloudy")
		labelC.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
elif (precipitation == "freezing, possible sleet") or (precipitation ==  "possible snow"):
        photo4 = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\snowyicon.gif")
        label4 = Label(MainWindow, image=photo4)
        label4.grid(row=1, sticky="sw")
        labelSS = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 80 bold", bg="royalblue4", fg="deepskyblue", text="Snowy")
        labelSS.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
elif rainy != 0:
        photo2 = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\rainyicon.gif")
        label2 = Label(MainWindow, image=photo2)
        label2.grid(row=1, sticky="sw")
        labelR = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 80 bold", bg="royalblue4", fg="deepskyblue", text="Rainy")
        labelR.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
else :
		print ("Error")


# *** humidity, air pressure, and wind speed/direction always at bottom of page
humidity = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 50 normal", bg="royalblue4", fg="deepskyblue", text="Humidity: {}".format(hum))
humidity.grid(row=10, column=2, pady=50, sticky="w")

pressure = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 50 normal", bg="royalblue4", fg="deepskyblue", text="Pressure: {}".format(pres))
pressure.grid(row=10, column=1, pady=50)

wind = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 50 normal", bg="royalblue4", fg="deepskyblue", text="wind: {} {} {}".format(*windy))
wind.grid(row=10, column=0, pady=50, sticky="e")

# *** checkmark or x on mouse press (right or left) DO THIS LAST SO THAT X AND V APPEAR ABOVE EVERYTHING ELSE
def correct (*ignore):
	labelCheck.place(x=width_value/3, y=height_value/5)
	labelCheck.after(500, labelCheck.place_forget)
def incorrect (*ignore):
	labelEx.place(x=width_value/3, y=height_value/5)
	labelEx.after(500, labelEx.place_forget)

labelCheck = Label(MainWindow, font="HelveticaNeue 500 bold", bg="royalblue4", fg="limegreen", text = "✓", anchor='center')		
labelEx = Label(MainWindow, font="HelveticaNeue 500 bold", bg="royalblue4", fg="crimson", text = "✗", anchor='center')

MainWindow.bind('<Button-1>', correct)			#bindings
MainWindow.bind('<Button-2>', incorrect)

MainWindow.mainloop()

