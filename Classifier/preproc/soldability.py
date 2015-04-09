#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Gera uma tabela (item, qtd_clicks, qtd_compras) para os itens

#INPUT 1
#SESSION, 	DAY, 	MONTH, 	YEAR, 	TIME, 	ITEM, 		PRICE 		QUANTITY
#11,		3,		4,		2014,	11.07,	214821371,	1046,		1
#11,		3,		4,		2014,	11.07,	214821371,	1046,		1
#12,		2,		4,		2014,	10.7,	214717867,	1778,		4
#489758,	6,		4,		2014,	9.98,	214826955,	1360,		2

#INPUT 2
#SESSION, 	DAY, 	MONTH, 	YEAR, 	TIME, 	ITEM, 		CATEGORY
#1,			7,		4,		2014,	10.85,	214536502,	0
#1,			7,		4,		2014,	10.9,	214536500,	0
#1,			7,		4,		2014,	10.9,	214536506,	0
#1,			7,		4,		2014,	10.95,	214577561,	0

#OUTPUT - soldability.dat
#ITEM,		CLICKS_N,		SOLD_N
#123123,	25,				3
#001001,	103,			15		

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

	return list_temp

def read_single_file(filename):
	arq = open(filename, "r")
	return arq.readlines()

#metodo nativo JOIN nao junta int com string :( 
def join(sep, lista):
	string = ""

	for i in lista:
		string = string + str(i) + sep
	
	return string[:-1]

def to_1st_column(linha_split, index_column):
	lista = [linha_split.pop(index_column)]
	for i in linha_split:
		lista.append(i)
	return join(",", lista)


def sort(array):
    global recursion_count
    global million_recursion
    recursion_count = recursion_count + 1

    if (recursion_count == 1000000):
        million_recursion = million_recursion + 1
        print million_recursion, "million recursion"
      	recursion_count = 0

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

def count_buys(lista_linhas):
    subtotal = 0
    for linha in lista_linhas:
        linha_split = linha.split(",")
        subtotal = subtotal + int(linha_split[len(linha_split) - 1])
    
    return subtotal

import os
import sys

sys.setrecursionlimit(1000000000)

recursion_count = 0
million_recursion = 0

#init
path =  "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[0:-2]) + "/Data/"
print "Loading BUYS data"
linhas = read_single_file(path + "buys-proc-basico.dat")
print len(linhas), "lines loaded"
print

arq_w = open(path + "soldability.dat", "w")

linhas_item_1st_column = []


###ordenar as linhas por item para iterar em "blocos" de itens, evitar complexidade n2
print "Formating buy data to sort by item"
for linha in linhas:
	linhas_item_1st_column.append(to_1st_column(linha.split(","), 5))

print "Sorting buys"
linhas_sort = sort(linhas_item_1st_column)
linhas_item_1st_column = None
###

###contar ocorrencia de compras e botar num dicionario
buy_item_occur = {}

item_id_anterior = linhas_sort[0].split(",")[0]
linhas_do_mesmo_item = []

#apenas para poder registrar as linhas da ultima sessão
linhas_sort.append("-1,0,0,0,0.0,0,0")

conta_linhas = 0

for linha in linhas_sort:
	conta_linhas = conta_linhas + 1
	
	linhaSplit = linha.split(",")
	item_id = linhaSplit[0]

	if(item_id != item_id_anterior):
		buy_item_occur[item_id_anterior] = count_buys(linhas_do_mesmo_item)

		#recomeça a juntar as linhas do mesmo item na lista
		linhas_do_mesmo_item = []
		item_id_anterior = item_id
		linhas_do_mesmo_item.append(linha)

	else:
		linhas_do_mesmo_item.append(linha)


	#apenas para dar print no andamento do script
	if (conta_linhas * 100 % len(linhas_sort) == 0):
		print "Processing Buys ", str(((conta_linhas+0.0)/len(linhas_sort)) * 100) + "%" + " done!"

	elif ((len(linhas)/100) == conta_linhas):
		print "Processing Buys ", str(((conta_linhas+0.0)/len(linhas_sort)) * 100) + "%" + " done!"	

print "All item boughts processed"
print
#Daqui para frente faz o mesmo com CLICKS

path =  "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[0:-2]) + "/Data/"
print "Loading CLICKS data"
linhas = read_file_parts(path, "clicks-proc-basico-parteX.dat", "X", [1,2,3,4,5,6])
print len(linhas), "lines loaded"
print

linhas_item_1st_column = []

###ordenar as linhas por item para iterar em "blocos" de itens, evitar complexidade n2
print "Formating click data to sort by item"
for linha in linhas:
	linhas_item_1st_column.append(to_1st_column(linha.split(","), 5))

print "Sorting clicks"
linhas_sort = sort(linhas_item_1st_column)
linhas_item_1st_column = None
###

###contar ocorrencia de compras e botar num dicionario
click_item_occur = {}

item_id_anterior = linhas_sort[0].split(",")[0]
linhas_do_mesmo_item = []

#apenas para poder registrar as linhas da ultima sessão
linhas_sort.append("-1,0,0,0,0.0,0,0")

conta_linhas = 0
percent_done = 0

for linha in linhas_sort:
	conta_linhas = conta_linhas + 1
	
	linhaSplit = linha.split(",")
	item_id = linhaSplit[0]

	if(item_id != item_id_anterior):
		click_item_occur[item_id_anterior] = len(linhas_do_mesmo_item)

		linhas_do_mesmo_item = []
		item_id_anterior = item_id
		linhas_do_mesmo_item.append(linha)

	else:
		linhas_do_mesmo_item.append(linha)

	#apenas para dar print no andamento do script
	if (len(linhas_sort) == conta_linhas):
		percent_done = 100
		conta_linhas = 0
		#print datetime.datetime.now().time().hour, datetime.datetime.now().minute
		print "Done:", (str(percent_done) + "%")

	elif ((len(linhas_sort) / 100) == conta_linhas):
		percent_done = percent_done + 1
		conta_linhas = 0
		#print datetime.datetime.now().time().hour, datetime.datetime.now().minute
		print "Done:", (str(percent_done) + "%")

#agora monta a tabela item, clicados, vendidos
#tabela dos items com venda
print
print "Processing items bought"
for item_b in buy_item_occur.keys():
	if(item_b in click_item_occur.keys()):
		arq_w.write(str(item_b) + "," + str(click_item_occur[item_b]) + "," + str(buy_item_occur[item_b]) + "\n")
		buy_item_occur.pop(item_b, None)
		click_item_occur.pop(item_b, None)

	else:
		arq_w.write(str(item_b) + "," + "ITEM_COMPRADO" + "," + "MAS_NAO_CLICADO" + "\n")

#tabela dos items com click e sem venda
print "Processing items clicks"
for item_c in click_item_occur.keys():
	if(not item_c in buy_item_occur.keys()):
		arq_w.write(str(item_c) + "," + str(click_item_occur[item_c]) + "," + "0" + "\n")
		click_item_occur.pop(item_c, None)

#ao final ele testa se todos os items comprados foram clicados
print
print "WARNING"
print "There is", len(buy_item_occur), "items boughts but not clicked"
print "There is", len(click_item_occur), "items clicked but not saved"

arq_ex = open(path + "sold_exceptions.dat", "w")

for ex in click_item_occur:
	arq_ex.write(ex + "\n")

arq_ex.write("---")

for ex in buy_item_occur:
	arq_ex.write(ex + "\n")

arq_ex.close()

print "million_recursion", million_recursion
