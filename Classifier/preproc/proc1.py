#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Gerar uma tabela substituindo a coluna TIMESTAMP por DAY, MOTH, YEAR , TIME

#INPUT
#SESSION	TIMESTAMP					ITEM		CATEGORY
#1,			2014-04-07T10:51:09.277Z,	214536502,	0
#1,			2014-04-07T10:54:09.868Z,	214536500,	0
#1,			2014-04-07T10:54:46.998Z,	214536506,	0
#1,			2014-04-07T10:57:00.306Z,	214577561,	0

#OUTPUT - clicks_proc1.dat
#SESSION, 	DAY, 	MONTH, 	YEAR, 	TIME, 	ITEM, 		CATEGORY
#1,			7,		4,		2014,	10.85,	214536502,	0
#1,			7,		4,		2014,	10.9,	214536500,	0
#1,			7,		4,		2014,	10.9,	214536506,	0
#1,			7,		4,		2014,	10.95,	214577561,	0

def read_file_parts(path, pattern_filename, match_numeric, list_index):
	list_temp = []

	for i in list_index:
		print "Reading file:", pattern_filename.replace(match_numeric, str(i))
		arq = open(path + pattern_filename.replace(match_numeric, str(i)), "r")
		list_temp = list_temp + arq.readlines()
		arq.close()

	return list_temp

def split_timestamp(linha):
	linhaSplit = linha.split(",")
	ano = linhaSplit[1][0:4]
	mes = linhaSplit[1][5:7]
	dia = linhaSplit[1][8:10]
	hora = linhaSplit[1][11:13]
	minuto = linhaSplit[1][14:16]
	minuto_fraction = int(minuto) / 60.
	return (linhaSplit[0] + "," + dia + "," + mes + "," + ano + "," + hora + "." + str(minuto_fraction)[2:] + "," + linhaSplit[2] + "," + linhaSplit[3])

#init
path = "/home/tales/development/Git/RecSys-cariris/Data/"
print "Loading CLICKS data"
linhas = read_file_parts(path, "yoochoose-clicks-3M-parteX.dat", "X", [1,2,3])
print len(linhas), "lines loaded"

arq_w = open(path + "clicks_proc_basico.dat","w")

for linha in linhas:
	arq_w.write(split_timestamp(linha))

arq_w.close()