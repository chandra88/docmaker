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
from initialize import *

doctype = '<!DOCTYPE HTML> ''\n'' \
<html lang=en> ''\n'' \
<head> ''\n'' \
	<meta charset="tf-8" /> ''\n'' \
	<title>' + 'Title' + '</title> ''\n'' \
	<link rel="stylesheet" href="style.css" type="text/css"/> ''\n'' \
</head> ''\n\n'' '
#-----------------------------------------------------------

def writeIndex(dirList):
	alpha = {}
	for x in range(1, 27):
		y = []
		alpha[numToalpha(x)] = y
	#-------------------------------
	for dirr in dirList:
		if(dirr[len(dirr)-1] == '/'): dirr = dirr[:-1]
		name = os.path.basename(dirr)
		lt = name[0]
		if(lt == '.'): continue
		alpha[lt.upper()].append(dirr)
	#-------------------------------
	
	body = '\t<body> ''\n'' '
	body = body + '\t\t<div>''\n'' '
	body = body + '\t\t\t<header id="top"> ''\n'' \
				<a href="toc.html" target="left">' + 'All' + '</a> ''\n'' '	

	for x in range(1, len(alpha)+1):
		al = alpha[numToalpha(x)]
		if(len(al) > 0): 
			body = body + '\t\t\t\t<a href="' + numToalpha(x).lower() + '.html" target="left">' + numToalpha(x) + '</a> ''\n'' '
	body = body + \
'			</header> ''\n'' \
			<iframe class="left" name="left" src="toc.html"></iframe> ''\n'' \
			<iframe class="center" name="center" src=""></iframe> ''\n'' \
			<iframe class="right" name="right" src=""></iframe> ''\n'' \
		</div> ''\n\n'' \
\
		<footer> ''\n''\
			<span> Created by docmaker </span> ''\n'' \
			<a style="color: red; margin-left: 20px;" href="mailto:code84682@gmail.com">email</a> ''\n'' \
		</footer> ''\n'' \
	</body> ''\n'' \
</html> '

	os.chdir('Html')
	fi = open('index.html', 'w')
	fi.write(doctype)
	fi.write(body)
	fi.close()
	os.chdir('..')
#-----------------------------------------------------------

def writeMain(Title, Description):
	os.chdir('Html')
	fi = open('main.html', 'w')

	head = '<!DOCTYPE HTML> ''\n''\
<html lang='"en"'> ''\n'' \
	<head> ''\n'' \
		<meta charset="utf-8" /> ''\n'' \
		<title> ' + Title + ' </title> ''\n'' \
		<link rel="stylesheet" href="style.css" type="text/css"/> ''\n'' \
	</head> ''\n\n'' \
	<body> \
		<p style="text-align: center">' + Title + '</p> \
		<p style="text-align: center">' + '*'*(len(Title)+8) + '</p><br> \
		<p style="text-align: center" "font-size: 120%">' + Description + '</p> \
</body> ''\n'' '

	fi.write(head)
	fi.write('</html>')
	os.chdir('..')
#-----------------------------------------------------------

def writeTOC(dirList, st):
	body = '\t<body> ''\n'' \
		<nav class="leftnavbar"> \n \
			<p><a href="main.html" target="center">Main Page</a></p>\n'
	body = body + '\t\t\t<!--  --------------------  -->\n\n'

	for dirr in dirList:
		classlist = findClass(dirr)

		body = body + '\t\t\t<p style="margin-bottom: -10px;"></p> \n '
		if(st == '.'): body = body + '\t\t\t<p style="margin-bottom: -16px;"><a href="' + dirr[2:] + '_h.html" target="center">' + dirr[2:] + '</a></p>\n'
		else: body = body + '\t\t\t<p style="margin-bottom: -16px;"><a href="' + dirr + '_h.html" target="center">' + dirr + '</a></p>\n'

		if(len(classlist.classes) > 0): 
			body = body + '\t\t\t<ul>\n'
			for cl in classlist.classes:
				header = cl.header
				header = os.path.basename(header)
				header = header[:-2]

				if(dirr == '.'): body = body + '\t\t\t\t<li><a style="font-size: 95%" href="' + dirr + '/' + header + '_h.html" target="center">' + header + '</a></li>\n'
				else: body = body + '\t\t\t\t<li><a href="' + dirr + '/' + header + '_h.html" target="center">' + header + '</a></li>\n' 
		
			body  = body + '\t\t\t</ul>\n'	

		body = body + '\t\t\t<p style="margin-bottom: -14px;"></p>\n'

		for fl in classlist.files: 
			flName = os.path.basename(fl)
			body = body + '\t\t\t<a class="file" href="' + dirr + '/' + flName.replace('.', '_') + '.html" target="center">' + flName + '</a>\n'
		body = body + '\t\t\t<!--  --------------------  -->\n\n'
		
	body = body + '\t\t</nav>\n'
	body = body + '\t</body>\n'

	os.chdir('Html')
	fi = ''
	if(st == '.' or len(st) > 2): fi = open('toc.html', 'w')
	else: fi = open(st.lower() + '.html', 'w')
	fi.write(doctype)
	fi.write(body)
	fi.write('</html>')
	fi.close()
	os.chdir('..')
#-----------------------------------------------------------

def writeHeader(dirr):
	cwd = os.getcwd()
	stDir = cwd + '/Html/style.css'
	classlist = findClass(dirr)		# list of classes in this directory
	for cl in classlist.classes:
		header = cl.header 	
		header = os.path.basename(header)
		header = header[:-2]

		body = '\t<body> ''\n'' '

		head = '<!DOCTYPE HTML> ''\n''\
<html lang='"en"'> ''\n'' \
	<head> ''\n'' \
		<meta charset="utf-8" /> ''\n'' \
		<title> ' + header + ' </title> ''\n'' \
		<link rel="stylesheet" href="' + stDir + '" type="text/css"/> ''\n'' \
	</head> ''\n\n'' '

		fl = open(cl.header, 'r')
		lines = fl.readlines()
		fl.close()

		line0 = getLineNum(lines, 'class')
		line1 = getLineNum(lines, 'private:', line0)
		line2 = getLineNum(lines, 'public:', line1)
		line3 = getLineNum(lines, '#endif', line2)

		# write comments
		for x in range(0, line0): 
			line = lines[x].strip()
			line = setLinks(dirr, line, cl)
			if(len(line) < 3): continue
			if(line[0] == '/' and line[1] == '/'): body = body + '\t\t<code class="comment">' + line + '</code><br>\n'
		body = body + '\n'
		
		# write include:
		for x in range(0, line0):
			line = lines[x].strip()
			if(len(line) <= 0):
				body = body + '\t\t<br>\n'
				continue

			line = line.replace('<', '&lt')
			line = line.replace('>', '&gt')
			line = setLinks(dirr, line, cl)
			if(line[0] == '#' or line[0:5] == 'using'): body = body + '\t\t<code>' + line + '</code><br>\n'
		body = body + '\n'
	
		# writing private:
		for x in range(line1, line2):
			line = lines[x].strip()
			if(len(line) == 0): 
				body = body + '<br>'
				continue

			line = line.replace('<', '&lt')
			line = line.replace('>', '&gt')
			line = setLinks(dirr, line, cl)
			if(line[0] == '/' and line[1] == '/'): body = body + '\t\t&nbsp &nbsp<code class="comment">' + line + '</code><br>\n'	
			elif(line[0] == '/' and line[1] == '/' and line[2] == '/'): body = body + '\t\t&nbsp &nbsp<code class="comment">' + line + '</code>\n'
 			else:
				line = formatType(line)
				if(x == line1): body = body + '\t\t<code>' + line + '</code><br>\n'
				else: body = body + '\t\t&nbsp&nbsp&nbsp&nbsp <code>' + line + '</code><br>\n'
		body = body + '\n'
	
		# write public:
		for x in range(line2, line3-1): 
			line = lines[x].strip()
			line = line.replace('<', '&lt')
			line = line.replace('>', '&gt')
			if(len(line) == 0):
				body = body + '<br>'
				continue
	
			if(len(line) > 0 and line[0] == '/' and line[1] == '/'): body = body + '\t\t&nbsp; &nbsp;<code class="comment">' + line + '</code><br>\n'
			else: 
				line = formatType(line)
				if(x == line2): body = body + '\t\t<code>' + line + '</code><br>\n'
				else: 
					line = setLinks(dirr, line, cl)
					body = body + '\t\t&nbsp&nbsp&nbsp&nbsp <code>' + line + '</code><br>\n'

		cwd = os.getcwd()
		body = body + '\t</body> ''\n'''
		os.chdir('Html/' + dirr)
		fi = open(header + '_h.html', 'w')
		fi.write(head)
		fi.write(body)
		fi.write('</html>')
		fi.close()
		os.chdir(cwd)
#-----------------------------------------------------------

def writeSource(dirr):
	cwd = os.getcwd()
	stDir = cwd + '/Html/style.css'
	classlist = findClass(dirr)

	for cl in classlist.classes:
		header = cl.header
		header = os.path.basename(header)
		header = header[:-2]

		body = '\t<body> ''\n'' '

		head = '<!DOCTYPE HTML> ''\n''\
<html lang='"en"'> ''\n'' \
	<head> ''\n'' \
		<meta charset="utf-8" /> ''\n'' \
		<title> ' + dirr + ' </title> ''\n'' \
		<link rel="stylesheet" href="' + stDir + '" type="text/css"/> ''\n'' \
	</head> ''\n\n'' '

		fl = open(cl.source, 'r')
		lines = fl.readlines()
		fl.close()

		a = 0
		b = 0
		space = ''
		for line in lines:
			line = line.strip()
			line = line.replace('<', '&lt')
			line = line.replace('>', '&gt')
			if(len(line) == 0):
				body = body + '\t\t<br>\n'
				continue

			if('{' in line): a = a + 1

			if(len(line) > 0 and line[0] == '/' and line[1] == '/'): 
				sp = '&nbsp&nbsp&nbsp&nbsp&nbsp'*a
				body = body + '\t\t<br><code class="comment">' + sp + line + '</code><br>\n'
			else:
				line = formatType(line)
				line = setTarget(line)
				if(line[0] == '#' or header + '::' in line): body = body + '\t\t<code>' + line + '</code><br>\n'
				else: 
					if('}' in line): 
						a = a - 1
						space = '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'*a
					body = body + '<br>\t\t' + space + '<code>' + line + '</code>\n'
					space = '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'*a
		body = body + ' ''\n'' '

		cwd = os.getcwd()
		body = body + '\t</body> ''\n'''
		os.chdir('Html/' + dirr)
		fi = open(header + '_cxx.html', 'w')
		fi.write(head)
		fi.write(body)
		fi.write('</html>')
		fi.close()
		os.chdir(cwd)
#-----------------------------------------------------------

def writeFiles(dirr):
	cwd = os.getcwd()
	stDir = cwd + '/Html/style.css'

	classlist = findClass(dirr)
	for fl in classlist.files:
		body = '\t<body> ''\n'' '

		head = '<!DOCTYPE HTML> ''\n''\
<html lang='"en"'> ''\n'' \
	<head> ''\n'' \
		<meta charset="utf-8" /> ''\n'' \
		<title> ' + fl + ' </title> ''\n'' \
		<link rel="stylesheet" href="' + stDir + '" type="text/css"/> ''\n'' \
        </head> ''\n\n'' '
		
		f = open(fl, 'r')
		lines = f.readlines()
       	        f.close()

		includeList = []
		for line in lines:
			line = line.replace('<', '&lt')
			line = line.replace('>', '&gt')
			if(line[0] == '#'): includeList.append(line)

		for include in includeList: 
			include = include.strip()
			body = body + '\t\t<code>' + include + '</code><br>\n'
		body = body + '\t\t<br>\n'

		a = 0
		b = 0
		space = ''
		for line in lines:
			line = line.strip()
			line = line.replace('<', '&lt')
			line = line.replace('>', '&gt')
			if(len(line) <= 0): 
				body = body + '\t\t<br>\n'
				continue

			if('{' in line): a = a + 1
			if(len(line) > 0 and line[0] == '/' and line[1] == '/'): 
				sp = '&nbsp&nbsp&nbsp&nbsp&nbsp'*a
				body = body + '\t\t<br><code class="comment">' + sp + line + '</code>\n'
			else:
				line = formatType(line)
				line = setTarget(line)
				if(line[0] == '#'): continue
				else:
					if('}' in line):
						a = a - 1
						space = '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'*a
					body = body + '\t\t<br>' + space + '<code>' + line + '</code>\n'
					space = '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'*a
				body = body + ' ''\n'' '
		body = body + '\t</body> ''\n'''


		cwd = os.getcwd()
		body = body + '\t</body> ''\n'''
		os.chdir('Html/' + dirr)
		fll = os.path.basename(fl)
		fll = fll.replace('.', '_') + '.html'
		fi = open(fll, 'w')

		fi.write(head)
		fi.write(body)
		fi.write('</html>')
		fi.close()
		os.chdir(cwd)
#-----------------------------------------------------------

def alphaTonum(alpha):
	al = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':10, 'K':11, 'L':12, 'M':13, 'N':14, 'O':15, 'P':16, 'Q':17, 'R':18, 'S':19, 'T':20, 'U':21, 'V':22, 'W':23, 'X':24, 'Y':25, 'Z':26}
	return(alpha)
#-----------------------------------------------------------

def numToalpha(num):
	nu = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I', 10:'J', 11:'K', 12:'L', 13:'M', 14:'N', 15:'O', 16:'P', 17:'Q', 18:'R', 19:'S', 20:'T', 21:'U', 22:'V', 23:'W', 24:'X', 25:'Y', 26:'Z'}
	return nu[num]
