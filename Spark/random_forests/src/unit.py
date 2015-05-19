from pyspark.mllib.tree import RandomForest
from pyspark import SparkContext, SparkConf
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors
import logging
import time, os, sys
import re

def union(line):
    predic = line[0]
    values = line[1]
    #if(predic == u'1.0'):
    return (str(values[0]),str(values[1]))

def saveCSV(line):
    newValue = line[0]+","+line[1]
    return newValue
#    f.write(line[0]+","+line[1])

 #   f.close()

conf = (SparkConf()
         .setMaster("local")
         .setAppName("My app"))
sc = SparkContext(conf = conf)

predicitions = sc.textFile("/local/data/recsys/predicitions_real.dat/",10)

data2 = sc.textFile( '/local/data/recsysTales/all_samples/all_clicks_test_i.dat',10)
#data2 = sc.textFile( '/local/data/recsys/rel_test.dat/',9)

data2 = data2.map(lambda line:line.split(','))
#data2.saveAsTextFile('/local/data/recsys/rel_test.dat/',)
#lines = predicitions.count()
print data2.getNumPartitions()
print predicitions.getNumPartitions()

a = predicitions.zip(data2)
print a.take(3)
paraSalvar =  a.map(union).filter(lambda line: line!=None)
paraSalvar = paraSalvar.map(saveCSV)
print paraSalvar.take(3)
paraSalvar.saveAsTextFile('/local/data/recsysTales/all_samples/output_real')


