from tkinter import *
from PIL import ImageTk,Image
import sys
import os
sys.path.append(os.path.abspath(r"\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master"))
import ArduinoFunctions
connection1, name1 = ArduinoFunctions.connectSerial() #open serial ports
connection2, name2 = ArduinoFunctions.connectSerial()
data1 = ArduinoFunctions.readSerial(connection1, name1)
data2 = ArduinoFunctions.readSerial(connection2, name2)


# *** Window setup
MainWindow = Tk()
MainWindow.attributes("-fullscreen", True)
MainWindow.title("Coastal Connections Weather Station")  # the name of the window
width_value = MainWindow.winfo_screenwidth()    # automatically sets the window fullsize based on the resolution of the screen used
height_value = MainWindow.winfo_screenheight()
##width_value=1920
##height_value=1080
MainWindow.geometry("%dx%d+0+0" %(width_value,height_value))

Can=Canvas(MainWindow, width=width_value, height=height_value, bg="blue")
img = Image.open(r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\BGW.gif").resize((width_value,height_value),Image.ANTIALIAS)
pic = ImageTk.PhotoImage(img)
Can.create_image(0, 0, image=pic, anchor=NW)
Can.place(x=-10, y=-10)


# *** Coastal Connections logo
coast = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\coast.gif")
coast1 = Label(MainWindow, image=coast)
coast1.grid(sticky="n", rowspan=4) 


# *** Title
label0 = Label(MainWindow,  text="Weather Station", bd=8, relief="flat", font="HelveticaNeue 40 bold",bg="blue4", fg="deepskyblue")   # first label that appears is the name of the project
label0.grid(row=0,column=1, sticky="n")


# *** Battery status
BATst= "100% Full"
statuslabel = Label(MainWindow, text=BATst, bd=1, relief= "sunken")    # this is just a simple status bar
statuslabel.grid(row=0, column=2, sticky="ne")                    # this just expands the status bar through the whole line


# *** Clock/Date
# *** this function calls the time libary which will be used to create a dyanmic digital clock
# *** Creates a frame to add a grid within the cell allowing for date/time to be in single cell
f1 = Frame(MainWindow)
f1.grid(row=1,column=1,columnspan=2)

import time as tm
def display_time():
    current_time= tm.strftime('%I:%M:%S:%p')
    labelTime['text'] = current_time
    MainWindow.after(1000,display_time)
labelTime= Label(f1,bd=4, relief="sunken", font="HelveticaNeue 80 bold", bg="blue4", fg ="deepskyblue", text= display_time, anchor=CENTER, width= 15)
labelTime.grid(row=0, column=0, sticky="nwse")
display_time()
# *** this function is used to get and display the current date
from datetime import date
def display_date():
    today=date.today()
    cdate=today.strftime("%b %d, %Y")
    DateLabel['text']=cdate
    MainWindow.after(1000,display_date)
DateLabel = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 80 bold", bg="blue4",  fg="deepskyblue", text=display_date, anchor=CENTER, width=15)
DateLabel.grid(row=1, column=0, sticky="nwse")
display_date()



photoresistor = 0
rainy = 0
temp = 0
hum = 0
pres = 0
precipitation = 0
windD = "N"
windSpeed = 0
windy = (windD,windSpeed,"mi/hr")

if(name1 =="moteino"):
  
    photoresistor = data1[7]
    rainy = ArduinoFunctions.getRainVolume(data1[2])
    temp = ArduinoFunctions.data1[0]
    hum = ArduinoFunctions.data1[1]
    pres = 0
    precipitation = ArduinoFunctions.getSnow(data1[5])
    windD = ArduinoFunctions.getWindDirection(data1[4])
    windSpeed = ArduinoFunctions.getWindSpeed(data1[3])
    windy = (windD,windSpeed,"mi/hr")

elif(name2 == "moteino"):
    photoresistor = data2[7]
    rainy = ArduinoFunctions.getRainVolume(data2[2])
    temp = ArduinoFunctions.data2[0]
    hum = ArduinoFunctions.data2[1]
    pres = 0
    precipitation = ArduinoFunctions.getSnow(data2[5])
    windD = ArduinoFunctions.getWindDirection(data2[4])
    windSpeed = ArduinoFunctions.getWindSpeed(data2[3])
    windy = (windD,windSpeed,"mi/hr")

# *** puts corresponding icon on left and aligns the text under the cell holding the date/time
if photoresistor >1000:
        photo1 = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\sunnyicon2.gif")
        label1 = Label(MainWindow, image=photo1)
        label1.grid(row=1, sticky="w")
        labelS = Label(f1, bd=4, relief="flat", font="HelveticaNeue 80 normal", bg="blue4", fg="deepskyblue", text="Sunny" )
        labelS.grid(row=2, column=0, sticky="nwse")
elif photoresistor< 1000 and rainy==0 :
		photo3 = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\cloudyicon.gif")
		label3 = Label(MainWindow, image=photo3)
		label3.grid(row=1, sticky="nswe")
		labelC = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 80 normal", bg="blue4", fg="deepskyblue", text="cloudy")
		labelC.grid(row=2, column=0, sticky="nswe")
elif (precipitation == "freezing, possible sleet") or (precipitation==  "possible snow"):
        photo4 = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\snowyicon.gif")
        label4 = Label(MainWindow, image=photo4)
        label4.grid(row=1, sticky="w")
        labelSS = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 80 normal", bg="blue4", fg="deepskyblue", text="snowy")
        labelSS.grid(row=2, column=0, sticky="nwse")
elif rainy !=0:
        photo2 = PhotoImage(file=r"C:\Users\leebr\PycharmProjects\Buttons\WeatherStation-master\WeatherStation-master\rainyicon.gif")
        label2 = Label(MainWindow, image=photo2)
        label2.grid(row=1, sticky="w")
        labelR = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 80 normal", bg="blue4", fg="deepskyblue", text="Rainy" )
        labelR.grid(row=2, column=0, sticky="nwse")
else :
    print ("Error")

# *** REMOVE Sample checkmark and x
'''
labelCheck = Label(MainWindow, font="HelveticaNeue 100 bold", bg="darkblue", fg="limegreen", text = "✓")
labelCheck.grid(row=2, column=2)
labelEx = Label(MainWindow, font="HelveticaNeue 100 bold", bg="darkblue", fg="crimson", text = "✗")
labelEx.grid(row=2, column=2)
'''

humidity = Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 50 normal", bg="blue4", fg="deepskyblue", text="Humidity: {}".format(hum))
humidity.grid(row=3, column=2)

pressure = Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 50 normal", bg="blue4", fg="deepskyblue", text="Pressure: {}".format(pres))
pressure.grid(row=3, column=1)

wind = Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 50 normal", bg="blue4", fg="deepskyblue", text="wind: {} {} {}".format(*windy))
wind.grid(row=3, column=0)



MainWindow.mainloop()

