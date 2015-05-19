import sys
import os

print "Loading data"
#path = '/local/data/recsysTales/all_samples/trains_tests/test_70nb_90_s.dat'
path = '/local/data/recsys/outputs/compras_10.dat'
arq_r = open(path, "r")
linhas = arq_r.readlines()
arq_r.close()
print "Data loaded"
count = 0
milhas = 0
session_proxima = 0
session_items = ""
arq_w = open(path.replace(".dat","-formated.dat"), "w")
linhas.append("0,0,0")
for i in range(len(linhas) - 1):
    if(count % 1000 == 1):
        print milhas
        milhas = milhas + 1
    count = count + 1
    linha = linhas[i].replace("\n", "").split(",")
    session_atual = linha[0]
    session_proxima = linhas[i + 1].replace("\n", "").split(",")[0]
    item = linha[1]
#    pred = linha[2]
    session_items = session_items + item + ","
    if(session_atual != session_proxima):
        session_item_list = session_items[0:len(session_items)-1].split(",")
        item_set = set(session_item_list)
        session_items = ",".join(list(item_set))
        arq_w.write(session_atual + ";" + session_items + "\n")
        session_items = ""
arq_w.close()
