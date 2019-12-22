from tkinter import *
from PIL import ImageTk,Image
import sys
import os
sys.path.append(os.path.abspath("/home/pi/Documents/WeatherStation"))
import ArduinoFunctions
connection1, name1 = ArduinoFunctions.connectSerial() #open serial ports
connection2, name2 = ArduinoFunctions.connectSerial()
MainWindow = Tk()


MainWindow.title("Coastal Connections Weather Station")  # the name of the window
width_value=MainWindow.winfo_screenwidth()    # line4-5  automatically sets the window  fullsize based on the resolution of the screen used
height_value=MainWindow.winfo_screenheight()
MainWindow.geometry("%dx%d+0+0" %(width_value,height_value))

C=Canvas(MainWindow,width= width_value,height=height_value, bg="blue")
C.pack()
img=Image.open("/home/pi/Documents/WeatherStation/BGW.gif").resize((width_value,height_value),Image.ANTIALIAS)
pic=ImageTk.PhotoImage(img)
C.create_image(0,-50,image =pic,anchor =NW)


data1  = ArduinoFunctions.readSerial(connection1, name1)

data2 = ArduinoFunctions.readSerial(connection2, name2)

BATst= "100% Full"
statuslabel = Label(MainWindow,text=BATst,bd=1,relief= "sunken",anchor=NW , width=width_value )    # this is just a simple status bar
statuslabel.place(x=0,y=0)                    # this just expands the status bar through the whole line
label0 = Label(MainWindow,bd=8 ,relief = "flat" ,font = "Times 22 bold",bg="ghostwhite",fg ="deepskyblue", text= "Weather Station")   # first label that appears is the name of the project
label0.pack(fill=X)

coast = PhotoImage(file="/home/pi/Documents/WeatherStation/coast.gif")
coast1 = Label(MainWindow, image=coast)
coast1.place(x=1590,y=70)

# *** this function calls the time libary which will be used to create a dyanmic digital clock **# line 12-19
import time as tm
def display_time():
    current_time= tm.strftime('%I:%M:%S:%p')
    labelTime['text'] =current_time
    MainWindow.after(1000,display_time)
labelTime= Label(MainWindow,bd=4 ,relief = "sunken" ,font = "HelveticaNeue 80 bold",bg="ghostwhite",fg ="deepskyblue", text= display_time,anchor=CENTER,width= 15)
labelTime.place(x=780,y=200)
display_time()
## this function is used to get and display the current date
from datetime import date
def display_date():
    today=date.today()
    cdate=today.strftime("%b %d, %Y")
    DateLabel['text']=cdate
    MainWindow.after(1000,display_date)
DateLabel = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 60 bold", bg="ghostwhite",  fg="deepskyblue", text=display_date, anchor=CENTER, width=15)
DateLabel.place(x=870, y=450)
display_date()
photoresistor = 0
rainy= 0
temp =0
hum= 0
#pres=
percipitation=0
windD=0
windSpeed = "N"
windy= (windD,windSpeed,"mi/hr")
if(name1 =="moteino"):
  
    photoresistor = data1[7]
    rainy= ArduinoFunctions.getRainVolume(data1[2])
    temp = ArduinoFunctions.data1[0]
    hum= ArduinoFunctions.data1[1]
    #pres=
    percipitation=ArduinoFunctions.getSnow(data1[5])
    windD=ArduinoFunctions.getWindDirection(data1[4])
    windSpeed =ArduinoFunctions.getWindSpeed(data1[3])
    windy= (windD,windSpeed,"mi/hr")

elif(name2 == "moteino"):
    photoresistor = data2[7]
    rainy= ArduinoFunctions.getRainVolume(data2[2])
    temp = ArduinoFunctions.data2[0]
    hum= ArduinoFunctions.data2[1]
    #pres=
    percipitation=ArduinoFunctions.getSnow(data2[5])
    windD=ArduinoFunctions.getWindDirection(data2[4])
    windSpeed =ArduinoFunctions.getWindSpeed(data2[3])
    windy= (windD,windSpeed,"mi/hr")

if photoresistor >1000:
         photo1 = PhotoImage(file="/home/pi/Documents/WeatherStation/sunnyicon2.gif")
         label1 = Label(MainWindow, image=photo1)
         label1.place(x=0, y=70)
         labelS = Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text="Sunny" )
         labelS.place(x=780, y=420)
elif photoresistor< 1000 and rainy==0 :
    photo3 = PhotoImage(file="/home/pi/Documents/WeatherStation/cloudyicon.gif")
    label3 = Label(MainWindow, image=photo3)
    label3.place(x=0, y=70)
    labelC = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue",
                   text="cloudy")
    labelC.place(x=680, y=420)
elif (precipitation == "freezing, possible sleet") or (percipitation==  "possible snow"):
        photo4 = PhotoImage(file="/home/pi/Documents/WeatherStation/snowyicon.gif")
        label4 = Label(MainWindow, image=photo4)
        label4.place(x=0,y=70)
        labelSS = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text="snowy")
        labelSS.place(x=680,y=420)
elif rainy !=0:
        photo2 = PhotoImage(file="/home/pi/Documents/WeatherStation/rainyicon.gif")
        label2 = Label(MainWindow, image=photo2)
        label2.place(x=0,y=70)
        labelR = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text="Rainy" )
        labelR.place(x=680,y=420)
else :
    print ("Error")

humidity= Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text="Humidity")
humidity.place(x=50,y=700)
humidlabel=Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text=hum)
humidlabel.place(x=320,y=700)
'''
pressure= Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text="Pressure:")
pressure.place(x=480,y=700)
pressurelabel=Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text=pres)
pressurelabel.place(x=747,y=700)
'''

wind= Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text="wind:")
wind.place(x=900,y=700)
windlabel=Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text=windy)
windlabel.place(x=1060,y=700)

MainWindow.mainloop()
