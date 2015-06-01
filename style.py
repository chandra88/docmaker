#!/bin/python
import os, sys, shutil

#if not os.path.exists('Html'): os.makedirs('Html')
#shutil.copy('style.css', 'Html')
def style():
	if not os.path.exists('Html'): os.makedirs('Html')
	os.chdir('Html')

	fl = open('style.css', 'w')
	fl.write('\n\
div {\n\
	width: 99.5vw;\n\
	height: 93vh;\n\
}\n')

#div > #top{\n\
#	width: 98.8vw;\n\
#	height: 4vh;\n\
#	background-color: #5B5A5A;\n\
#	font-size: 140%;\n\
#	text-align: center;\n\
#	margin-top: 6px;\n\
#}\n
#\n
	fl.write('\n\
div > header#top {\n\
	width: 98.8vw;\n\
	height: 4vh;\n\
	background-color: #5B5A5A;\n\
	font-size: 140%;\n\
	text-align: center;\n\
	margin-top: 6px;\n\
}\n\
\n\
div > header#top > a {\n\
	color: orange;\n\
	margin-left: 10px;\n\
}\n\
\n\
body {\n\
	color: white;\n\
}\n\
\n\
iframe.left {\n\
	width: 12%;\n\
	height: 96%;\n\
	border: 1px solid black;\n\
	background-color: #5B5A5A;\n\
}\n\
\n\
iframe.center {\n\
	width: 44%;\n\
	height: 96%;\n\
	border: 1px solid black;\n\
	background-color: #4B4A4A;\n\
	margin-left: -6.0px;\n\
	margin-right: -6.0px;\n\
}\n\
\n\
iframe.right {\n\
	width: 43%;\n\
	height: 96%;\n\
	border: 1px solid black;\n\
	background-color: #4B4A4A;\n\
}\n\
\n\
code {\n\
	line-height: 50%;\n\
	color: white;\n\
	text-decoration: none;\n\
}\n\
\n\
code.comment {\n\
	white-space: nowrap;\n\
	color: #B83D3D;\n\
	line-height: 50%;\n\
}\n\
\n\
.type {\n\
	color: #17F707;\n\
}\n\
\n\
a {\n\
	text-decoration: none;\n\
	color: white;\n\
}\n\
\n\
a:hover {\n\
	color: cyan;\n\
}\n\
\n\
ul > li {\n\
	text-decoration: none;\n\
	color: white;\n\
	font-size: 95%;\n\
}\n\
\n\
.file {\n\
	text-decoration: none;\n\
	color: white;\n\
	font-size: 92%;\n\
	margin-left: 14px;\n\
	padding-left: 14px;\n\
	display: block;\n\
}\n\
\n\
ul > li > a {\n\
	text-decoration: none;\n\
	color: white;\n\
}\n\
\n\
nav.leftnavbar > p > a {\n\
	text-decoration: none;\n\
	font-family: Utopia, Arial, Helvetica, sans-serif;\n\
	color: white;\n\
	border: none;\n\
	height: 10%;\n\
}\n\
\n\
nav.leftnavbar {\n\
	color: white;\n\
	text-decoration: none;\n\
	font-family: Utopia, Arial, Helvetica, sans-serif;\n\
	text-align: left;\n\
	padding-right: 1em;\n\
	padding-left: 1em;\n\
	white-space: nowrap;\n\
}\n\
\n\
nav.leftnavbar > p > a:hover {\n\
	color: cyan;\n\
}\n\
\n\
nav.leftnavbar > p > a:visited {\n\
//	color: white;\n\
}\n\
\n\
footer {\n\
	text-align: center;\n\
	padding-top: 6px;\n\
	color: orange;\n\
	width: 98.8vw;\n\
	height: 4vh;\n\
	background-color: #5B5A5A;\n\
	font-size: 110%;\n\
}')
	os.chdir('..')

style()
