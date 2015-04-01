#!/usr/bin/env python
# -*- coding: utf-8 -*-


#Para cada linha que representa uma click de uma SESSÃO em um ITEM, inserir o dado de clicks dados na mesma CATEGORIA do item em questão

#INPUT
#SESSION, 	DAY, 	MONTH, 	YEAR, 	TIME, 	ITEM, 		CATEGORY
#1,			7,		4,		2014,	10.85,	214536502,	0
#1,			7,		4,		2014,	10.9,	214536500,	0
#1,			7,		4,		2014,	10.9,	214536506,	0
#1,			7,		4,		2014,	10.95,	214577561,	0

#OUTPUT - clicks_proc2.dat
#1,			7,		4,		2014,	10.85,	214536502,	0,	4
#1,			7,		4,		2014,	10.9,	214536500,	0,	4
#1,			7,		4,		2014,	10.9,	214536506,	0,	4
#1,			7,		4,		2014,	10.95,	214577561,	0,	4

import os

def read_file_parts(path, pattern_filename, match_numeric, list_index):
	list_temp = []

	for i in list_index:
		print "Reading file:", pattern_filename.replace(match_numeric, str(i))
		arq = open(path + pattern_filename.replace(match_numeric, str(i)), "r")
		list_temp = list_temp + arq.readlines()

	return list_temp

def insert_and_save_clicks_same_category(session, lista_linhas, arq_w):
	map_category_count = {}

	linhas_with_clicks_same_cat = []

	for linhaSplit in lista_linhas:
		item = linhaSplit[5]
		categ = linhaSplit[6]

		if(categ in map_category_count.keys()):
			map_category_count[categ] = map_category_count[categ] + 1
		else:
			map_category_count[categ] = 1

	for linhaSplit in lista_linhas:
		categ = linhaSplit[6]
		new_line = linhaSplit
		
		new_line.append(map_category_count[categ])

		arq_w.write(join(",", new_line) + "\n")

#metodo nativo JOIN nao junta int com string :( 
def join(sep, lista):
	string = ""

	for i in lista:
		string = string + str(i) + sep
	
	return string[:-1]
		

#init
path = "/home/tales/development/RecSys-cariris/Data/"
print "Loading CLICKS data"
linhas = read_file_parts(path, "clicks_parte_X_proc_basico.dat", "X", [1,2,3,4])
print len(linhas), "lines loaded"
arq_w = open(path + "clicks_proc_2.dat", "w")


###########################################################
##   Este trecho permite uma rapida iteração por sessões ##
## quando é necessário comparar elas. Se lembre que elas ##
## estão juntas no arquivo. TalesBoy :)                  ##
###########################################################
session_id_anterior = "0"
lista_linhas_por_id = []

updated_lines = []

linhas.append("0,0,0,0,0.0,0,0")

conta_linhas = 0
percent_done = 0

for linha in linhas:
	conta_linhas = conta_linhas + 1
	
	linhaSplit = linha.replace("\n","").split(",")
	session_id = linhaSplit[0]

	if(session_id != session_id_anterior):
		insert_and_save_clicks_same_category(session_id_anterior, lista_linhas_por_id, arq_w)
		
		lista_linhas_por_id = []
		session_id_anterior = session_id
		
		lista_linhas_por_id.append(linhaSplit)

	else:
		lista_linhas_por_id.append(linhaSplit)


	#apenas para dar print no andamento do script
	if (len(linhas) == conta_linhas):
		percent_done = 100
		conta_linhas = 0
		#print datetime.datetime.now().time().hour, datetime.datetime.now().minute
		print "Done:", (str(percent_done) + "%")

	elif (330039 == conta_linhas):
		percent_done = percent_done + 1
		conta_linhas = 0
		#print datetime.datetime.now().time().hour, datetime.datetime.now().minute
		print "Done:", (str(percent_done) + "%")


##########################################
## FIM DO TRECHO DESCRITO ANTERIORMENTE ##
##########################################