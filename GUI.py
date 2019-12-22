from tkinter import *
from PIL import ImageTk,Image

MainWindow = Tk()
MainWindow.title("Coastal Connections Weather Station")  # the name of the window
width_value=MainWindow.winfo_screenwidth()    # line4-5  automatically sets the window  fullsize based on the resolution of the screen used
height_value=MainWindow.winfo_screenheight()
MainWindow.geometry("%dx%d+0+0" %(width_value,height_value))
# MainWindow.geometry("1000x600")
#MainWindow.minsize(width=1440, height=900)
#MainWindow.maxsize(width=1440, height=900)
C=Canvas(MainWindow,width= width_value,height=height_value, bg="blue")
C.pack()
img=Image.open("BGW.gif").resize((width_value,height_value),Image.ANTIALIAS)
pic=ImageTk.PhotoImage(img)
C.create_image(0,-50,image =pic,anchor =NW)

#background= PhotoImage(file="abstract-aqua-blue-clean-261403.gif")
#backgroundlabel = Label(MainWindow, image=background)
#backgroundlabel.place(x=-1000,y=-1200)
#MainWindow.configure(bg="green")
statuslabel = Label(MainWindow,text="battery Drained 20% ",bd=1,relief= "sunken",anchor=E  )    # this is just a simple status bar
statuslabel.pack(side=TOP,fill=X)                     # this just expands the status bar through the whole line
label0 = Label(MainWindow,bd=8 ,relief = "flat" ,font = "Times 22 bold",bg="ghostwhite",fg ="deepskyblue", text= "Weather Station")   # first label that appears is the name of the project
label0.pack(fill=X)

coast = PhotoImage(file="coast.gif")
coast1 = Label(MainWindow, image=coast)
coast1.place(x=1590,y=70)

# *** this function calls the time libary which will be used to create a dyanmic digital clock **# line 12-19
import time as tm
def display_time():
    current_time= tm.strftime('%I:%M:%S:%p')
    labelTime['text'] =current_time
    MainWindow.after(1000,display_time)
labelTime= Label(MainWindow,bd=4 ,relief = "sunken" ,font = "HelveticaNeue 80 bold",bg="ghostwhite",fg ="deepskyblue", text= display_time,anchor=CENTER,width= 15)
labelTime.place(x=800,y=200)
display_time()
## this function is used to get and display the current date
from datetime import date
def display_date():
    today=date.today()
    cdate=today.strftime("%b %d, %Y")
    DateLabel['text']=cdate
    MainWindow.after(1000,display_date)
DateLabel = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 60 bold", bg="ghostwhite",  fg="deepskyblue", text=display_date, anchor=CENTER, width=15)
DateLabel.place(x=800, y=303)
display_date()



inputdata= input("what is the weather :")
temp= input("what is the temperature :")
try:
    if inputdata == "sunny":
        photo1 = PhotoImage(file="sunnyicon2.gif")
        label1 = Label(MainWindow, image=photo1)
        label1.place(x=0,y=70)
        labelS = Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 90 normal",bg="ghostwhite",  fg="deepskyblue", text=inputdata )
        labelS.place(x=780,y=420)
        labeltemp= Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text=temp + "F" )
        labeltemp.place(x=600 ,y=420)
    elif inputdata == "rainy":
        photo2 = PhotoImage(file="rainyicon.gif")
        label2 = Label(MainWindow, image=photo2)
        label2.place(x=0,y=70)
        labelR = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text=inputdata )
        labelR.place(x=680,y=420)
        labeltemp= Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text=temp + "F" )
        labeltemp.place(x=600,y=420)
    elif inputdata == "cloudy":
        photo3 = PhotoImage(file="cloudyicon.gif")
        label3 = Label(MainWindow, image=photo3)
        label3.place(x=0,y=70)
        labelC = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text=inputdata)
        labelC.place(x=680,y=420)
        labeltemp = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text=temp + " F")
        labeltemp.place(x=600,y=420)
    elif inputdata == "snowy":
        photo4 = PhotoImage(file="snowyicon.gif")
        label4 = Label(MainWindow, image=photo4)
        label4.place(x=0,y=70)
        labelSS = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text=inputdata)
        labelSS.place(x=680,y=420)
        labeltemp = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text=temp + "F")
        labeltemp.place(x=600,y=420)
    else:
        print("error")
except:
    photo2 = PhotoImage(file="rainyicon.gif")
    label2 = Label(MainWindow, image=photo2)
    label2.place(x=0, y=70)
    labelR = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue",
                   text=inputdata)
    labelR.place(x=680, y=420)
    labeltemp = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite",
                      fg="deepskyblue", text=temp + "F")
    labeltemp.place(x=600, y=420)
humidinput= input("what is the humidity:")
pressureinput=input("what is the pressure:")
windinput=input("what is the wind:")

humidity= Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text="Humidity:")
humidity.place(x=50,y=700)
humidlabel=Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text=humidinput)
humidlabel.place(x=320,y=700)

pressure= Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text="Pressure:")
pressure.place(x=480,y=700)
pressurelabel=Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text=pressureinput)
pressurelabel.place(x=747,y=700)

wind= Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text="wind:")
wind.place(x=900,y=700)
windlabel=Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 60 normal", bg="ghostwhite", fg="deepskyblue", text=windinput)
windlabel.place(x=1060,y=700)

MainWindow.mainloop()
