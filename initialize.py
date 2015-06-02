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
from classFile import *

def init(dirr):
	excludes = []
	fl = open('initFile.txt', 'r')
	lines = fl.readlines()
	for line in lines:
		line = line.strip()
		if('title' in line or 'Title' in line): Title = line.split(':')[1]
		elif('description' in line): Description = line.split(':')[1]
		elif('exclude' in line):
			excludes = line.split(':')[1]
			excludes = split(excludes)
	fl.close()
	#---------------------------------------------------

	if not os.path.exists('Html'): os.makedirs('Html')

	listDir = []
	for dirname, dirnames, filenames in os.walk(dirr):
		dirr = os.path.basename(dirname)
		path = os.path.abspath(dirname)
		a = 0
		for exe in excludes:
			if(exe in path): a = 1

		if(dirr == '.'): continue

		if(a == 0):
			if not os.path.exists('Html/' + dirname): os.makedirs('Html/' + dirname)
			listDir.append(dirname)
	listDir.append('.')	
        return listDir, Title, Description
#-----------------------------------------------------------

def scandirs(dirr):
	dirList = []
	fl = open('initFile.txt')
	lines = fl.readlines()
	fl.close()

	exclude = []
	for line in lines:
		line = line.strip()
		if('exclude:' in line): 
			tmp = line
			lns = line.split(':')
			exclude = split(lns[1])

	for name in os.listdir("."):
		if(not os.path.isdir(name)): continue
		if(name in exclude): continue
		dirList.append(name)

	dirList.insert(0, '.')
	return dirList
#-----------------------------------------------------------

def findClass(dirr):
	headers = glob.glob(dirr + '/*.h')
	files = glob.glob(dirr + '/*.cxx')
	files = files + glob.glob(dirr + '/*.C')

	headersDict = glob.glob(dirr + '/*Dict.h')
	headersDict = headersDict + glob.glob(dirr + '/*LinkDef.h')
	fileDict = glob.glob(dirr + '/*Dict.cxx')

	headers = set(headers) - set(headersDict)
	files = set(files) - set(fileDict)

	tmp = Info(dirr)
	
	for headerPath in headers:
		header = os.path.basename(headerPath)
		path = os.path.dirname(headerPath)
		source = header[0:-2] + '.cxx'
		sourcePath = path + '/' + source
		if(os.path.isfile(sourcePath)):
			cl = Class(headerPath, sourcePath)
			files.remove(sourcePath)
			# scan methods			
			fl = open(headerPath, 'r')
			lines = fl.readlines()
			fl.close()
		
			line1 = getLineNum(lines, 'private:')
			line2 = getLineNum(lines, '#endif', line1)

			for x in range(line1, line2-1): 
				line = lines[x].strip()
				if(len(line) == 0): continue
				if 'private:' in line: continue
				if 'public:' in line: continue
				if(len(line) > 0 and line[0] == '/' and line[1] == '/'): continue
				else: 
					if('(' in line and ')' in line): cl.methods.append(line)	
			#-------------------------

			tmp.classes.append(cl)
				
	tmp.files = files
	return tmp
	
#-----------------------------------------------------------
'''
def findClassList():
	classList = []
	dirList = scandirs()
	for dirr in dirList:
		headers = glob.glob(dirr + '/*.h')
		files = glob.glob(dirr + '/*.cxx')

		headersDict = glob.glob(dirr + '/*Dict.h')
		headersDict = headersDict + glob.glob(dirr + '/*LinkDef.h')
		fileDict = glob.glob(dirr + '/*Dict.cxx')

		headers = set(headers) - set(headersDict)
		files = set(files) - set(fileDict)

		tmp = Info(dirr)
		for headerPath in headers:
			header = os.path.basename(headerPath)
			source = header[0:-2] + '.cxx'
			sourcePath = dirr + '/' + source
			if(os.path.isfile(sourcePath)):
				cl = Class(headerPath, sourcePath)
				files.remove(sourcePath)

				# scan methods                  
				fl = open(headerPath, 'r')
				lines = fl.readlines()
				fl.close()

				line1 = getLineNum(lines, 'private:')
				line2 = getLineNum(lines, '#endif', line1)
	
				for x in range(line1, line2-1):
					line = lines[x].strip()
					if(len(line) == 0): continue
					if 'private:' in line: continue
					if 'public:' in line: continue
					if(len(line) > 0 and line[0] == '/' and line[1] == '/'): continue
					else:
						if('(' in line and ')' in line): cl.methods.append(line)
				#-------------------------

				tmp.classes.append(cl)

		tmp.files = files
		return tmp
'''
#-----------------------------------------------------------

def split(line):
	words = []
	tmp = ''
	for x in range(0, len(line)):
		if(not line[x] == ' '): tmp = tmp + line[x]
		if(line[x] == ' ' and not line[x-1] == ' '):
			if(len(tmp) > 0): words.append(tmp)
			tmp = ''
		if(x == len(line)-1): 
			if(len(tmp) > 0): words.append(tmp)
	return words
#-----------------------------------------------------------
