from pyspark.mllib.tree import RandomForest
from pyspark import SparkContext, SparkConf
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors
import logging
import time, re

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
    return parts

def outro(line):
    a = line.split(',')
    parts =  convertColumns(a)
    return LabeledPoint(parts[-1], Vectors.dense(parts[0:-1]))

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
#buyData = MLUtils.loadLabeledPoints(sc,'/local/data/recsys/treino_test/treino_buy1')
data = sc.textFile( '/local/data/recsysTales/all_samples/trains_tests/train_70nb_90_v.dat')
trainingData = data.map(outro)
log.info("--- %s minutes ---" % ((time.time() - start_time)/60))

#start_time = time.time()
#notBuyData = MLUtils.loadLabeledPoints(sc,'/local/data/recsys/treino_test/treino_nobuy_filtered3')
#log.info("--- %s minutes ---" % ((time.time() - start_time)/60))

#start_time = time.time()
#allData = buyData.union(notBuyData)
#log.info("--- %s minutes ---" % ((time.time() - start_time)/60))

# Split the data into training and test sets (30% held out for testing)
#(trainingData, testData) = parsedData.randomSplit([0.8, 0.2])

# Train a RandomForest model.
log.info("============================================================================TREINANDO")
# print("============================================================================TREINANDO")
start_time = time.time()
model = RandomForest.trainClassifier(trainingData, numClasses=2, categoricalFeaturesInfo={},numTrees=50)
log.info("--- %s minutes ---" % ((time.time() - start_time)/60))

log.info("============================================================================CARREGANDO DADOS DE TESTE")
# print("============================================================================CARREGANDO DADOS DE TESTE")
start_time = time.time()
data2 = sc.textFile( '/local/data/recsysTales/all_samples/trains_tests/test_70nb_90_v.dat')
testData = data2.map(outro)
log.info("--- %s minutes ---" % ((time.time() - start_time)/60))


log.info("============================================================================CALCULANDO METRICA DE ERRO")
start_time = time.time()


# Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
predictions.saveAsTextFile("/local/data/recsys/predicitions.dat")
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
labelsAndPredictions.saveAsTextFile("/local/data/recsys/labelsAndpredictions.dat")
testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
log.info('Test Error = ' + str(testErr))
log.info("--- %s minutes ---" % ((time.time() - start_time)/60))