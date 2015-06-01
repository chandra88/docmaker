#!/bin/python
import os, sys
import os.path
import subprocess as sp
import fileinput
import glob
import commands
import shutil
import re

from textManip import *
import classFile
from classFile import *
from writeFile import *
import initialize
import style

arg = ''
args = sys.argv
if(len(args) == 2): arg = args[1]
elif(len(args) == 1): arg = '.'
else: 
	print 'wrong argument: exiting'	
	sys.exit()

style.style()
dirList, title, description = initialize.init(arg)

writeTOC(dirList, arg)

for dirr in dirList:
	writeHeader(dirr)
	writeSource(dirr)
	writeFiles(dirr)

writeIndex(dirList)
writeMain(title, description)
writeBlank()

# table of content for each alphabet directory
al = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
for a in al:
	dd = []
	for d in dirList:
		name = os.path.basename(d)
		if(name[0] == a.lower() or name[0] == a.upper()): dd.append(name)
	if(len(dd) > 0): writeTOC(dd, a)
#-----------------------------------------------------------
