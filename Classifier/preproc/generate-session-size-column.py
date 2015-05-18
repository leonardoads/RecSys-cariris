#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Gerar a coluna do tamanho da sessão, ou seja, a quantidade de clicks feitos por ela

#INPUT
#clicks_proc_basico.dat
#SESSION, 	DAY, 	MONTH, 	YEAR, 	TIME, 	ITEM, 		CATEGORY
#1,			7,		4,		2014,	10.85,	214536502,	0
#1,			7,		4,		2014,	10.9,	214536500,	0
#1,			7,		4,		2014,	10.9,	214536506,	0
#1,			7,		4,		2014,	10.95,	214577561,	0

#OUTPUT - clicks_session_size.dat
#CLICKS_SAME_CAT
#4
#4
#4
#4


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

#já salva as linhas com a nova coluna
def sum_and_save_session_size(session, lista_linhas, arq_w):
	for i in range(len(lista_linhas)):
		arq_w.write( str(len(lista_linhas)) + "\n")

#metodo nativo JOIN nao junta int com string :( 
def join(sep, lista):
	string = ""

	for i in lista:
		string = string + str(i) + sep
	
	return string[:-1]
		
import os

#init
path =  "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[0:-2]) + "/Data/"
print "Loading CLICKS data"
linhas = read_file_parts(path, "clicks-proc-basico/clicks-proc-basico-parteX.dat", "X", [1,2,3,4,5,6])
print len(linhas), "lines loaded"
arq_w = open(path + "columns/clicks-column-session-size.dat", "w")


###########################################################
##   Este trecho permite uma rapida iteração por sessões ##
## quando é necessário comparar elas. Se lembre que elas ##
## estão juntas no arquivo. TalesBoy :)                  ##
###########################################################

session_id_anterior = linhas[0].split(",")[0]
lista_linhas_por_id = []

#apenas para poder registrar as linhas da ultima sessão
linhas.append("0,0,0,0,0.0,0,0")

conta_linhas = 0
percent_done = 0
total = 0
for linha in linhas:
	total = total + 1
	conta_linhas = conta_linhas + 1
	
	linhaSplit = linha.replace("\n","").split(",")
	session_id = linhaSplit[0]

	if(session_id != session_id_anterior):
		sum_and_save_session_size(session_id_anterior, lista_linhas_por_id, arq_w)
		
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

	elif ((len(linhas) / 100) == conta_linhas):
		percent_done = percent_done + 1
		conta_linhas = 0
		#print datetime.datetime.now().time().hour, datetime.datetime.now().minute
		print "Done:", (str(percent_done) + "%")


##########################################
## FIM DO TRECHO DESCRITO ANTERIORMENTE ##
##########################################

print total - 1, "lines saved"

arq_w.close()
