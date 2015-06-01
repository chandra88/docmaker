#!/bin/python
import os, sys
import os.path
import subprocess as sp
import fileinput
import glob
import commands
import shutil

#-----------------------------------------------------------
def getLineNum(lines, ln, st=0):
	a = 0;
	for x in range(st, len(lines)):
		if ln in lines[x]: 
			if(not lines[x][0] == '/'): return a+st
		a = a + 1
#-----------------------------------------------------------

def isHeader(line, head):
	line = line.strip()
	lines = line.split(' ')
	x = lines[0].find(head)
	return x
#-----------------------------------------------------------

def insertFormat(line, pair):
	head = pair.header
	head = os.path.basename(head)
	head = head[:-2]

	source = pair.source

	x = isHeader(line, head)
	ln = len(head)
	if(x >= 0): line = line[:x] + '<span class="type">' + '<a href="' + head.lower() + '_cxx.html" target="right">' + head + '</a></span>' + line[x+ln:]
	return line
#-----------------------------------------------------------

def formatType(line):
	ty = ['int', 'float', 'double', 'long', 'vector', 'void', 'const', 'bool', 'string']

	line = line.replace('print', 'prTmp')	# to avoid link to 'int' in 'print'
	for t in ty:
		line = line.replace(t, '<span class="type">' + t + '</span>')
	line = line.replace('prTmp', 'print')	# return to original string
	return line
#-----------------------------------------------------------

def setLinks(dirr, line, pair):
	head = pair.header
	head = os.path.basename(head)
	head = head[:-2]	

	fun = findFun(line)
	if(len(fun) > 0): line = line.replace(fun, '<span class="type">' + '<a href="' + head + '_cxx.html#' + fun + '" target="right">' + fun + '</a></span>')
	return line
#-----------------------------------------------------------

def setTarget(line):
	fun = findFun(line)
	funs = fun.split('::')
	if(len(funs) == 1): return line
	fun = funs[1]
	if(len(fun) > 0): line = line.replace(fun, '<span name="' + fun + '" id="' + fun + '">' + fun + '</span>')
	return line
#-----------------------------------------------------------

def isType(tt):
	tyy = ['int', 'float', 'double', 'vector', 'void', 'const', 'bool', 'string', 'ClassDef', 'long', '{}']
	for ty in tyy:
		if(ty in tt): return True
	return False
#-----------------------------------------------------------

def findFun(st):
	lines = st.split(' ')
	word = ''
	for line in lines:
		if(line.find('(') >= 0):
			word = line
			break

	words = word.split('(')
	if('ClassDef' in words[0]): return ''
	return words[0]
#-----------------------------------------------------------
