from pyspark.mllib.tree import RandomForest
from pyspark import SparkContext, SparkConf
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors
import logging
import time, os, sys
import re
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


def convertColumns(a):
    parts = []
    map = {"SUN":0,"MON":1,"TUE":2,"WED":3,"THU":4,"FRI":5,"SAT":6}
    for index in range(0, len(a)):
        if (index == 3):
            string_ = re.findall('([A-Z]+)',str(a[index]))[0]
            parts.append(map[string_])
        else:
            parts.append(float(a[index]))
    # if (index in [0, 1, 3, 4, 6, 10]):
    #     parts.append(int(a[index]))
    # elif (index in [2, 5, 7, 8, 9]):
    #     parts.append(float(a[index]))
    return parts

def outro(line):
    a = line.split(',')
    parts =  convertColumns(a)
    return LabeledPoint(parts[-1], Vectors.dense(parts[0:-1]))

def toVector(line):
    a = line.split(',')
    parts =  convertColumns(a)
    return Vectors.dense(parts)


setup_logger('log', '/local/data/recsys/log.log')
log = logging.getLogger('log')

conf = (SparkConf()
         .setMaster("local")
         .setAppName("My app"))
sc = SparkContext(conf = conf)


log.info("============================================================================50 ARVORES, 50% / 50% por clicks _ train e test")
log.info("============================================================================CARREGANDO DADOS DE TREINO")
print("============================================================================CARREGANDO DADOS DE TREINO")
start_time = time.time()

data = sc.textFile( '/local/data/recsys/data/trains_tests/sample_50nb.dat')
trainingData = data.map(outro)
log.info("--- %s minutes ---" % ((time.time() - start_time)/60))


# Train a RandomForest model.
log.info("============================================================================TREINANDO")

start_time = time.time()
model = RandomForest.trainClassifier(trainingData, numClasses=2, categoricalFeaturesInfo={3:7},numTrees=50)
log.info("--- %s minutes ---" % ((time.time() - start_time)/60))

log.info("============================================================================CARREGANDO DADOS DE TESTE")
start_time = time.time()
data2 = sc.textFile( '/local/data/recsys/data/real_test_v.dat')
testData = data2.map(toVector)
log.info("--- %s minutes ---" % ((time.time() - start_time)/60))


log.info("============================================================================CALCULANDO METRICA DE ERRO")
# print("============================================================================CARREGANDO DADOS DE TESTCALCULANDO METRICA DE ERRO")
start_time = time.time()

#print trainingData.take(2)
#print testData.take(2)

# Evaluate model on test instances and compute test error
predictions = model.predict(testData)

predictions.saveAsTextFile("/local/data/recsys/predictions/predicitions_real_50_50")
#labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
#labelsAndPredictions.saveAsTextFile("/local/data/recsys/labelsAndpredictions.dat")
#testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
#log.info('Test Error = ' + str(testErr))
log.info("--- %s minutes ---" % ((time.time() - start_time)/60))

#print('Learned classification forest model:')
#print(model.toDebugString())

             
