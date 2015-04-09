#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Gerar a informação de BUY, a compra realizada para o par SESSION, ITEM.

#INPUT
#SESSION	TIMESTAMP			ITEM		CATEGORY
#1,			74201410.85,		214536502,	0
#1,			74201410.9,			214536500,	0
#1,			74201410.9,			214536506,	0
#1,			74201410.95,		214577561,	0

#INPUT 2
#SESSION, 	DAY, 	MONTH, 	YEAR, 	TIME, 	ITEM, 		PRICE 		QUANTITY
#11,		3,		4,		2014,	11.07,	214821371,	1046,		1
#11,		3,		4,		2014,	11.07,	214821371,	1046,		1
#12,		2,		4,		2014,	10.7,	214717867,	1778,		4
#489758,	6,		4,		2014,	9.98,	214826955,	1360,		2

#OUTPUT - column-buys.dat
#0
#1
#0
#0

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

path = path =  "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[0:-2]) + "/Data/"
print "Loading CLICKS data"
clicks_lines = read_file_parts(path, "yoochoose-clicks-parteX.dat", "X", [1,2,3,4,5,6])
print len(clicks_lines), "lines loaded"

print "Loading BUYS data"
buys_lines = read_single_file(path + "buys-proc-basico.dat")
print len(buys_lines), "lines loaded"
print

map_session_item = {}

print "mapping buys"
for linha in buys_lines:
	linha_split = linha.replace("\n","").split(",")
	session = linha_split[0]
	item = linha_split[5]

	if(session in map_session_item.keys()):
		map_session_item[session].append(item)

	else:
		lista = [item]
		map_session_item[session] = lista
print

buy_column = []

conta_linhas = 0
percent_done = 0
print "generating buy column"
for linha in clicks_lines:
	conta_linhas = conta_linhas + 1

	linha_split = linha.replace("\n","").split(",")
	session = linha_split[0]
	item = linha_split[2]

	if(session in map_session_item.keys()):

		if(item in map_session_item[session]):
			buy_column.append("1")
		else:
			buy_column.append("0")

	else:
		buy_column.append("0")

	if (conta_linhas * 100 % len(clicks_lines) == 0):
		print "Processing Buys ", str(((conta_linhas+0.0)/len(linhas_sort)) * 100) + "%" + " done!"

	elif ((len(clicks_lines)/100) == conta_linhas):
		print "Processing Buys ", str(((conta_linhas+0.0)/len(linhas_sort)) * 100) + "%" + " done!"	

print
print len(buy_column), "lines"

arq_w = open("clicks-column-buy.dat", "w")

print "saving data"
for i in buy_column:
	arq_w.write(i)

arq_w.close()