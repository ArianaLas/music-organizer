#
# Copyright (c) by Patryk Jaworski
# Contact:
# -> E-mail: Patryk Jaworski <skorpion9312@gmail.com>
# -> XMPP/Jabber: skorpion9312@jabber.org
#

class Interface:
	def __init__(self, args):
		"""
		Defaut constructor - get args
		"""
		raise NotImplementedError;
	
	def operate(self):
		"""
		Start interface
		"""
		raise NotImplementedError;

