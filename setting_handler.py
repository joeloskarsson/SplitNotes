import tkinter.colorchooser as colorchooser
from tkinter import messagebox as msgbox
import tkinter
import os
import sys

import config

settings_path = os.path.join(
	str(os.path.dirname(os.path.realpath(sys.argv[0]))),
	config.RESOURCE_FOLDER,
	config.SETTINGS_FILE
)

settings_icon_path = os.path.join(
	str(os.path.dirname(os.path.realpath(sys.argv[0]))),
	config.RESOURCE_FOLDER,
	config.ICONS["SETTINGS"]
)


def load_settings():
	"""
	Tries to load settings from file.
	If no working settings-file exist one is created and the default settings are returned.
	
	returns a dictionary with all settings.
	"""

	# try to open default settings file
	try:
		settings_file = open(settings_path, "r+")
		settings_content = get_file_lines(settings_file)
	except:
		# File not found
		settings_content = set_default_settings();

	settings = format_settings(settings_content)

	# Check so settings file has all settings
	if not validate_settings(settings):
		settings = format_settings(set_default_settings())

	return settings


def set_default_settings():
	"""
	Creates a config file with default settings. 
	Returns the default config-file content.
	"""
	set_settings_file_content(config.DEFAULT_CONFIG)
	return config.DEFAULT_CONFIG.split("\n")


def format_settings(file_rows):
	"""
	Takes a list of settings (as written in config files) and 
	formats it to a dictionary.
	
	Returns a dictionary with all settings as keys.
	"""
	SETTING_PART_LENGTH = 2

	settings = {}

	for row in file_rows:
		row = row.strip("\n")
		parts = row.split("=", 1)

		if len(parts) == SETTING_PART_LENGTH:
			# Strip to remove whitespace at end and beginning
			settings[parts[0].strip()] = parts[1].strip()

	return settings


def get_file_lines(file):
	"""
	Returns a list containing all the lines of the gicen file.
	"""
	# read file line per line
	f_lines = []
	keep_reading = True
	while keep_reading:
		cur_line = file.readline()

		if cur_line:
			f_lines.append(cur_line)
		else:
			keep_reading = False

	return f_lines


def validate_settings(settings):
	"""
	Checks a settings dictionary so that all the needed settings are present.
	"""

	for req_setting in config.REQUIRED_SETTINGS:
		if not (req_setting in settings):
			return False

	if not validate_font_size(settings["font_size"]):
		return False

	if not validate_server_port(settings["server_port"]):
		return False

	if not validate_color(settings["text_color"]):
		return False

	if not validate_color(settings["background_color"]):
		return False

	if not (settings["font"] in config.AVAILABLE_FONTS):
		return False

	if not ((settings["double_layout"] == "True") or
				(settings["double_layout"] == "False")):
		return False

	return True


def set_settings_file_content(content):
	"""
	Saves given content to the config file, config.cfg, in the resources directory.
	"""
	settings_file = open(settings_path, "w")
	settings_file.write(content)
	settings_file.close()


def edit_settings(root_wnd, apply_method):
	"""
	Sets up a window for editing settings.
	root_wnd is the main window that settings should be applied to.
	apply_method is the method to be called to apply validated settings.
	"""
	settings_wnd = tkinter.Toplevel(master=root_wnd,
									width=config.SETTINGS_WINDOW["WIDTH"],
									height=config.SETTINGS_WINDOW["HEIGHT"])
	settings_wnd.title(config.SETTINGS_WINDOW["TITLE"])
	settings_icon = tkinter.Image("photo", file=settings_icon_path)
	settings_wnd.tk.call('wm', 'iconphoto', settings_wnd._w, settings_icon)

	settings = load_settings()

	settings_wnd.resizable(0, 0)

	font_label = tkinter.Label(settings_wnd,
							   text=config.SETTINGS_OPTIONS["FONT"],
							   font=config.GUI_FONT)
	font_size_label = tkinter.Label(settings_wnd,
									text=config.SETTINGS_OPTIONS["FONT_SIZE"],
									font=config.GUI_FONT)
	text_color_label = tkinter.Label(settings_wnd,
									 text=config.SETTINGS_OPTIONS["TEXT_COLOR"],
									 font=config.GUI_FONT)
	bg_color_label = tkinter.Label(settings_wnd,
								   text=config.SETTINGS_OPTIONS["BG_COLOR"],
								   font=config.GUI_FONT)
	layout_label = tkinter.Label(settings_wnd,
								   text=config.SETTINGS_OPTIONS["DOUBLE_LAYOUT"],
								   font=config.GUI_FONT)
	port_label = tkinter.Label(settings_wnd,
								   text=config.SETTINGS_OPTIONS["SERVER_PORT"],
								   font=config.GUI_FONT)
	default_port_label = tkinter.Label(settings_wnd,
								   text=config.SETTINGS_OPTIONS["DEFAULT_SERVER_PORT"],
								   font=config.GUI_FONT)


	# Font Selection
	selected_font = tkinter.StringVar(settings_wnd)
	selected_font.set(settings["font"])

	font_dropdown = tkinter.OptionMenu(settings_wnd,
									   selected_font,
									   *config.AVAILABLE_FONTS)
	font_dropdown.configure(font=config.GUI_FONT)

	# Font Size Selection
	font_size_entry = tkinter.Entry(settings_wnd, width=2, font=config.GUI_FONT)
	font_size_entry.insert(0, settings["font_size"])

	# Text Color Selection
	text_color = tkinter.Button(settings_wnd,
								width=3,
								height=1,
								)

	if validate_color(settings["text_color"]):
			text_color.configure(background=settings["text_color"])
	else:
		text_color.configure(background="#000000")

	def text_color_selection():
		choosen_color = colorchooser.askcolor()
		if choosen_color[1]:
			settings["text_color"] = choosen_color[1]
			text_color.configure(background=settings["text_color"])

		settings_wnd.focus_force()

	text_color.configure(command=text_color_selection)

	# Background color Selection
	bg_color = tkinter.Button(settings_wnd,
								width=3,
								height=1,
								)

	if validate_color(settings["background_color"]):
			bg_color.configure(background=settings["background_color"])
	else:
		bg_color.configure(background="#FFFFFF")

	def bg_color_selection():
		choosen_color = colorchooser.askcolor()
		if choosen_color[1]:
			settings["background_color"] = choosen_color[1]
			bg_color.configure(background=settings["background_color"])

		settings_wnd.focus_force()

	bg_color.configure(command=bg_color_selection)

	# Server port Selection
	port_entry = tkinter.Entry(settings_wnd, width=6, font=config.GUI_FONT)
	port_entry.insert(0, settings["server_port"])

	# Double Layout Selection
	double_layout = tkinter.BooleanVar()
	double_layout_btn = tkinter.Checkbutton(settings_wnd, variable=double_layout)

	if decode_boolean_setting(settings["double_layout"]):
		double_layout_btn.select()

	# Save and cancel buttons
	def control_and_save():
		errors_found = False

		settings["font"] = selected_font.get()

		chosen_font_size = font_size_entry.get()
		chosen_port = port_entry.get()

		settings["double_layout"] = encode_boolean_setting(double_layout.get())

		if not validate_font_size(chosen_font_size):
			msgbox.showerror(config.ERRORS["FONT_SIZE"][0], config.ERRORS["FONT_SIZE"][1])
			errors_found = True
		else:
			settings["font_size"] = chosen_font_size

		if not validate_server_port(chosen_port):
			msgbox.showerror(config.ERRORS["SERVER_PORT"][0], config.ERRORS["SERVER_PORT"][1])
			errors_found = True
		else:
			settings["server_port"] = chosen_port

		if not errors_found:
			save_settings(settings)
			apply_method(settings)
			settings_wnd.destroy()
		else:
			settings_wnd.focus_force()

	save_btn = tkinter.Button(settings_wnd,
							  	command=control_and_save,
							  	text=config.SETTINGS_WINDOW["SAVE"],
							  	font=config.GUI_FONT)
	cancel_btn = tkinter.Button(settings_wnd,
								command=settings_wnd.destroy,
								text=config.SETTINGS_WINDOW["CANCEL"],
								font=config.GUI_FONT)

	# Place all components
	font_label.place(x=15, y=15)
	font_size_label.place(x=15, y=55)
	text_color_label.place(x=15, y=95)
	bg_color_label.place(x=15, y=135)
	layout_label.place(x=15, y=175)
	port_label.place(x=15, y=215)
	default_port_label.place(x=15, y=240)

	font_dropdown.place(x=178, y=15)
	font_size_entry.place(x=180, y=55)
	text_color.place(x=180, y=95)
	bg_color.place(x=180, y=135)
	double_layout_btn.place(x=180, y=175)
	port_entry.place(x=180, y=215)

	save_btn.place(x=110, y=280)
	cancel_btn.place(x=190, y=280)


def validate_color(color):
	"""
	Returns whether or not given color is valid in the hexadecimal format.
	"""
	return isinstance(color, str) and len(color) == 7 and color[0] == "#"


def validate_font_size(size):
	"""
	Returns whether or not given size is an acceptable font size.
	"""
	try:
		size = int(size)
	except:
		return False

	return 0 < size < 70


def validate_server_port(port):
	"""
	Returns Whether or not gicen port is a valid server port.
	"""
	try:
		port = int(port)
		return True
	except:
		return False


def save_settings(settings):
	file_content = ""

	for key in settings.keys():
			file_content += key + "=" + settings[key] + "\n"

	set_settings_file_content(file_content)


def decode_boolean_setting(setting):
	return setting == "True"

def encode_boolean_setting(value):
	if value:
		return "True"
	else:
		return "False"
