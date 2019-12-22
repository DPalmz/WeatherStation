from tkinter import *
from PIL import ImageTk,Image
MainWindow = Tk()
MainWindow.title("Matching game")  # the name of the window
Canvas=Canvas(MainWindow,width= 500,height=500, bg="white")
Canvas.pack()
import random
for x in range(1):
   x= random.randint(1,10)
   print(x)
if x > 5:
    Rightresize=Image.open("RIGHT.gif").resize((500,500),Image.ANTIALIAS)
    Right=ImageTk.PhotoImage(Rightresize)
    Canvas.create_image(0,-50,image =Right,anchor =NW)
    MainWindow.after(2000, lambda: MainWindow.destroy())
else:
    Wrongresize=Image.open("WRONG.gif").resize((500,500),Image.ANTIALIAS)
    Right=ImageTk.PhotoImage(Wrongresize)
    Canvas.create_image(0,-50,image =Right,anchor =NW)
MainWindow.after(2000,lambda:MainWindow.destroy())




MainWindow.mainloop()