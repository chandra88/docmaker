#!/bin/python
import os, sys


#-----------------------------------------------------------

# to hold one class info
class Class():
	def __init__(self, head, source):
		self.header = head
		self.source = source
		self.methods = []
#-----------------------------------------------------------

# classes and files inside one directory. 
# name => directory name. 
# pairs => header and source files for a particular class.
# files => other files
class Info:
	def __init__(self, name):
		self.name = name
		self.classes = []
		self.files = []
#-----------------------------------------------------------
