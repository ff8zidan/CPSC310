from django.db import models
from decimal import Decimal
from rango.models import Er_Room
from django.test import TestCase
import os
# Reads ERtext.txt from tango (parent) folder

class Parse():
	
	def parsing(self,path, path2):
		reader = open(path, 'r')
		line = reader.readline()
		import sqlite3 as lite
		con = lite.connect(path2)
		i = 0
	
		for line in reader:
			str = line.split("\t")
			i = i + 1
	 		city = str[19]
	 	  	address = str[15]
	 	 	name = str[3]
	 	 	lat = float(str[22])
	 	 	lon = float(str[23])
	 	 	with con:
	 	 	 	cur = con.cursor()
	 	 	 	cur.execute("INSERT INTO rango_Er_Room VALUES(?,?,?,?,?,?)", (i,address, name, city, lat, lon))
	 	 	 	
		cur.execute("select * from rango_Er_Room")
		for er_room in cur.fetchall():
			print(er_room)
