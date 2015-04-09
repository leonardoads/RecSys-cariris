#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Para cada linha que representa uma click de uma SESSÃO em um ITEM, inserir o dado de clicks
#Para cada linha que representa uma click de uma SESSÃO em um ITEM, inserir o dado de vendas
#Para cada linha que representa uma click de uma SESSÃO em um ITEM, inserir o dado de vendabilidade


#INPUT 1
#SESSION, 	DAY, 	MONTH, 	YEAR, 	TIME, 	ITEM, 		CATEGORY
#1,			7,		4,		2014,	10.85,	214536502,	0
#1,			7,		4,		2014,	10.9,	214536500,	0
#1,			7,		4,		2014,	10.9,	214536506,	0
#1,			7,		4,		2014,	10.95,	214577561,	0

#INPUT 2
#ITEM,		CLICKS,	SOLD
#214697848,	169,	2
#214530982,	713,	2
#214687792,	1526,	26
#214687790,	1396,	6

#OUTPUT 1 - clicks_proc3-clicked.dat
#1814
#560
#70
#142

#OUTPUT 2 - clicks_proc3-bought.dat
#20
#0
#3
#0

#OUTPUT 3 - clicks_proc3-soldability.dat
#1,10
#0
#4,28
#0

#no caso de o arquivo estar dividido em partes
#path - local do diretorio
#pattern_filename - padrao do nome das partes do arquivo
#match_numeric - qual parte do padrao deve ser substituido pelo diferenciador da parte
#list_index - lista de diferenciador das partes
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


def save_column(arq_w, list_columns):
	arq_w.write(str(list_columns[-1]) + "\n")

#metodo nativo JOIN nao junta int com string :( 
def join(sep, lista):
	string = ""

	for i in lista:
		string = string + str(i) + sep
	
	return string[:-1]
		
import os

#init
path =  "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[0:-2]) + "/Data/"

print "Loading SOLDABILITY data"
soldability_lines = read_single_file(path + "soldability.dat")
print "Soldability loaded"
print

print "Loading CLICKS data"
click_lines = read_file_parts(path, "clicks-proc-basico-parteX.dat", "X", [1,2,3,4,5,6])
print "Clicks loaded"
print len(click_lines), "lines loaded"
print

arq_w_c = open(path + "clicks-column-clicked.dat", "w")
arq_w_b = open(path + "clicks-column-bought.dat", "w")
arq_w_s	 = open(path + "clicks-column-soldability.dat", "w")

#organizar a soldability em um dicionario
print "Mapping item soldability"
map_item_soldability = {}
for line in soldability_lines:
	line_split = line.replace("\n","").split(",")

	item = line_split[0]

	if (not item in map_item_soldability.keys()):
		map_item_soldability[item] = line_split[1:]
	else:
		print "WARNING: this item is repeated soldability:", item
print

print "Saving soldability associated to session,item"
#associar a informação de clicks, vendas e vendabilidade para cada item de cada session
for line in click_lines:
	line_split = line.replace("\n","").split(",")

	item = line_split[5]

	try:
		item_clicks = map_item_soldability[item][0]
		item_boughts = map_item_soldability[item][1]
		item_soldability = float((map_item_soldability[item][1])) / int(map_item_soldability[item][0])

		#deixar dois digitos apos a vírgola
		item_soldability = str(item_soldability * 100)
		item_soldability = item_soldability.split(".")[0] + "." + item_soldability.split(".")[1][0:2]

		arq_w_c.write(item_clicks + "\n")
		arq_w_b.write(item_boughts + "\n")
		arq_w_s.write(item_soldability + "\n")
	except:
		#items que nunca tiveram clicks, nem vendas
		print item
		arq_w_c.write("-1" + "\n")
		arq_w_b.write("-1" + "\n")
		arq_w_s.write("-1" + "\n")

arq_w_s.close()
arq_w_b.close()
arq_w_c.close()
