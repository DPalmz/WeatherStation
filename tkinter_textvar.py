import tkinter as tk

def eevee():
	text_var.set('The counter is {}!'.format(int(text_var.get()[15:-1])+1))
	print(text_var.get())
	return

okno = tk.Tk()
text_var = tk.StringVar(okno)
tk.Label(okno, textvariable=text_var).pack()
text_var.set('The counter is {}!'.format(0))
print(text_var.get())
tk.Button(okno, text = "Refresh!", command=eevee).pack()
okno.mainloop()
