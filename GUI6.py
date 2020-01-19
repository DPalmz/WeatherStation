from tkinter import *
from contextlib import contextmanager
from PIL import ImageTk,Image
from datetime import date
from threading import Lock, Thread
import ArduinoFunctions
import os
import sys
import time as tm
import weatherData

sys.path.append(os.path.abspath(r"/home/pi/Documents/WeatherStation"))


# *** Default data values
BATst = ""
photoresistor = 0 
rainy = 0
temp = 0
hum = 0
precipitation = 0
windD = "??"
windSpeed = 0
windy = (windD,windSpeed,"mi/hr")

data1 = 0
data2 = 0
lock = Lock()


# *** Establish connection
connection1, name1 = ArduinoFunctions.connectSerial() #open serial ports
connection2, name2 = ArduinoFunctions.connectSerial()
    
    
# *** Window setup
print("window setup")
MainWindow = Tk()
MainWindow.attributes("-fullscreen", True)
MainWindow.title("Coastal Connections Weather Station")                     # the name of the window
width_value = MainWindow.winfo_screenwidth()                                # automatically sets the window fullsize based on the resolution of the screen used
height_value = MainWindow.winfo_screenheight()
MainWindow.geometry("%dx%d+0+0" %(width_value,height_value))

Can=Canvas(MainWindow, width=width_value, height=height_value, bg="blue")   # base window
Can.place(x=0, y=0)
img = Image.open(r"/home/pi/Documents/WeatherStation/Pictures/BGW.gif").resize((width_value+10,height_value+10),Image.ANTIALIAS)
pic = ImageTk.PhotoImage(img)                                               # background image
Can.create_image(-5, -5, image=pic, anchor=NW)


# *** Coastal Connections logo

img2 = Image.open(r"/home/pi/Documents/WeatherStation/Pictures/coast.gif").resize((506,210),Image.ANTIALIAS)
coast = ImageTk.PhotoImage(img2)
coast1 = Label(MainWindow, image=coast)
coast1.grid(sticky="ns") 


# *** Title
label0 = Label(MainWindow,  text="Weather Station", borderwidth=12, relief="groove", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue")
label0.grid(row=0, column=1, columnspan=2, sticky="n")


# *** Clock/Date
# *** this function calls the time libary which will be used to create a dyanmic digital clock
# *** Creates a frame to add a grid within the cell - this allows for date/time to be in single cell (w/out overlapping)
f1 = Frame(MainWindow)
f1.grid(row=1, column=1, columnspan=2)

def display_time():
    current_time= tm.strftime('%I:%M:%S:%p')
    labelTime['text'] = current_time
    MainWindow.after(1000,display_time)
labelTime= Label(f1,bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg ="deepskyblue", text= display_time, anchor=CENTER, width= 15)
labelTime.grid(row=0, column=0, columnspan=2, sticky="nwse")
display_time()

def display_date():
    today=date.today()
    cdate=today.strftime("%b %d, %Y")
    DateLabel['text']=cdate
    MainWindow.after(1000,display_date)
DateLabel = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4",  fg="deepskyblue", text=display_date, anchor=CENTER, width=15)
DateLabel.grid(row=1, column=0, columnspan=2, sticky="nwse")
display_date()
'''
# *** context manager - handles timeout for the thread lock
def acquire_timeout(lock, timeout):
    result = lock.acquire
    yield result
    if result:
        lock.release()
with acquire_timeout(lock, 2) as acquired:
    if acquired:
        weatherData()
    else:
        polling()
'''     
        
# *** puts battery status icon on top right of page
if(BATst == "100"):
    battPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_Full.gif")
elif(BATst == "80"):
    battPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_75.gif")
elif(BATst == "50"):
    battPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_50.gif")
elif(BATst == "20"):
    battPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_25.gif")
elif(BATst == "Dead"):
    battPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_0.gif")
elif(BATst == "Overcharged"):
    battPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_Ovr.gif")
else:
    battPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_Unk.gif")

statuslabel = Label(MainWindow, relief="sunken", image=battPic)                      #display battery level on top right of screen
statuslabel.place(x=width_value-130, y=0)                           


# *** puts corresponding weather condition icon on left and places the text under date/time
if photoresistor > 1000:
        photo1 = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/sunnyicon2.gif")
        label1 = Label(MainWindow, image=photo1)
        label1.grid(row=1, sticky="sw")
        labelS = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Sunny" )
        labelS.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
elif photoresistor < 1000 and rainy == 0:
        photo2 = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/cloudyicon.gif")
        label2 = Label(MainWindow, image=photo2)
        label2.grid(row=1, sticky="sw")
        labelC = Label(f1, bd=4, relief="sunken", font="HeLveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Cloudy")
        labelC.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
elif (precipitation == "freezing, possible sleet") or (precipitation ==  "possible snow"):
        photo3 = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/snowyicon.gif")
        label3 = Label(MainWindow, image=photo3)
        label3.grid(row=1, sticky="sw")
        labelSS = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Snowy")
        labelSS.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
elif rainy != 0:
        photo4 = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/rainyicon.gif")
        label4 = Label(MainWindow, image=photo4)
        label4.grid(row=1, sticky="sw")
        labelR = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Rainy")
        labelR.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
else :
        print ("Error")


# *** humidity, temp and wind speed/direction always at bottom of page
humidity = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 50 normal", bg="royalblue4", fg="deepskyblue", text="Humidity: {}".format(hum))
humidity.grid(row=10, column=2, pady=50, sticky="ew")

temperature = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 50 normal", bg="royalblue4", fg="deepskyblue", text="Temperature: {}°F".format(hum))
temperature.grid(row=10, column=1, pady=50)

wind = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 50 normal", bg="royalblue4", fg="deepskyblue", text="wind: {} {} {}".format(*windy))
wind.grid(row=10, column=0, pady=50, sticky="ew")

# *** Button i/o
# *** Checkmark or x on mouse press (right or left) DO THIS LAST SO THAT X AND V APPEAR ABOVE EVERYTHING ELSE
def polling():
    def escape():
        return

    global data1
    global data2
    #lock.acquire()
    data1 = ArduinoFunctions.readSerial(connection1, name1)
    data2 = ArduinoFunctions.readSerial(connection2, name2)
    #lock.release()
    escape()
'''
threads = []
for func in [polling(), weatherData()]:
        threads.append(Thread(target=funct))
        threads[-1].start()
thread.join()    
'''

# *** button handling
def correct (*ignore):
    labelCheck.place(x=width_value/3, y=height_value/5)
    labelCheck.after(500, labelCheck.place_forget)
def incorrect (*ignore):
    labelEx.place(x=width_value/3, y=height_value/5)
    labelEx.after(500, labelEx.place_forget)

labelCheck = Label(MainWindow, font="HelveticaNeue 500 bold", bg="royalblue4", fg="limegreen", text = "✓", anchor='center')     
labelEx = Label(MainWindow, font="HelveticaNeue 500 bold", bg="royalblue4", fg="crimson", text = "✗", anchor='center')

MainWindow.bind('<Button-1>', correct)          #bindings
MainWindow.bind('<Button-2>', incorrect)


while True:
    polling()
    weatherData()

MainWindow.mainloop()

