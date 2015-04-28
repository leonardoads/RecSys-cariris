#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Gerar a informação de DAY_OF_WEEK para o click

#INPUT
##SESSION, 	DAY, 		MONTH,	 	YEAR, 	TIME, 	ITEM,		CATEGORY
#14679,		03,		04,		2014,	04.73,	214645087,	0
#14672,		02,		04,		2014,	07.61,	214664919,	0
#14672,		02,		04,		2014,	07.61,	214826625,	0
#14673,		06,		04,		2014,	15.85,	214696625,	0
#14673,		06,		04,		2014,	15.96,	214696740,	0

#OUTPUT
##SESSION, 	DAY, 		MONTH,	 	WEEKDAY		YEAR, 	TIME, 	ITEM,		CATEGORY
#14679,		03,		04,		WEDNESDAY,	2014,	04.73,	214645087,	0
#14672,		02,		04,		TUESDAY,	2014,	07.61,	214664919,	0
#14672,		02,		04,		TUESDAY,	2014,	07.61,	214826625,	0
#14673,		06,		04,		SATURDAY,	2014,	15.85,	214696625,	0
#14673,		06,		04,		SATURDAY,	2014,	15.96,	214696740,	0


def read_file_parts(path, pattern_filename, match_numeric, list_index):
	list_temp = []

	for i in list_index:
		print "Reading file:", pattern_filename.replace(match_numeric, str(i))
		arq = open(path + pattern_filename.replace(match_numeric, str(i)), "r")
		list_temp = list_temp + arq.readlines()
		arq.close()

	return list_temp


def read_single_file(filename):
	lines = ""

	print "Reading file:", filename
	arq = open(filename, "r")
	lines = arq.readlines()

	return lines

import os
import datetime

days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

path =  "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[0:-2]) + "/Data/"
print "Loading CLICKS data"
clicks_lines = read_file_parts(path, "clicks-proc-basico/clicks-proc-basico-parteX.dat", "X", [1,2,3,4,5,6])
print len(clicks_lines), "lines loaded\n"

arq_w = open(path + "/columns/clicks-column-weekday.dat", "w")

for linha in clicks_lines:
	linha_split = linha.split(",")
	day = int(linha_split[1])
	month = int(linha_split[2])
	year = int(linha_split[3])

	d = datetime.date(year, month, day)

	arq_w.write(days[d.weekday()] + "\n")	

arq_w.close()
