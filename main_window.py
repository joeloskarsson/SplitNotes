import tkinter
from tkinter import messagebox

import socket
import os

import config
import ls_connection as con
import note_reader as noter

runtime_info = {
				"ls_connected": False,
				"timer_running": False,
				"icon_active": False,
				"active_split": -1,
				"notes": [],
				"double_layout": False
				}

root = tkinter.Tk()

red_path= os.path.join(
					str(os.path.dirname(os.path.realpath(__file__))), 
					config.ICON_FOLDER, 
					config.ICONS["RED"]
					)
green_path= os.path.join(
					str(os.path.dirname(os.path.realpath(__file__))), 
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
		connection_ok = con.ls_connect(com_socket, server_found, window)
	else:
		#is_connected
		if runtime_info["notes"]:
			#notes loaded
			
			#get index of current split
			new_index = con.get_split_index(com_socket)
			
			if isinstance(new_index, bool):
				#Connection error
				test_connection(com_socket)
			else:
				#index retrieved succesfully
				if new_index == -1:
					#timer not running
					if runtime_info["timer_running"]:
						runtime_info["timer_running"] = False
						runtime_info["active_split"] = new_index
						update_notes(window, text1, text2, new_index)
						set_title_notes(window, 0)
				else:
					#timer is running
					runtime_info["timer_running"] = True
					
					if not runtime_info["active_split"] == new_index:
						#new split, need to update
					
						#update notes
						update_notes(window, text1, text2, new_index)
						
						#set new window title
						new_split = con.get_split_name(com_socket)
						
						if new_split:
							set_title_notes(window, new_index, new_split)
						else:
							#connection error
							set_title_notes(window, new_index)
							test_connection(com_socket)
							
						runtime_info["active_split"] = new_index

		else:
			#notes not yet loaded
			if not con.check_connection(com_socket):
				#connection lost
				runtime_info["ls_connected"] = False
				update_icon(False, window)
				com_socket = con.init_socket()
			
	
	
	#self looping
	window.after(int(config.POLLING_TIME * 1000), update, window, com_socket, text1, text2)					
	
	
def test_connection(com_socket):
	if con.check_connection(com_socket):
		return True
	else:
		reset_connection(com_socket)
		return False


def reset_connection(com_socket):
	runtime_info["ls_connected"] = False
	com_socket = con.init_socket()
	

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

	
def menu_load_notes(window, text1, text2):
	"""Menu selected load notes option."""
	load_notes(window, text1, text2)
		
		
def load_notes(window, text1, text2):
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

			update_notes(window, text1, text2, runtime_info["active_split"])
			set_title_notes(window, 0, split_name = False)
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

		
def right_arrow(window, text1, text2):
	"""Event handler for right arrow key."""
	change_preview(window, text1, text2, 1)
	
	
def left_arrow(window, text1, text2):
	"""Event handler for left arrow key."""
	change_preview(window, text1, text2, -1)


def change_preview(window, text1, text2, move):
	"""move is either 1 for next or -1 for previous."""
	if runtime_info["notes"] and (not runtime_info["timer_running"]):
		max_index = (len(runtime_info["notes"]) - 1)
		index = runtime_info["active_split"]
		
		if index < 0:
			index = 0
			
		index += move
		
		if index > max_index:
			index = max_index
		
		update_notes(window, text1, text2, index)
		runtime_info["active_split"] = index
		
		if index < 0:
			index = 0
		set_title_notes(window, index)
	
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
	
def init_UI(root):
	"""Draws default UI and creates event bindings."""
	
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
						wrap=tkinter.WORD
						)
	text1.insert(tkinter.END, config.DEFAULT_MSG)
	text1.config(state=tkinter.DISABLED)
	text1.pack(fill=tkinter.BOTH, expand=True)

	text2 = tkinter.Text(
						box2, 
						yscrollcommand=scroll2.set, 
						wrap=tkinter.WORD
						)
	text2.insert(tkinter.END, config.DEFAULT_MSG)
	text2.config(state=tkinter.DISABLED)
	text2.pack(fill=tkinter.BOTH, expand=True)

	scroll1.config(command=text1.yview)
	scroll2.config(command=text2.yview)
	
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
					label=config.MENU_OPTIONS["LOAD"], 
					command=(lambda: menu_load_notes(root, text1, text2))
					)
	
	
	#Set default window icon and title
	root.tk.call('wm', 'iconphoto', root._w, red_icon)
	update_title(config.DEFAULT_WINDOW["TITLE"], root)
	
	#Event binds
	root.bind("<Configure>", (lambda e: adjust_content(root, box1, box2)))
	root.bind("<Button-3>", (lambda e: show_popup(e, popup)))
	root.bind("<Right>", (lambda e: right_arrow(root, text1, text2)))
	root.bind("<Left>", (lambda e: left_arrow(root, text1, text2)))
	
	#call update loop
	com_socket = con.init_socket()
	update(root, com_socket, text1, text2)
	

init_UI(root)

root.mainloop()