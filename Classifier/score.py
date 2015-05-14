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

real_solution_path = sys.argv[1]
real_solution_lines = read_single_file(real_solution_path)

predict_path = sys.argv[2]
predict_lines = read_single_file(predict_path)

#real solution map
map_session_items = {}

#build solution map_session_items
for linha in real_solution_lines:
	linha_split = linha.replace("\n", "").split(",")
	session = linha_split[0]
	item = linha_split[5]

	if(not session in map_session_items.keys()):
		items_temp = [item]
		map_session_items[session] = items_temp

	elif(not item in map_session_items[session]):
		items_temp = map_session_items[session]
		items_temp.append(item)

		map_session_items[session] = items_temp

for linha in predict_lines:

	linha_split = linha.replace("\n", "").split(";")
	session = linha_split[0]
	lista_items = linha_split[1].split(",")

	if(session in map_session_items.keys()):
		print session, ">>", jaccard_score(lista_items, map_session_items[session])
		score = score + buy_sessions_proportion + jaccard_score(lista_items, map_session_items[session])
		#break
	else:
		score = score - buy_sessions_proportion


print "Score", score
