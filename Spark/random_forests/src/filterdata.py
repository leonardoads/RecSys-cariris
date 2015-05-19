from pyspark.mllib.tree import RandomForest
from pyspark import SparkContext, SparkConf
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors

import logging
import time, os, sys

def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

def outro(line):
    a = line.split(',')
    parts = map(lambda x: float(x),a)
    return LabeledPoint(parts[-1], Vectors.dense(parts[0:-1]))


setup_logger('log_filter', '/local/data/recsys/log_filter.log')
log = logging.getLogger('log_filter')

conf = (SparkConf()
         .setMaster("local")
         .setAppName("My app"))
sc = SparkContext(conf = conf)

data = sc.textFile( '/local/data/recsys/treino_test/treinoFilt')

# log.info("============================================================================CARREGANDO DADOS DE TREINO")
print("============================================================================CARREGANDO DADOS DE TREINO")
start_time = time.time()
trainingData = data.map(outro)
log.info("---CONVERT CSV %s minutes ---" % ((time.time() - start_time)/60))

start_time = time.time()
buyData = trainingData.filter(lambda point: point.label == 1)
log.info("--- FILTER BUYDATA %s minutes ---" % ((time.time() - start_time)/60))

start_time = time.time()
buyData.saveAsSequenceFile('/local/data/recsys/treino_test/treino_buy')
log.info("--- SAVE BUYDATA %s minutes ---" % ((time.time() - start_time)/60))

start_time = time.time()
notBuyData = trainingData.filter(lambda point: point.label == 0)
log.info("---FILTER NOBUYDATA %s minutes ---" % ((time.time() - start_time)/60))

start_time = time.time()
notBuyData.saveAsSequenceFile('/local/data/recsys/treino_test/treino_nobuy')
log.info("--- SAVE NOBUYDATA %s minutes ---" % ((time.time() - start_time)/60))

start_time = time.time()
filtered = notBuyData.sample(False,0.05)
log.info("--- SAMPLE BUYDATA %s minutes ---" % ((time.time() - start_time)/60))

start_time = time.time()
filtered.saveAsSequenceFile('/local/data/recsys/treino_test/treino_nobuy_filtered')
log.info("---SAVE FILTERED %s minutes ---" % ((time.time() - start_time)/60))


#
# # log.info("--- %s minutes ---" % ((time.time() - start_time)/60))
#
# # Split the data into training and test sets (30% held out for testing)
# #(trainingData, testData) = parsedData.randomSplit([0.8, 0.2])
#
# # Train a RandomForest model.
# # log.info("============================================================================TREINANDO")
# print("============================================================================TREINANDO")
# start_time = time.time()
# model = RandomForest.trainClassifier(trainingData, numClasses=2, categoricalFeaturesInfo={},numTrees=5)
# # log.info("--- %s minutes ---" % ((time.time() - start_time)/60))
#
# # log.info("============================================================================CARREGANDO DADOS DE TESTE")
# print("============================================================================CARREGANDO DADOS DE TESTE")
# start_time = time.time()
# data2 = sc.textFile( '/local/data/recsys/treino_test/testeFilt')
# testData = data2.map(outro)
# # log.info("--- %s minutes ---" % ((time.time() - start_time)/60))
#
#
# # log.info("============================================================================CALCULANDO METRICA DE ERRO")
# print("============================================================================CARREGANDO DADOS DE TESTCALCULANDO METRICA DE ERRO")
# start_time = time.time()
#
# # Evaluate model on test instances and compute test error
# predictions = model.predict(testData.map(lambda x: x.features))
# predictions.saveAsTextFile("/local/data/recsys/predicitions.dat")
# labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
# labelsAndPredictions.saveAsTextFile("/local/data/recsys/labelsAndpredictions.dat")
# testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
# # log.info('Test Error = ' + str(testErr))
# # log.info("--- %s minutes ---" % ((time.time() - start_time)/60))
#
# #print(labelsAndPredictions)
# #print('Learned classification forest model:')
# #print(model.toDebugString())
#
