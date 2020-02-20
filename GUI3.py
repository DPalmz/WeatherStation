import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image
from datetime import date
from pydub import AudioSegment
from pydub.playback import play
import ArduinoFunctions
import altTab
import Feedback
import os
import resource
import sys
import time as tm
#import tracemalloc

#tracemalloc.start()

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
btnpress = 0                          #Button Box input and weather condition value to compare with
cnd = 0
counter = 0

#correctSound = AudioSegment.from_wav(sys.path[0] + "/Sounds/correct_Current.wav")
#incorrectSound = AudioSegment.from_wav(sys.path[0] + "/Sounds/wrong_Current.wav")

# *** Establish connection
connection1, name1, counter = ArduinoFunctions.connectSerial(counter) #open serial ports for button box and weather station
counter += 1
connection2, name2, counter = ArduinoFunctions.connectSerial(counter)  
   
# ***** Window setup *****
print("window setup")
MainWindow = tk.Tk()
MainWindow.attributes("-fullscreen", True)
MainWindow.title("Coastal Connections Weather Station")                     # the name of the window
width_value = MainWindow.winfo_screenwidth()                                 
height_value = MainWindow.winfo_screenheight()
#MainWindow.geometry("%dx%d+0+0" %(width_value,height_value))

'''
Can=Canvas(MainWindow, width=width_value, height=height_value, bg="blue")   # base window
Can.place(x=0, y=0)
img = Image.open(sys.path[0] + "/Pictures/BGW.gif").resize((width_value+10,height_value+10),Image.ANTIALIAS)
pic = ImageTk.PhotoImage(img)                                               # background image
Can.create_image(-5, -5, image=pic, anchor=NW)
'''

#canvas alternative
bgImg = Image.open(sys.path[0] + "/Pictures/BGW.gif")
bgImg = bgImg.resize((width_value+10,height_value+10),Image.ANTIALIAS)
bgPic = ImageTk.PhotoImage(bgImg)
bgLabel = Label(MainWindow, relief = "flat", image=bgPic)
bgLabel.place(x = 0, y = 0)

# *** Coastal Connections logo
img2 = Image.open(sys.path[0] + "/Pictures/coast.gif").resize((506,210),Image.ANTIALIAS)
coast = ImageTk.PhotoImage(img2)
coast1 = Label(MainWindow, image=coast)
coast1.grid(sticky="ns") 
print("Logo")

# *** Title
label0 = Label(MainWindow,  text="Weather Station", borderwidth=12, relief="groove", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue")
label0.grid(row=0, column=1, columnspan=2, sticky="n")
print("Title")

# *** Default Battery Status Images
battPic100 = ImageTk.PhotoImage(Image.open(sys.path[0] + "/Pictures/Batt_Full.gif"))
battPic80 = ImageTk.PhotoImage(Image.open(sys.path[0] + "/Pictures/Batt_75.gif"))
battPic50 = ImageTk.PhotoImage(Image.open(sys.path[0] + "/Pictures/Batt_50.gif"))
battPic20 = ImageTk.PhotoImage(Image.open(sys.path[0] + "/Pictures/Batt_25.gif"))
battPic0 = ImageTk.PhotoImage(Image.open(sys.path[0] + "/Pictures/Batt_0.gif"))
battPicOvr = ImageTk.PhotoImage(Image.open(sys.path[0] + "/Pictures/Batt_Ovr.gif"))
battPicUnk = ImageTk.PhotoImage(Image.open(sys.path[0] + "/Pictures/Batt_Unk.gif"))  

battStatLabel = Label(MainWindow, relief="sunken", image=battPicUnk)   #display battery level on top right of screen
battStatLabel.place(x=width_value-130, y=0)
print("Battery Images")

# *** Weather Condition Images
sunnyPic = PhotoImage(file=sys.path[0] + "/Pictures/sunnyicon2.gif")
cloudyPic = PhotoImage(file=sys.path[0] + "/Pictures/cloudyicon.gif")
snowyPic = PhotoImage(file=sys.path[0] + "/Pictures/snowyicon.gif")
rainyPic = PhotoImage(file=sys.path[0] + "/Pictures/rainyicon.gif")
weatherPic = Label(MainWindow, image=sunnyPic)
weatherPic.grid(row=1, sticky="sw")
print("Weather Images")

# *** Clock/Date
# *** f1 is a frame to add a grid within a single cell - aligns time, date, and weather condition text
f1 = Frame(MainWindow)
f1.grid(row=1, column=1, columnspan=2)
# sunnyLabel = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Sunny" )
# cloudyLabel = Label(f1, bd=4, relief="sunken", font="HeLveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Cloudy")
# snowyLabel = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Snowy")
# rainyLabel = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Rainy")
weatherLabel = Label(f1, bd=4, relief="sunken", font="HelveticaNeue 90 bold", bg="royalblue4", fg="deepskyblue", text="Sunny")
weatherLabel.grid(row=2, column=0, columnspan=2, sticky="nwse")

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

# *** Humidity, temp and wind speed/direction always placed at bottom of the grid
hum_text = tk.StringVar(MainWindow)
humidity = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 40 normal", bg="royalblue4", fg="deepskyblue", textvariable=hum_text, width=15)
humidity.grid(row=10, column=1, sticky="ew")

temp_text = tk.StringVar(MainWindow)
temperature = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 40 normal", bg="royalblue4", fg="deepskyblue", textvariable=temp_text)
temperature.grid(row=10, column=0, sticky="ew")

windy_text = tk.StringVar(MainWindow)
wind = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 40 normal", bg="royalblue4", fg="deepskyblue", textvariable=windy_text)
wind.grid(row=10, column=2, sticky="ew")

# *** Feedback Labels (Declared last to appear above other elements)
labelCheck = Label(MainWindow, font="HelveticaNeue 500 bold", bg="royalblue4", fg="limegreen", text = "✓") #Feedback indicator
labelCheckFlag = 0

# ***** DATA HANDLING *****
def polling(MainWindow):
    global data1
    global data2
    global labelCheckFlag
    global labelExFlag

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


    while True:
        data1 = ArduinoFunctions.readSerial(connection1, name1)      # get data from weather station and button box
        data2 = ArduinoFunctions.readSerial(connection2, name2)
        #snapshot1 = tracemalloc.take_snapshot()
        #print("data1: ", data1, "data2: ", data2)
        #print('Memory usage (data): {}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
        if (labelCheckFlag > 0):
            labelCheckFlag = labelCheckFlag - 1
        else:
            labelCheck.place_forget()
            print("Forget that!")
        if (name1 == "Moteino"):
            newData = weatherData(data1)         #BATst, hum, photoresistor, rainy, temp, precipitation, windD, windSpeed, windy                                       # update weather station data values
            buttonEvent(data2)
        elif (name2 == "Moteino"):
            newData = weatherData(data2)
            buttonEvent(data1)
        else:
            newData = [0, 0, 0, 0, 0, 0, 0] #in case the weather station is not connected
           
        if (newData != '-1'):   #if newData is valid then update labels
            #print('newData: ', newData)
            #print('Memory usage (before): {}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
            battStat(newData[0])                      # determine image for battery status and weather condition
            #print('Memory usage (battStatPolling): {}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
            weatherStat(newData[1], newData[2], newData[3], newData[6])
            #print('Memory usage (weatherStatPolling): {}\n'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
            MainWindow.update()
        
        #snapshot2 = tracemalloc.take_snapshot()
        #top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        #print(" Top 10 Differences ")
        #for stat in top_stats[:10]:
            #print(stat)
            
        #memory_tracker.print_diff()
    
# *** Puts battery status icon on top right of page
def battStat(BATst):
    global battPic
    ##print("Battery Level: ", BATst)
    #newbattPic = 0
    #if (data != '-1'):
    if(BATst == "100%"):
        battStatLabel.configure(image=battPic100)
    elif(BATst == "80%"):
        battStatLabel.configure(image=battPic80)
    elif(BATst == "50%"):
        battStatLabel.configure(image=battPic50)
    elif(BATst == "20%"):
        battStatLabel.configure(image=battPic20)
    elif(BATst == "Dead"):
        battStatLabel.configure(image=battPic0)
    elif(BATst == "Overcharged"):
        battStatLabel.configure(image=battPicOvr)
    else:
        battStatLabel.configure(image=battPicUnk)              
    #print('Memory usage (battStat): {}\n'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))

# *** Button i/o
def buttonEvent(data): 
    global labelCheckFlag
    global cnd

    btnpress = data
    #print('Memo/home/pi/Documents/WeatherStationry usage (buttonEvent): {}'.format(resource.getrusage(resource.RUSAGE_SELF)))
    print("button press = ", btnpress, "cnd = ", cnd)
    if(btnpress == cnd):#show correct if matches weather condition
        #play(correctSound) 
        labelCheck.configure(fg="limegreen", text="✓")
        labelCheck.place(x=width_value/3, y=height_value/5)    #place checkmark or ex at about center of the screen
        print("check placed")
        labelCheckFlag = 100
    elif(btnpress == '10'):
        altTab.altTab()
    elif(btnpress != '-1' and btnpress != '0'):
        #play(incorrectSound)   
        labelCheck.configure(fg="crimson", text = "✗")
        labelCheck.place(x=width_value/3, y=height_value/5)
        print("ex placed")
        labelCheckFlag = 100
    else:
        return
    MainWindow.update
    return

# *** weather station data handling
def weatherData(data1):
    BATst = '0'
    #print('Memory usage (weatherDataStart): {}'.format(resource.getrusage(resource.RUSAGE_SELF)))
    if (data1[0]!='-1'):               #Only change values when receiving new data
        BATst = ArduinoFunctions.getBatStatus(int(data1[6]))
        #print("Moteino Battery Level: ",BATst)
        hum = float(data1[1])                                                  #humidity
        photoresistor = int(data1[7])                                        #photoresistor
        rainy = ArduinoFunctions.getRainVolume(float(data1[2]))                #precipitation
        try:
            temp = round(float(data1[0]) * 9/5 + 32, 0)                            #temperature converted from C to F, rounded
        except(ValueError):
            temp = round(float(data1[0][-4:]) * 9/5 + 32, 0)
            print("Weather Data Error!")
        precipitation = ArduinoFunctions.getSnow(int(data1[5]), temp, hum)   #snow fall
        windD = ArduinoFunctions.getWindDirection(int(data1[4]))             #wind direction
        windSpeed = round(ArduinoFunctions.getWindSpeed(int(data1[3])), 0)   #wind speed
            
        windy = (windD,windSpeed,"mi/hr")                               #format for wind output
            
        hum_text.set("Humidity:{}".format(hum))
        temp_text.set("Temperature:{}°F".format(temp))
        windy_text.set("Wind:{}{}{}".format(*windy))
        #print(BATst, hum, photoresistor, rainy, temp, precipitation, windD, windSpeed, windy)
        #print('Memory usage (weatherDataEnd): {}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
        return BATst, hum, photoresistor, rainy, temp, precipitation, windD, windSpeed, windy
    
    return data1[0]
    
# *** Puts weather condition icon on left and places the corresponding text under date/time
def weatherStat(hum, photoresistor, rainy, precipitation):
    global cnd
    #print("weather photoresistor: " , photoresistor)
    if photoresistor < 400:                                                                     #sunny condition
        if (cnd != '2'):         #if the same condition is repeated, then don't update
            weatherPic.configure(image=sunnyPic)
            weatherLabel.configure(text="Sunny")
            
            cnd = '2'
    elif photoresistor >= 400 and rainy == 0:                                                  #cloudy condition
        if (cnd != '4'):
            weatherPic.configure(image=cloudyPic)
            weatherLabel.configure(text="Cloudy")
            
            cnd = '4'
    elif precipitation == "freezing, possible sleet" or precipitation ==  "possible snow":   #snowy condition
        if (cnd != '8'):
            weatherPic.configure(image=snowyPic)
            weatherLabel.configure(text="Snowy")
            
            cnd = '8'
    elif rainy != 0:                                                                        #rainy condition
        if (cnd != '1'):
            weatherPic.configure(image=rainyPic)
            weatherLabel.configure(text="Rainy")
            
            cnd = '1'
    else:
        return
        print ("Error")
    #print('Memory usage (weatherStat): {}\n'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))

# *** continuously poll weather data and button presses and update gui
polling(MainWindow)              

MainWindow.mainloop()