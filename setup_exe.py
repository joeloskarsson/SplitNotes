from distutils.core import setup
import py2exe

setup(
	windows=[r'main_window.py'],
	options = {'py2exe': {'bundle_files': 2, 'compressed': True}},
	zipfile = None,
	data_files = [('resources', ['resources/green.png']),
				('resources', ['resources/red.png']),
				('resources', ['resources/settings_icon.png'])]
	)