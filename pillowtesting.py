from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox


MainWindow = Tk()
width_value=MainWindow.winfo_screenwidth()    # line4-5  automatically sets the window  fullsize based on the resolution of the screen used
height_value=MainWindow.winfo_screenheight()
MainWindow.geometry("%dx%d+0+0" %(width_value,height_value))

C=Canvas(MainWindow,width= width_value,height=height_value, bg="blue")
C.pack()
img=Image.open("BGW.gif").resize((width_value,height_value),Image.ANTIALIAS)
pic=ImageTk.PhotoImage(img)
C.create_image(0,-50,image =pic,anchor =NW)
MainWindow.mainloop()

