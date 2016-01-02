"""
ls refers to LiveSplit in the entire document.
Conversation with livesplit is done through the server component.
"""
import socket
from threading import Thread
import config
import select #used for checking if socket has data pending

def ls_connect(ls_socket, call_func, window):
	"""Connects given socket to the livesplit server."""
	con_thread = Thread(target=try_connection, args=(ls_socket, call_func, window))
	con_thread.start()
	
		
def init_socket():
	"""Returns a fresh socket"""
	return socket.socket()
		
def try_connection(ls_socket, call_func, window):
	"""
	Tries to connect given socket to ls.
	If connection is successful given "call_func" 
	is called with window as argument.
	(made to be ran in a separate thread)
	"""
	try:
		ls_socket.connect((config.HOST, config.PORT))
	except:
		return False
		
	call_func(window)
	
def close_socket(com_socket):
	"""Closes given socket."""
	com_socket.close()

def check_connection(ls_socket):
	"""
	Check so connection between socket and livesplit 
	is still active and working.
	Returns boolean
	"""
	if send_to_ls(ls_socket, "best_possible"):
		return True
	else:
		return False
		
	
def send_to_ls(ls_socket, command):
	"""
	Sends given command to ls using given socket.
	If connected is False, tries to send without socket being connected to ls.
	Returns the response, or False if an error occurs.
	Check config.LS_COMMANDS for avaiable commands.
	"""

	try:
		ls_socket.send(str.encode(config.LS_COMMANDS[command]))
	except:
		return False
	
	socket_ready = select.select([ls_socket], [], [], config.COM_TIMEOUT)
	if socket_ready[0]:
		try:
			return (ls_socket.recv(1000)).decode("utf-8")
		except:
			return False
	else:
		return False
	

def get_split_index(ls_socket):
	"""
	Returns the index of the active split in livesplit.
	Returns -1 if timer is not yet started.
	(First split is 0)
	
	Returns False on Error
	"""
	ls_data = send_to_ls(ls_socket, "cur_split_index")
	
	if not isinstance(ls_data, bool):
		return int(ls_data)
	else:
		return False
		

def get_split_name(ls_socket):
	"""
	Returns name of the active split in livesplit.
	Returns False if no split is active or Error occurs.
	"""
	ls_data = send_to_ls(ls_socket, "cur_split_name")
	
	if ls_data:
		return ls_data
	else:
		return False