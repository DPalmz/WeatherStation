import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image
from datetime import date
#from threading import Lock, Thread
import ArduinoFunctions
import os
import sys
import time as tm
import altTab

sys.path.append(os.path.abspath(r"/home/pi/Documents/WeatherStation"))

# ***** Default Values *****
BATst = ""                          #Weather Station
photoresistor = 0 
rainy = 0
temp = 0
hum = 0
precipitation = 0
windD = "??"
windSpeed = 0
windy = (windD,windSpeed,"mi/hr")
#results = [BATst, hum, photoresistor, rainy, temp, precipitation, windD, windSpeed]

btnpress = 0                          #Button Box input and weather condition value to compare with
cnd = 0
#data1 = 0                             #Data in from weather station and button box (undetermined)
#data2 = 0
counter = 0
#lock = Lock()                         #Lock for multithreading

# *** Establish connection
connection1, name1 = ArduinoFunctions.connectSerial(counter) #open serial ports for button box and weather station
counter += 1
connection2, name2 = ArduinoFunctions.connectSerial(counter)  
   
# ***** Window setup *****
print("window setup")
MainWindow = tk.Tk()
MainWindow.attributes("-fullscreen", True)
MainWindow.title("Coastal Connections Weather Station")                     # the name of the window
width_value = MainWindow.winfo_screenwidth()                                 
height_value = MainWindow.winfo_screenheight()
#MainWindow.geometry("%dx%d+0+0" %(width_value,height_value))

Can=Canvas(MainWindow, width=width_value, height=height_value, bg="blue")   # base window
Can.place(x=0, y=0)
img = Image.open(r"/home/pi/Documents/WeatherStation/Pictures/BGW.gif").resize((width_value+10,height_value+10),Image.ANTIALIAS)
pic = ImageTk.PhotoImage(img)                                               # background image
Can.create_image(-5, -5, image=pic, anchor=NW)

# *** Coastal Connections logo
print("Logo")
img2 = Image.open(r"/home/pi/Documents/WeatherStation/Pictures/coast.gif").resize((506,210),Image.ANTIALIAS)
coast = ImageTk.PhotoImage(img2)
coast1 = Label(MainWindow, image=coast)
coast1.grid(sticky="ns") 

# *** Title
print("Title")
label0 = Label(MainWindow,  text="Weather Station", borderwidth=12, relief="groove", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue")
label0.grid(row=0, column=1, columnspan=2, sticky="n")

# *** Default Battery Status Image
battPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_Unk.gif")
statuslabel = Label(MainWindow, relief="sunken", image=battPic)   #display battery level on top right of screen
statuslabel.place(x=width_value-130, y=0) 

# *** Weather Condition Images
photo1 = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/sunnyicon2.gif")
label1 = Label(MainWindow, image=photo1)
photo2 = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/cloudyicon.gif")
label2 = Label(MainWindow, image=photo2, bg="green")
photo3 = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/snowyicon.gif")
label3 = Label(MainWindow, image=photo3)
photo4 = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/rainyicon.gif")
label4 = Label(MainWindow, image=photo4)

# *** Clock/Date
# *** f1 is a frame to add a grid within a single cell
f1 = Frame(MainWindow)
f1.grid(row=1, column=1, columnspan=2)
labelS = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Sunny" )
labelC = Label(f1, bd=4, relief="sunken", font="HeLveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Cloudy")
labelSS = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Snowy")
labelR = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Rainy")

# *** this function calls the time libary which will be used to create a dyanmic digital clock
def display_time():
    current_time= tm.strftime('%I:%M %p')
    #labelTime['text'] = current_time
    time_text.set(current_time)
    MainWindow.after(1000,display_time)
time_text = tk.StringVar(MainWindow)
labelTime= Label(f1,bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg ="deepskyblue", textvariable= time_text, anchor=CENTER, width= 15)
labelTime.grid(row=0, column=0, columnspan=2, sticky="nwse")
display_time()

def display_date():
    today=date.today()
    cdate=today.strftime("%b %d, %Y")
    #DateLabel['text']=cdate
    date_text.set(cdate)
    MainWindow.after(1000,display_date)
date_text = tk.StringVar(MainWindow)
DateLabel = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4",  fg="deepskyblue", textvariable=date_text, anchor=CENTER, width=15)
DateLabel.grid(row=1, column=0, columnspan=2, sticky="nwse")
display_date()

# ***** DATA HANDLING *****
def polling(MainWindow):
    global data1
    global data2
    # ***** Default Values *****
    BATst = ""                          #Weather Station
    photoresistor = 0 
    rainy = 0
    temp = 0
    hum = 0
    precipitation = 0
    windD = "??"
    windSpeed = 0
    windy = (windD,windSpeed,"mi/hr")
    tempData = '0'
    newData = []
    #lock.acquire()
    while True:
        data1 = ArduinoFunctions.readSerial(connection1, name1)      # get data from weather station and button box
        data2 = ArduinoFunctions.readSerial(connection2, name2)
        #lock.release()
        #MainWindow.update()
        #MainWindow.update_idletasks()
        
        if (name1 == "Moteino"):
            newData = weatherData(data1)         #BATst, hum, photoresistor, rainy, temp, precipitation, windD, windSpeed, windy                                       # update weather station data values
            buttonEvent(data2)
        elif (name2 == "Moteino"):
            newData = weatherData(data2)
            buttonEvent(data1)
        if (newData != '-1'):
            battStat(newData[0], newData[8])                                                   # determine image for battery status and weather condition
            weatherStat(newData[1], newData[2], newData[3], newData[6])
                                                # gets button input and compares to weather condition
        if (data1 != '-1' or data2 != '-1' or data1[0]!='-1' or data2[0]!='-1'):
            #print(data1, data2)
            MainWindow.update()
        #polling(MainWindow)                  # poll every 100ms
'''
# *** button box data handling
def buttonData(connection, name):
    if(name=="CC1101"):
            btnpress = ArduinoFunctions.readSerial(connection, name)
    return btnpress
'''
# *** Button i/o
def buttonEvent(data):
    def correct ():
        labelCheck.place(x=width_value/3, y=height_value/5)
        print("correct")
        MainWindow.after(200, labelCheck.place_forget)
    def incorrect ():
        labelEx.place(x=width_value/3, y=height_value/5)
        print("incorrect")
        MainWindow.after(200, labelEx.place_forget)

    labelCheck = Label(MainWindow, font="HelveticaNeue 500 bold", bg="royalblue4", fg="limegreen", text = "✓", anchor='center')
    labelEx = Label(MainWindow, font="HelveticaNeue 500 bold", bg="royalblue4", fg="crimson", text = "✗", anchor='center')

    btnpress = data

    if(btnpress == cnd):#show correct if matches weather condition
        correct()
    elif(btnpress == '1' or btnpress == '2' or btnpress == '4' or btnpress == '8'):
        incorrect()
    elif(btnpress == '10'):
        altTab.altTab()
    else:
        return
    return

# *** Puts battery status icon on top right of page
def battStat(BATst, data):
    global battPic
    #print("Battery Level: ", BATst)
    newbattPic = 0
    if (data != '-1'):
        if(BATst == "100%"):
            newbattPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_Full.gif")
        elif(BATst == "80%"):
            newbattPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_75.gif")
        elif(BATst == "50%"):
            newbattPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_50.gif")
        elif(BATst == "20%"):
            newbattPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_25.gif")
        elif(BATst == "Dead"):
            newbattPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_0.gif")
        elif(BATst == "Overcharged"):
            newbattPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_Ovr.gif")
        else:
            newbattPic = PhotoImage(file=r"/home/pi/Documents/WeatherStation/Pictures/Batt_Unk.gif")                     
    if newbattPic != battPic and newbattPic != 0:
        battPic = newbattPic
        statuslabel = Label(MainWindow, relief="sunken", image=battPic)
        statuslabel.place(x=width_value-130, y=0)

# *** weather station data handling
def weatherData(data1):
    BATst = '0'
    if (data1[0]!='-1'):               #Only change values when receiving new data
        BATst = ArduinoFunctions.getBatStatus(int(data1[6]))
        #print("Moteino Battery Level: ",BATst)
        hum = int(data1[1])                                                  #humidity
        photoresistor = int(data1[7])                                        #photoresistor
        rainy = ArduinoFunctions.getRainVolume(float(data1[2]))                #precipitation
        try:
            temp = round(float(data1[0]) * 9/5 + 32, 0)                            #temperature converted from C to F, rounded
        except(ValueError):
            temp = round(float(data1[0][-4:]) * 9/5 + 32, 0) 
        precipitation = ArduinoFunctions.getSnow(int(data1[5]), temp, hum)   #snow fall
        windD = ArduinoFunctions.getWindDirection(int(data1[4]))             #wind direction
        windSpeed = round(ArduinoFunctions.getWindSpeed(int(data1[3])), 0)   #wind speed
            
        windy = (windD,windSpeed,"mi/hr")                               #format for wind output
            
        hum_text.set("Humidity:{}".format(hum))
        temp_text.set("Temperature:{}°F".format(temp))
        windy_text.set("wind:{}{}{}".format(*windy))
            
        print(BATst, hum, photoresistor, rainy, temp, precipitation, windD, windSpeed, windy)
        #rain_text.set("Rain:{}".format(rainy))
        return BATst, hum, photoresistor, rainy, temp, precipitation, windD, windSpeed, windy
    
    return data1[0]
    
# *** Puts weather condition icon on left and places the corresponding text under date/time
def weatherStat(hum, photoresistor, rainy, precipitation):
    global cnd
    print("weather photoresistor: " , photoresistor)
    if photoresistor < 400:
        if (cnd != '2'): #if repeated, then don't update
            label1.grid(row=1, sticky="sw")
            labelS.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
            cnd = '2'
    elif photoresistor >= 400 and rainy == 0:
        if (cnd != '4'):
            label2.grid(row=1, sticky="sw")
            labelC.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
            cnd = '4'
    elif precipitation == "freezing, possible sleet" or precipitation ==  "possible snow":
        if (cnd != '8'):
            label3.grid(row=1, sticky="sw")
            labelSS.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
            cnd = '8'
    elif rainy != 0:
        if (cnd != '1'):
            label4.grid(row=1, sticky="sw")
            labelR.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nwse")
            cnd = '1'
    else :
            print ("Error")

# ***Humidity, temp and wind speed/direction always placed at bottom of the grid
hum_text = tk.StringVar(MainWindow)
humidity = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 40 normal", bg="royalblue4", fg="deepskyblue", textvariable=hum_text, width=15)
humidity.grid(row=10, column=1, sticky="ew")

temp_text = tk.StringVar(MainWindow)
temperature = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 40 normal", bg="royalblue4", fg="deepskyblue", textvariable=temp_text)
temperature.grid(row=10, column=0, sticky="ew")

windy_text = tk.StringVar(MainWindow)
wind = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 40 normal", bg="royalblue4", fg="deepskyblue", textvariable=windy_text)
wind.grid(row=10, column=2, sticky="ew")

# *** continuously poll weather data and button presses and update gui
polling(MainWindow)              

MainWindow.mainloop()