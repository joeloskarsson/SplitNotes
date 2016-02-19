import tkinter.filedialog as file_dia
import os.path as path

import config

"""
NOTE STANDARD FORMATTING

empty newlines separate notes for different splits

lines that start and end with [ ] are ignored for notes.
these can be used for titles. 
(ex. [Split1] is not included in notes)

all other lines of text are added as notes
"""


def get_note_lines(file_path):
	"""
	Reads file at given path and returns 
	a list containing all rows of text in given file.
	Returns false if file can not be read.
	"""

	# check so file isn't too big
	if path.getsize(file_path) > config.MAX_FILE_SIZE:
		return False

	try:
		notes_file = open(file_path, "r")
	except:
		return False

	# read file line per line
	f_lines = []
	keep_reading = True
	while keep_reading:

		try:
			cur_line = notes_file.readline()
		except:
			return False

		if cur_line:
			f_lines.append(cur_line)
		else:
			keep_reading = False

	return f_lines


def encode_notes(note_lines):
	"""
	Takes a list containing strings.
	Encodes given strings according to the note formatting.
	Returns the list containing the notes for every split. 
	"""

	def is_title(line):
		if not line:
			return False

		return (line[0] == "[") and (line[-1] == "]")

	def is_newline(line):
		return (line == "\n") or (line == "\r")

	def remove_new_line(line):
		if (len(line) >= 1) and (is_newline(line[-1])):
			return line[:-1]
		else:
			return line

	note_list = []
	cur_notes = ""

	for line in note_lines:
		# remove whitespace at beginning and end
		line = line.strip(" ")

		if is_newline(line):
			if cur_notes:
				note_list.append(cur_notes)
				cur_notes = ""
		else:
			line = remove_new_line(line)
			if not is_title(line):
				cur_notes += line + "\n"  # newline

	if cur_notes:
		note_list.append(cur_notes)

	return note_list


def get_notes(file_path):
	"""
	Takes a path to a file and returns a list with the notes 
	in the file encoded according to the note fromatting.
	
	Returns False if file is empty.
	"""
	note_lines = get_note_lines(file_path)

	if not note_lines:
		return False

	note_list = encode_notes(note_lines)

	return note_list


def select_file():
	"""
	Opens a file select window.
	Returns False upon no file selection.
	Otherwise returns absolute path to selected file.
	"""

	file = file_dia.askopenfilename(filetypes=config.TEXT_FILES)

	if file:
		return file
	else:
		return False


def file_exists(file):
	"""Checks if given path leads to an existing file."""
	return path.isfile(file)
