#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Script to calculate solution score as the formula at Evaluation Measure here http://2015.recsyschallenge.com/challenge.html

#input 1 - solution file (session, item)

#input 2 - prediction file (session; item1, item2, item3)

def read_single_file(filename):
 lines = ""

 print "Reading file:", filename
 print
 arq = open(filename, "r")
 lines = arq.readlines()
 arq.close()

 return lines

def jaccard_score(items_predicted_list, items_solution_list):
 items_predicted_set = set(items_predicted_list)
 items_solution_set = set(items_solution_list)

 interseccao_len = len(items_predicted_set.intersection(items_solution_set))
 uniao_len = len(items_predicted_set.union(items_solution_set))
 
 return (float(interseccao_len) / float(uniao_len))


import sys
item_index = 2
buy_sessions_proportion = 0.055
score = 0

real_solution_path = '/local/data/recsysTales/all_samples/trains_tests/test_70nb_90_s.dat'
real_solution_lines = read_single_file(real_solution_path)

#predict_path = sys.argv[2]
predict_path = '/local/data/recsys/outputs/test_70nb_90-formated.dat'
predict_lines = read_single_file(predict_path)

map_session_items = {line.split(',')[0]: line.strip('\n').split(',')[1:] for line in real_solution_lines}

print("vai ver predicts")

conta_linhas = 0
percent_done = 0
for linha in predict_lines:
 conta_linhas = conta_linhas + 1.

 linha_split = linha.replace("\n", "").split(";")
 session = linha_split[0]
 lista_items = linha_split[1].split(",")

 if(session in map_session_items.keys()):
  #print session, ">>", jaccard_score(lista_items, map_session_items[session])
  score = score + buy_sessions_proportion + jaccard_score(lista_items, map_session_items[session])
  #break
 else:
  score = score - buy_sessions_proportion
#apenas para dar print no andamento do script
 if (len(predict_lines) == conta_linhas):
       percent_done = 100
       conta_linhas = 0
       #print datetime.datetime.now().time().hour, datetime.datetime.now().minute
       print "Done:", (str(percent_done) + "%")

 elif ((len(predict_lines) / 100) == conta_linhas):
       percent_done = percent_done + 1
       conta_linhas = 0
       #print datetime.datetime.now().time().hour, datetime.datetime.now().minute
       print "Done:", (str(percent_done) + "%")

print "Score", score