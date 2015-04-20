#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Gerar a informação de BUY, a compra realizada para o par SESSION, ITEM.

#INPUT
##SESSION, 	DAY, 	MONTH, 	YEAR, 	TIME, 	ITEM,		CATEGORY
#14679,		03,		04,		2014,	04.73,	214645087,	0
#14672,		02,		04,		2014,	07.61,	214664919,	0
#14672,		02,		04,		2014,	07.61,	214826625,	0
#14673,		06,		04,		2014,	15.85,	214696625,	0
#14673,		06,		04,		2014,	15.96,	214696740,	0


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

def busca_binaria(lista, busca):
    inicio, fim = 0, len(lista)-1
    while inicio <= fim:
        meio = (inicio + fim)/2
        if busca == lista[meio]:
            return lista.index(lista[meio])
        else:
            if lista[meio] < busca:
                inicio = meio + 1
            else:
                fim = meio - 1
    return None

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

import os
import sys

sys.setrecursionlimit(1000000000)

path =  "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[0:-2]) + "/Data/"
print "Loading CLICKS data"
clicks_lines = read_file_parts(path, "clicks-proc-basico/clicks-proc-basico-parteX.dat", "X", [1,2,3,4,5,6])
print len(clicks_lines), "lines loaded\n"

print "Loading BUYS data"
buys_lines = read_file_parts(path, "buys-proc-basico/buys-proc-basico-parteX.dat", "X", [1,2])
print len(buys_lines), "lines loaded\n"

print "Sorting buys data"
buys_lines = sort(buys_lines)
print "Buys data sorted\n"

#monta uma lista ordenada das sessions em que houve compra
buys_sessions_list = []
buys_items_list = []


count = 0
for linha in buys_lines:
	count = count + 1
	linha_split = linha.replace("\n","").split(",")
	session = linha_split[0]
	item = linha_split[5]
	
	if(not busca_binaria(buys_sessions_list, session)):
		buys_sessions_list.append(session)
		list_temp = [item]
		buys_items_list.append(list_temp)

	else:
		last_index = len(buys_items_list) - 1
		buys_items_list[last_index].append(item)

	if(count % 10000 == 0):
		print "Processing Buys ", str(((count+0.0)/len(buys_lines)) * 100)[0:7] + "%" + " done!"			

conta_linhas = 0

#gera array que representa a info de buy da linha
info_buy = []
for linha in clicks_lines:
	linha_split = linha.replace("\n","").split(",")
	session = linha_split[0]
	item = linha_split[5]

	buy_index = busca_binaria(buys_sessions_list, session)

	if (not buy_index == None):
		#print session, item, buys_items_list[buy_index]
		if (item in buys_items_list[buy_index]):
			info_buy.append(1)
			#print session, item
		else:
			info_buy.append(0)
	else:
		info_buy.append(0)

        if(conta_linhas % 10000 == 0):
		print "Processing Clicks ", str(((conta_linhas+0.0)/len(clicks_lines)) * 100)[0:7] + "%" + " done!"	

print "Processing Clicks  99.5024% done!"

#salvando coluna de info de buy
arq_w = open(path + "columns/clicks-column-buy.dat", "w")
i = 0
for i in range(len(clicks_lines)):
	arq_w.write(str(i))
	arq_w.write("\n")

arq_w.close()
