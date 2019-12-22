from tkinter import *
from PIL import ImageTk,Image

MainWindow = Tk()
MainWindow.title("Coastal Connections Weather Station")  # the name of the window
width_value=MainWindow.winfo_screenwidth()    # line4-5  automatically sets the window  fullsize based on the resolution of the screen used
height_value=MainWindow.winfo_screenheight()
MainWindow.geometry("%dx%d+0+0" %(width_value,height_value))

C=Canvas(MainWindow,width= width_value,height=height_value, bg="blue")
C.pack()
img=Image.open("BGW.gif").resize((width_value,height_value),Image.ANTIALIAS)
pic=ImageTk.PhotoImage(img)
C.create_image(0,-50,image =pic,anchor =NW)


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
def DATE():
    today=date.today()
    cdate=today.strftime("%b %d, %Y")
    MainWindow.after(1000,date)
    DateLabel =Label(MainWindow,bd=4 ,relief = "sunken" ,font = "HelveticaNeue 60 bold",bg="ghostwhite",fg ="deepskyblue", text= cdate,anchor=CENTER,width= 15)
    DateLabel.place(x=800,y=303)

import random
for x in range(1):
  print (random.randint(1,1024))
  if x > 500:
         photo1 = PhotoImage(file="sunnyicon2.gif")
         label1 = Label(MainWindow, image=photo1)
         label1.place(x=0, y=70)
         labelS = Label(MainWindow, bd=4, relief="flat", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue", text="Sunny" )
         labelS.place(x=780, y=420)
else :
    photo3 = PhotoImage(file="cloudyicon.gif")
    label3 = Label(MainWindow, image=photo3)
    label3.place(x=0, y=70)
    labelC = Label(MainWindow, bd=4, relief="sunken", font="HelveticaNeue 90 normal", bg="ghostwhite", fg="deepskyblue",
                   text="cloudy")
    labelC.place(x=680, y=420)

MainWindow.mainloop()