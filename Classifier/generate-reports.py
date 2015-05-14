import os
from os import listdir
from os.path import isfile, join
import sys

rep_dir = sys.argv[1]


def get_files_in_dir(dir_path):
	return [ f for f in listdir(dir_path) if isfile(join(dir_path,f)) ]


dir_path =  os.path.dirname(os.path.realpath(__file__)) + "/" + rep_dir + "/"
file_paths = get_files_in_dir(dir_path)


for path in file_paths:
	if("report" in path):

		arq = open(dir_path + path, "r")

		lines = arq.readlines()

		falso_positivo = lines[15].split("|")[2]
		falso_negativo = lines[18].split("|")[1]
		positivo_verdadeiro = lines[18].split("|")[2]

		print path
		print "precision", float(positivo_verdadeiro) / (float(positivo_verdadeiro) + float(falso_positivo)), "> > >", positivo_verdadeiro, falso_positivo
		print "recall", float(positivo_verdadeiro) / (float(positivo_verdadeiro) + float(falso_negativo)), "> > >", positivo_verdadeiro, falso_negativo
		print "\n"
