#CONFIG FILE WITH CONSTANTS

DEBUG = True

#Livesplit connection
HOST = "localhost"
PORT = 16834

#In network communication, time out after this time. (in seconds)
COM_TIMEOUT = 0.5

#Possible commands to send to LiveSplit
LS_COMMANDS = {
	"best_possible": "getbestpossibletime\r\n",
	"cur_split_index": "getsplitindex\r\n",
	"cur_split_name": "getcurrentsplitname\r\n"
}

#Default Window Size
DEFAULT_WINDOW = {"WIDTH": 400, "HEIGHT": 300, "TITLE": "SplitNotes"}

#Color Scheme
COLOR_SCHEME = {}

#Default Welcome Message
DEFAULT_MSG = "Right Click to Open Notes."

#Update time for polling livesplit and other actions (in seconds)
POLLING_TIME = 0.5

#file names and path of icons
ICON_FOLDER = "resources"
ICONS= {"GREEN": "green.png", "RED": "red.png"}

#Popup menu options
MENU_OPTIONS = {
				"SINGLE": "Set Single Layout", 
				"DOUBLE": "Set Double Layout", 
				"LOAD": "Load Notes",
				"BIG": "Big Font",
				"SMALL": "Small Font"
				}

#Error messages
ERRORS = {"NOTES_EMPTY": ("Error", "Notes empty or can't be loaded!")}

#Max file size for notes
MAX_FILE_SIZE = 1000000000 #1 Giga-Byte

#TO be added to title to alert user that timer is running
RUNNING_ALERT = "RUNNING"

#Font for notes
FONT = {"NAME": "Arial", "SMALL": 12, "BIG": 16}

#Color scheme
COLOR = {"TEXT": "black", "TEXT_BG": "ivory"}

#Files tht should be displayed and opened a notes
TEXT_FILES = [
			("Text Files", ("*.txt", "*.log", "*.asc", "*.conf", "*.cfg")), 
			('All','*')
			]

