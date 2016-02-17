import tkinter
import os
import sys

import config

settings_path = os.path.join(
		str(os.path.dirname(os.path.realpath(sys.argv[0]))), 
		config.RESOURCE_FOLDER, 
		config.SETTINGS_FILE
		)

def load_settings():
	"""
	Tries to load settings from file.
	If no working settings-file exist one is created and the default settings are returned.
	
	returns a dictionary with all settings.
	"""

	#try to open default settings file
	try:
		settings_file = open(settings_path,"r+")
		settings_content = get_file_lines(settings_file)
	except:
		#File not found
		settings_content = set_default_settings();
		
	settings = format_settings(settings_content)
	
	#Check so settings file has all settings
	if not validate_settings(settings):
		settings = format_settings(set_default_settings())
	
	return settings
	
def set_default_settings():
	"""
	Creates a config file with default settings. 
	Returns the default config-file content.
	"""
	#TODO create file
	settings_file = open(settings_path, "w")
	settings_file.write(config.DEFAULT_CONFIG)
	settings_file.close()
	
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
		parts = row.split("=")
		
		if(len(parts) == SETTING_PART_LENGTH):
			settings[parts[0]] = parts[1]
		
		
	return settings
	
def get_file_lines(file):
	"""
	Returns a list containing all the lines of the gicen file.
	"""
	#read file line per line
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
		if not req_setting in settings:
			return False
			
	return True
	
	
def edit_settings(root_wnd, apply_method, text1, text2):
	settings_wnd = tkinter.Toplevel(master=root_wnd, 
									width=config.SETTINGS_WINDOW["WIDTH"], 
									height=config.SETTINGS_WINDOW["HEIGHT"])
	settings_wnd.title(config.SETTINGS_WINDOW["TITLE"])
	
	settings = load_settings()
	
	settings_wnd.resizable(0,0)
	
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
	
	font_label.place(x=15, y=15)
	font_size_label.place(x=15, y=45)
	text_color_label.place(x=15, y=75)
	bg_color_label.place(x=15, y=105)
	
	#Font Selection
	selected_font = tkinter.StringVar(settings_wnd)
	
	font_dropdown = tkinter.OptionMenu(settings_wnd, selected_font, "saker")
	font_dropdown.place(x=100, y=15)
	
	#TODO finish font selection and rest of gui
	
	def save_settings():
		#TODO collect settings
		#font = selected_font.get()
		settings = []
		
		apply_method(settings, text1, text2)
		settings_wnd.destroy()
		
	save_btn = tkinter.Button(settings_wnd, 
								command=save_settings, 
								text=config.SETTINGS_WINDOW["SAVE"])
	cancel_btn = tkinter.Button(settings_wnd, 
								command=settings_wnd.destroy,
								text=config.SETTINGS_WINDOW["CANCEL"])
	
	save_btn.place(x=10, y=10)
	cancel_btn.place(x=10, y=50)

	
