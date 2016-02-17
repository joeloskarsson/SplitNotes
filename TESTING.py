import tkinter
import setting_handler as s

#s.load_settings()

root = tkinter.Tk();

top = tkinter.Toplevel()

e = tkinter.Entry(top)
e.pack()

top.title("About this application...")

tkinter.mainloop()