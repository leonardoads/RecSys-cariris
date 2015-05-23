#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Script to calculate solution score as the formula at Evaluation Measure here http://2015.recsyschallenge.com/challenge.html

#input 1 - real solution file (session;item1,item2,item3)

#input 2 - prediction file (session;item1,item2,item3)

def read_single_file(filename):
    lines = ""

    print "Reading file:", filename
    arq = open(filename, "r")
    lines = arq.readlines()
    arq.close()
    print "File read!"
    return lines

def jaccard_score(items_predicted_list, items_solution_list):
    items_predicted_set = set(items_predicted_list)
    items_solution_set = set(items_solution_list)

    interseccao_len = len(items_predicted_set.intersection(items_solution_set))
    uniao_len = len(items_predicted_set.union(items_solution_set))
    
    return (float(interseccao_len) / float(uniao_len))

def busca_binaria(lista, busca):
    inicio, fim = 0, len(lista)-1
    while inicio <= fim:
        meio = (inicio + fim)/2
        if busca == lista[meio][0]:
            return lista[meio]
        else:
            if lista[meio][0] < busca:
                inicio = meio + 1
            else:
                fim = meio - 1
    return None

def sort(array):
    less = []
    equal = []
    greater = []
    
    if len(array) > 1:
        pivot = array[0][0]
        
        for tupla in array:
            if tupla[0] < pivot:
                less.append(tupla)
            if tupla[0] == pivot:
                equal.append(tupla)
            if tupla[0] > pivot:
                greater.append(tupla)
        # Don't forget to return something!
        return sort(less)+equal+sort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array

import os
import sys
from operator import itemgetter

item_index = 2
buy_sessions_proportion = 0.055
score = 0

real_solution_path = sys.argv[1]
real_solution_lines = read_single_file(real_solution_path)

predict_path = sys.argv[2]
predict_lines = read_single_file(predict_path)


predict_list = []
for linha in predict_lines:

    linha_split = linha.replace("\n", "").replace(" ","").split(";")
    session = int(linha_split[0])
    lista_items = linha_split[1].split(",")

    line_to_tuple = (session, lista_items)

    predict_list.append(line_to_tuple)

predict_lines = None

#SORTING BY SESSION
print "Sorting predict_lines"
predict_list = sorted(predict_list, key=itemgetter(0))


real_solution_list = []
for linha in real_solution_lines:

    linha_split = linha.replace("\n", "").replace(" ","").split(";")
    session = int(linha_split[0])
    lista_items = linha_split[1].split(",")

    line_to_tuple = (session, lista_items)

    real_solution_list.append(line_to_tuple)

real_solution_lines = None


print "Sorting real_solution_lines"
real_solution_list = sorted(real_solution_list, key=itemgetter(0))
print "\nLists sorted"

percent_done = 0
conta_linhas = 0

print "calculating score for", len(predict_list), "sessions"
for tupla in predict_list:
    conta_linhas = conta_linhas + 1

    session_item_list = tupla[1]#.replace("\n", "").replace(" ","").split(";")
    session = tupla[0]

    searched_session = busca_binaria(real_solution_list, session)

    if(searched_session != None):

        #session_item_list = linha.split(";")[1].split(",")
        score = score + buy_sessions_proportion + jaccard_score(lista_items, session_item_list)

    else:
      #  print "sessão, não existe na solução", session
        score = score - buy_sessions_proportion

    #apenas para dar print no andamento do script
    if (len(predict_list) == conta_linhas):
        percent_done = 100
        conta_linhas = 0
        #print datetime.datetime.now().time().hour, datetime.datetime.now().minute
        print "Done:", (str(percent_done) + "%")

    elif ((len(predict_list) / 100) == conta_linhas):
        percent_done = percent_done + 1
        conta_linhas = 0
        #print datetime.datetime.now().time().hour, datetime.datetime.now().minute
        print "Done:", (str(percent_done) + "%")


print "Score", score
