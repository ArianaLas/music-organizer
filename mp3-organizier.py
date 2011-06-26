#!/usr/bin/python3
# coding=utf-8

# 
# Copyright by:
# -> Patryk Jaworski <skorpion9312@gmail.com>
# -> Ariana Las <ariana.las@gmail.com>
# License: GNU GPLv3
# 

import sys;
import os;

class Main:
	__interface = None;

	def __init__(self):
		path = os.path.abspath(__file__);
		if os.path.islink(path):
			path = os.readlink(path);
		path = os.path.dirname(path);
		os.chdir(path);
		if len(sys.argv) < 2:
			try:
				import MP3Organizer.interfaces.qt;
				self.__interface = MP3Organizer.interfaces.qt.Organizer(sys.argv);
			except ImportError:
				print("[E] GUI mode not installed...");
				sys.exit(2);
		else:
			try:
				import MP3Organizer.interfaces.standard;
				self.__interface = MP3Organizer.interfaces.standard.Organizer(sys.argv);
			except ImportError:
				print("[E] Standard mode not installed...");
				sys.exit(2);
		self.__interface.operate();

if __name__ == "__main__":
	try:
		Main();
	except KeyboardInterrupt:
		print("[I] Aborting...");
		sys.exit(5);

