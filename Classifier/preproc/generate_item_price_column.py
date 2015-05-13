#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Gerar a informação de BUY, a compra realizada para o par SESSION, ITEM.

#INPUT
##SESSION,      DAY,   		MONTH,		YEAR,   TIME,   ITEM,           CATEGORY
#14679,         03,             04,             2014,   04.73,  214645087,      0
#14672,         02,             04,             2014,   07.61,  214664919,      0
#14672,         02,             04,             2014,   07.61,  214826625,      0
#14673,         06,             04,             2014,   15.85,  214696625,      0
#14673,         06,             04,             2014,   15.96,  214696740,      0


#INPUT 2
#SESSION,       DAY,    	MONTH,  	YEAR,   	TIME,   ITEM,           PRICE           QUANTITY
#11,            3,              4,              2014,   	11.07,  214821371,      1046,           1
#11,            3,              4,              2014,   	11.07,  214821371,      1046,           1
#12,            2,              4,              2014,   	10.7,   214717867,      1778,           4
#489758,        6,              4,              2014,   	9.98,   214826955,      1360,           2

#OUTPUT - column-item-price.dat
#1046
#1046
#1778
#1360

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

#monta uma lista ordenada das sessions em que houve compra
buys_items_list = []

arq_logs = open(path + "logs/log_buy_column.txt", "w")

for linha in buys_lines:
	linha_split = linha.replace("\n","").split(",")
	buys_items_list.append(to_1st_column(linha_split, 5))

print "Sorting buys list"
buys_items_list = sort(buys_items_list)
print "Buys list sorted"

map_item_price = {}

print "Mapping buys list"
for linha in buys_items_list:
	linha_split = linha.replace("\n", "").split(",")
	item = linha_split[0]
	price = linha_split[6]

	if(not item in map_item_price.keys()):
		map_item_price[item] = price
print "Buys list mapped"

arq_w = open(path + "/columns/clicks-column-price.dat", "w")

print "Building price columns"
counter = 0
counter_done = 0
for linha in clicks_lines: 
	linha_split = linha.replace("\n", "").split(",")
	item = linha_split[5]
	
	if(item in map_item_price.keys()):
		price = str(map_item_price[item])
		arq_w.write(price + "\n")
	else:
		arq_w.write("-1" + "\n")

	#so para informar o andamento do script
	counter = counter + 1
	counter_done = counter_done + 1 
	if(counter == (len(clicks_lines) / 100000)):
		counter = 0
		print counter_done, "out of", len(clicks_lines), "done!" 

print "Price columns built"
arq_w.close()

for i in map_item_price.keys():
	print i, map_item_price[i]

print len(map_item_price.keys())
print len(buys_items_list)
