import tkinter
from tkinter import messagebox
from tkinter import font

import socket
import os
import sys

import config
import ls_connection as con
import note_reader as noter

runtime_info = {
				"ls_connected": False,
				"timer_running": False,
				"icon_active": False,
				"active_split": -1,
				"notes": [],
				"double_layout": False,
				"big_font": False
				}

root = tkinter.Tk()

red_path= os.path.join(
					str(os.path.dirname(os.path.realpath(sys.argv[0]))), 
					config.ICON_FOLDER, 
					config.ICONS["RED"]
					)
green_path= os.path.join(
					str(os.path.dirname(os.path.realpath(sys.argv[0]))), 
					config.ICON_FOLDER, 
					config.ICONS["GREEN"]
					)
red_icon = tkinter.Image("photo", file=red_path)
green_icon = tkinter.Image("photo", file=green_path)

def update(window, com_socket, text1, text2):
	"""
	Function to loop along tkinter mainloop.
	"""
	if not runtime_info["ls_connected"]:
		#try connecting to ls
		con.ls_connect(com_socket, server_found, window)
	else:
		#is_connected
		if runtime_info["notes"]:
			#notes loaded
			
			#get index of current split
			new_index = con.get_split_index(com_socket)
			
			if isinstance(new_index, bool):
				#Connection error
				com_socket = test_connection(com_socket, window, text1, text2)
			else:
				#index retrieved succesfully
				if new_index == -1:
					#timer not running
					if runtime_info["timer_running"]:
						runtime_info["timer_running"] = False
						runtime_info["active_split"] = new_index
						update_GUI(window, com_socket, text1, text2)
				else:
					#timer is running
					if not runtime_info["timer_running"]:
						runtime_info["timer_running"] = True
						
						#special case to fix scrolling
						if runtime_info["active_split"] == 0:
							runtime_info["active_split"] = -1
					
					if not runtime_info["active_split"] == new_index:
						#new split, need to update
						runtime_info["active_split"] = new_index
						
						update_GUI(window, com_socket, text1, text2)					
		else:
			#notes not yet loaded
			com_socket = test_connection(com_socket, window, text1, text2)
				
	
	
	#self looping
	window.after(int(config.POLLING_TIME * 1000), update, window, com_socket, text1, text2)


def	update_GUI(window, com_socket, text1, text2):
	"""
	Updates all graphics according to current runtime_info.
	Sets window title and Text-box content.
	Does NOT set window icon.
	"""
	index = runtime_info["active_split"]
	
	if index == -1:
		index = 0
	
	if runtime_info["timer_running"]:
		#Does not test connection if it fails
		split_name = con.get_split_name(com_socket)
	else:
		split_name = False
	
	if runtime_info["notes"]:
		set_title_notes(window, index, split_name)
		update_notes(window, text1, text2, index)
	else:
		update_title(config.DEFAULT_WINDOW["TITLE"], window)
	
	
def test_connection(com_socket, window, text1, text2):
	"""
	Runs a connection test to ls using given socket.
	If test is unsuccessful, resets connection.
	Returns a socket that should be used for communication with ls.
	"""
	if con.check_connection(com_socket):
		return com_socket
	else:
		return reset_connection(com_socket, window, text1, text2)


def reset_connection(com_socket, window, text1, text2):
	"""
	Resets all variables and closes given socket.
	Updates GUI to respond to connection loss.
	Returns a fresh socket that can be used to connect to ls.
	"""
	if runtime_info["timer_running"]:
		runtime_info["timer_running"] = False
		runtime_info["active_split"] = -1
	
	runtime_info["ls_connected"] = False
	
	update_icon(False, window)
	update_GUI(window, com_socket, text1, text2)
	
	#Close old and return a fresh socket
	con.close_socket(com_socket)
	return con.init_socket()
	

def server_found(window):
	"""
	Executes correct settings for when 
	ls connection has been established.
	"""
	runtime_info["ls_connected"] = True
	update_icon(True, window)

	
def update_icon(active, window):
	"""Updates icon of window depending on "active" variable"""
	if active and not runtime_info["icon_active"]:
		window.tk.call('wm', 'iconphoto', window._w, green_icon)
		runtime_info["icon_active"] = True
	elif runtime_info["icon_active"]:
		window.tk.call('wm', 'iconphoto', window._w, red_icon)
		runtime_info["icon_active"] = False
		
	
def update_title(name, window):
	"""Sets the title of given window to name."""
	window.wm_title(name)
	
	
def adjust_content(window, box1, box2):
	"""
	Adjusts size of box1 and box2 according to 
	layout and size of window.
	"""
	if runtime_info["double_layout"]:
		set_double_layout(window, box1, box2)
	else:
		set_single_layout(window, box1, box2)
	
		
def set_double_layout(window, box1, box2):
	"""
	Configures boxes in the window to fit as in double layout.
	"""
	runtime_info["double_layout"] = True
	
	w_width = window.winfo_width()
	w_height = window.winfo_height()
	
	box1.place(height=(w_height // 2), width=w_width)
	box2.place(height=(w_height // 2), width=w_width, y=(w_height // 2))
		

def set_single_layout(window, box1, box2):
	"""
	Configures boxes in the window to fit as in single layout.
	"""
	runtime_info["double_layout"] = False
	
	box2.place_forget()
	box1.place(height=window.winfo_height(), width=window.winfo_width())

	
def show_popup(event, menu):
	"""Displays given popup menu at cursor position."""
	menu.post(event.x_root, event.y_root)
	
	
def menu_change_layout(window, box1, box2, popup):
	"""Menu option for changing layout selected."""
	if runtime_info["double_layout"]:
		set_single_layout(window, box1, box2)
		popup.entryconfig(0, label=config.MENU_OPTIONS["DOUBLE"])
	else:
		set_double_layout(window, box1, box2)
		popup.entryconfig(0, label=config.MENU_OPTIONS["SINGLE"])

	
def menu_load_notes(window, text1, text2, com_socket):
	"""Menu selected load notes option."""
	load_notes(window, text1, text2, com_socket)
		
		
def load_notes(window, text1, text2, com_socket):
	"""
	Prompts user to select notes and then tries to load these into the UI.
	"""
	file = noter.select_file()
	
	if file:	
		notes = noter.get_notes(file)
		if notes:
			#Notes loaded correctly
			runtime_info["notes"] = notes
			
			split_c = len(notes)
			show_info(("Notes Loaded", ("Loaded notes with " + str(split_c) + " splits.")))
			
			if not runtime_info["timer_running"]:
				runtime_info["active_split"] = -1
				
			update_GUI(window, com_socket, text1, text2)
			
		else:
			show_info(config.ERRORS["NOTES_EMPTY"], True)

			
def show_info(info, warning = False):
	"""
	Displays an infor popup window.
	if warning is True window has a warning triangle.
	"""
	if warning:
		messagebox.showwarning(info[0], info[1])
	else:
		messagebox.showinfo(info[0], info[1])
		
		
def update_notes(window, text1, text2, index):
	"""
	Displays notes with the given index in given text widgets.
	If index is lower than 0, displays notes for index 0.
	If index is higher than the highest index there are 
	notes for the text widgets are left empty.
	
	text2 is always given the notes at index (index + 1) if existing
	"""
	max_index = (len(runtime_info["notes"]) - 1)
	
	if index < 0:
		index = 0
	
	text1.config(state=tkinter.NORMAL)
	text2.config(state=tkinter.NORMAL)
	
	text1.delete("1.0", tkinter.END)
	text2.delete("1.0", tkinter.END)
	
	if index <= max_index:
		text1.insert(tkinter.END, runtime_info["notes"][index])
		
		#cand disply notes for index+1
		if index < max_index:
			text2.insert(tkinter.END, runtime_info["notes"][index + 1])
			
	text1.config(state=tkinter.DISABLED)
	text2.config(state=tkinter.DISABLED)

		
def right_arrow(window, com_socket, text1, text2):
	"""Event handler for right arrow key."""
	change_preview(window, com_socket, text1, text2, 1)
	
	
def left_arrow(window, com_socket, text1, text2):
	"""Event handler for left arrow key."""
	change_preview(window, com_socket, text1, text2, -1)


def change_preview(window, com_socket, text1, text2, move):
	"""move is either 1 for next or -1 for previous."""
	if runtime_info["notes"] and (not runtime_info["timer_running"]):
		max_index = (len(runtime_info["notes"]) - 1)
		index = runtime_info["active_split"]
		
		if index < 0:
			index = 0
			
		index += move
		
		if index > max_index:
			index = max_index
		
		runtime_info["active_split"] = index
		
		update_GUI(window, com_socket, text1, text2)
	
def set_title_notes(window, index, split_name = False):
	"""
	Set window title to fit with displayed notes.
	"""
	title = config.DEFAULT_WINDOW["TITLE"]
	
	disp_index = str(index + 1) #start at 1
	title += " - " + disp_index
	
	if split_name:
		title += " - " + split_name
	
	if runtime_info["timer_running"]:
		title += " - " + config.RUNNING_ALERT
	
	update_title(title, window)
	
	
def	menu_font_size(text_font, menu):
	if runtime_info["big_font"]:
		runtime_info["big_font"] = False
		menu.entryconfig(1, label=config.MENU_OPTIONS["BIG"])
	else:
		runtime_info["big_font"] = True
		menu.entryconfig(1, label=config.MENU_OPTIONS["SMALL"])
		
	update_font_size(text_font)
	
def update_font_size(text_font):
	if runtime_info["big_font"]:
		font_size = config.FONT["BIG"]
	else:
		font_size = config.FONT["SMALL"]
		
	text_font.config(size=font_size)

def init_UI(root):
	"""Draws default UI and creates event bindings."""
	
	#Create communication socket
	com_socket = con.init_socket()
	
	#Graphical components
	root.geometry(str(config.DEFAULT_WINDOW["WIDTH"]) + "x" + str(config.DEFAULT_WINDOW["HEIGHT"]))
	
	box1 = tkinter.Frame(root)
	box2 = tkinter.Frame(root)

	scroll1 = tkinter.Scrollbar(box1)
	scroll1.pack(side=tkinter.RIGHT, fill=tkinter.Y)

	scroll2 = tkinter.Scrollbar(box2)
	scroll2.pack(side=tkinter.RIGHT, fill=tkinter.Y)


	text1 = tkinter.Text(
						box1, 
						yscrollcommand=scroll1.set, 
						wrap=tkinter.WORD,
						cursor="arrow"
						)
	text1.insert(tkinter.END, config.DEFAULT_MSG)
	text1.config(state=tkinter.DISABLED)
	text1.pack(fill=tkinter.BOTH, expand=True)

	text2 = tkinter.Text(
						box2, 
						yscrollcommand=scroll2.set, 
						wrap=tkinter.WORD,
						cursor="arrow"
						)
	text2.insert(tkinter.END, config.DEFAULT_MSG)
	text2.config(state=tkinter.DISABLED)
	text2.pack(fill=tkinter.BOTH, expand=True)

	scroll1.config(command=text1.yview)
	scroll2.config(command=text2.yview)
	
	#Set font and color for text
	text_font = font.Font(
						family=config.FONT["NAME"], 
						size=config.FONT["SMALL"]
						)
	text1.config(font=text_font)
	text2.config(font=text_font)
	text1.config(fg=config.COLOR["TEXT"], bg=config.COLOR["TEXT_BG"])
	text2.config(fg=config.COLOR["TEXT"], bg=config.COLOR["TEXT_BG"])
	
	set_single_layout(root, box1, box2)
	
	#create popup menu
	popup = tkinter.Menu(root, tearoff=0)
	popup.add_command(
					label=config.MENU_OPTIONS["DOUBLE"], 
					command=(
							lambda: menu_change_layout(root, box1, box2, popup)
							)
					) #Needs to be at index 0
	popup.add_command(
					label=config.MENU_OPTIONS["BIG"], 
					command=(
							lambda: menu_font_size(text_font, popup)
							)
					) #Needs to be at index 1
	popup.add_command(
					label=config.MENU_OPTIONS["LOAD"], 
					command=(lambda: menu_load_notes(root, text1, text2, com_socket))
					)
	
	
	#Set default window icon and title
	root.tk.call('wm', 'iconphoto', root._w, red_icon)
	update_title(config.DEFAULT_WINDOW["TITLE"], root)
	
	#Event binds
	root.bind("<Configure>", (lambda e: adjust_content(root, box1, box2)))
	root.bind("<Button-3>", (lambda e: show_popup(e, popup)))
	root.bind("<Right>", (lambda e: right_arrow(root, com_socket, text1, text2)))
	root.bind("<Left>", (lambda e: left_arrow(root, com_socket, text1, text2)))
	
	#call update loop
	update(root, com_socket, text1, text2)
	

init_UI(root)

root.mainloop()