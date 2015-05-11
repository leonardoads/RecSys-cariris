#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Para cada linha que representa uma click de uma SESSÃO em um ITEM, inserir o dado de clicks dados na mesma CATEGORIA do item em questão

#INPUT
#clicks_proc_basico.dat
#SESSION, 	DAY, 	MONTH, 	YEAR, 	TIME, 	ITEM, 		CATEGORY,	SOLDABILITY
#1,			7,		4,		2014,	10.85,	214536502,	0,			2,56
#1,			7,		4,		2014,	10.9,	214536500,	0,			8,5
#1,			7,		4,		2014,	10.9,	214536506,	0			22,37
#1,			7,		4,		2014,	10.95,	214577561,	0			1,44

#OUTPUT - clicks-soldability_mean_by_session.dat
#8.64
#8.64
#8.64
#8.64

#OUTPUT - clicks-soldability_mean_diff_by_session.dat
#6.08
#-0.14
#13.73
#-7.20

#OUTPUT - clicks-soldability_mean_by_session.dat
#5.53
#5.53
#5.53
#5.53


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

#já salva as linhas com a nova coluna
def calculate_and_store_soldability_mean(session, lista_linhas, arq_w_sold_mean, index_soldability_column):
	soldabilities = []

	for linhaSplit in lista_linhas:

		soldability = linhaSplit[index_soldability_column]
		soldabilities.append(soldability)

	soldability_mean = list_mean(soldabilities)
	string_soldability_mean = str(soldability_mean).split(".")[0] + "." + str(soldability_mean).split(".")[1][0:2]

	for s in range(len(soldabilities)):
		arq_w_sold_mean.write(string_soldability_mean + "\n")

def calculate_and_store_soldability_median(session, lista_linhas, arq_w_sold_median, index_soldability_column):
	soldabilities = []

	for linhaSplit in lista_linhas:

		soldability = linhaSplit[index_soldability_column]
		soldabilities.append(soldability)

	soldability_median = list_median(soldabilities)
	string_soldability_median = str(soldability_median).split(".")[0] + "." + str(soldability_median).split(".")[1][0:2]

	for s in range(len(soldabilities)):
		arq_w_sold_median.write(string_soldability_median + "\n")

#já salva as linhas com a nova coluna
def calculate_and_store_soldability_mean_diff(session, lista_linhas, arq_w_sold_mean_diff, index_soldability_column):
	soldabilities = []

	for linhaSplit in lista_linhas:

		soldability = linhaSplit[index_soldability_column]
		soldabilities.append(soldability)

	soldability_mean = list_mean(soldabilities)

	string_soldability_mean_diff = []

	for linhaSplit in lista_linhas:
		soldab = linhaSplit[index_soldability_column]
		diff = float(soldab) - float(soldability_mean)
		string_diff = str(diff).split(".")[0] + "." + str(diff).split(".")[1][0:2]
		arq_w_sold_mean_diff.write(string_diff + "\n")

def list_mean(number_list):
	soma = 0.0
	for num in number_list:
		soma = soma + float(num)

	return (soma / len(number_list) )

def list_median(number_list):
	list_temp = sort(number_list)

	if(len(list_temp) % 2 == 0):
		return( ( float(list_temp[len(list_temp) / 2]) + (float(list_temp[ (len(list_temp) / 2) - 1 ]))) / 2 )
	else:
		return (list_temp[len(list_temp) / 2])

def sort(array):

    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return sort(less)+equal+sort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array

#metodo nativo JOIN nao junta int com string :( 
def join(sep, lista):
	string = ""

	for i in lista:
		string = string + str(i) + sep
	
	return string[:-1]

def c_bind(colunas1, colunas2):
	new_lines = []

	if(not len(colunas1) == len(colunas2)):
		return "COLUMNS DON'T HAVE THE SAME LENGTH"

	index = 0
	for a in range(len(colunas1)):
		new_lines.append(colunas1[index] + "," + colunas2[index])
		index = index + 1

	return new_lines

import os

#init
path =  "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[0:-2]) + "/Data/"
print "Loading CLICKS data"
linhas = read_file_parts(path, "clicks-proc-basico/clicks-proc-basico-parteX.dat", "X", [1,2,3,4,5,6])
print len(linhas), "lines loaded"

print "Loading SOLDABILITY column data"
linhas_soldability = read_single_file(path + "clicks-column-soldability.dat")
print len(linhas_soldability), "lines loaded"

arq_w_sold_mean = open(path + "columns/clicks-soldability_mean_by_session.dat", "w")
arq_w_sold_median = open(path + "columns/clicks-soldability_median_by_session.dat", "w")
arq_w_sold_mean_diff = open(path + "columns/clicks-soldability_mean_diff_by_session.dat", "w")

linhas = c_bind(linhas, linhas_soldability)


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
		calculate_and_store_soldability_mean(session_id_anterior, lista_linhas_por_id, arq_w_sold_mean, 7)
		calculate_and_store_soldability_median(session_id_anterior, lista_linhas_por_id, arq_w_sold_median, 7)
		calculate_and_store_soldability_mean_diff(session_id_anterior, lista_linhas_por_id, arq_w_sold_mean_diff, 7)
		
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

arq_w_sold_mean.close()
arq_w_sold_median.close()
arq_w_sold_mean_diff.close()
