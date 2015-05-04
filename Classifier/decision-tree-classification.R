library("gmodels")
library("C50")

data = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/clicks-proc-basico/clicks-proc-basico-parte1.dat", sep = ",", header = F)
data = rbind(data, read.csv("/home/ubuntu/dev/RecSys-cariris/Data/clicks-proc-basico/clicks-proc-basico-parte2.dat", sep = ",", header = F))
data = rbind(data, read.csv("/home/ubuntu/dev/RecSys-cariris/Data/clicks-proc-basico/clicks-proc-basico-parte3.dat", sep = ",", header = F))
data = rbind(data, read.csv("/home/ubuntu/dev/RecSys-cariris/Data/clicks-proc-basico/clicks-proc-basico-parte4.dat", sep = ",", header = F))
data = rbind(data, read.csv("/home/ubuntu/dev/RecSys-cariris/Data/clicks-proc-basico/clicks-proc-basico-parte5.dat", sep = ",", header = F))
data = rbind(data, read.csv("/home/ubuntu/dev/RecSys-cariris/Data/clicks-proc-basico/clicks-proc-basico-parte6.dat", sep = ",", header = F))

is_buy = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/columns/clicks-column-buy.dat", sep = ",", header = F)

bought = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/columns/clicks-column-bought.dat", sep = ",", header = F)
clicked = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/columns/clicks-column-clicked.dat", sep = ",", header = F)
#soldability = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/columns/clicks-column-soldability.dat", sep = ",", header = F)
same_cat = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/columns/clicks-column-same-cat.dat", sep = ",", header = F)

#data = data.frame(data, clicked, bought, soldability, same_cat, is_buy)
data = data.frame(data, clicked, bought, same_cat, is_buy)

#liberando memoria
is_buy = NULL
bought = NULL
clicked = NULL
#soldability = NULL
same_cat = NULL
gc()

#colnames(data) <- c("SESSION", "DAY", "MONTH", "YEAR", "TIME", "ITEM", "CATEGORY", "CLICKED", "BOUGHT", "SOLDABILITY", "SAME_CAT", "IS_BUY")
colnames(data) <- c("SESSION", "DAY", "MONTH", "YEAR", "TIME", "ITEM", "CATEGORY", "CLICKED", "BOUGHT", "SAME_CAT", "IS_BUY")

data.buys = data[data$IS_BUY == 1,]
buy.sessions = data.buys$SESSION
buy.sessions = unique(buy.sessions)

#identificar as sessoes que nao compraram
data.no.buys = data[data$IS_BUY == 0,]
no.buy.sessions = data.no.buys[!is.element(data.no.buys$SESSION, buy.sessions),]$SESSION
no.buy.sessions = unique(no.buy.sessions)

#liberando memoria
data.buys = NULL
data.no.buys = NULL
gc()

#nao sei como fazer permutaca randomica de array... replicavel... o sample nao eh replicavel
#set.seed(1234)
data.no.buys = data[is.element(data$SESSION, no.buy.sessions),]
no.buy.subset.sessions = sample(no.buy.sessions)[0:length(buy.sessions)]
data.no.buys.subset = data.no.buys[is.element(data.no.buys$SESSION, no.buy.subset.sessions),]

data.buys = data[is.element(data$SESSION, buy.sessions),]

#Checar se a o subset de no.buy.sessions preservou o aspecto geral de data.no.buys
#adicionar mais colunas a medida que o modelo cresce
summary(data.no.buys$DAY)
summary(data.no.buys.subset$DAY)
summary(data.no.buys$MONTH)
summary(data.no.buys.subset$MONTH)
summary(data.no.buys$TIME)
summary(data.no.buys.subset$TIME)
summary(data.no.buys$BOUGHT)
summary(data.no.buys.subset$BOUGHT)
summary(data.no.buys$CLICKED)
summary(data.no.buys.subset$CLICKED)
summary(data.no.buys$SOLDABILITY)
summary(data.no.buys.subset$SOLDABILITY)
summary(data.no.buys$SAME_CAT)
summary(data.no.buys.subset$SAME_CAT)

data_train = rbind(data.buys, data.no.buys.subset)
sapply(data_train, class)

#finalizando o modelo
data_train$YEAR = NULL
data_train$CATEGORY = NULL

#liberando memoria
data = NULL
data.no.buys.subset = NULL
data.no.buys = NULL
buy.sessions = NULL
no.buy.sessions = NULL
no.buy.subset.sessions = NULL
gc()

n_trees = 5
error_cost <- matrix(c(1, 1, 3, 3), nrow = 2)

#model <- C5.0(data_train[-8], as.factor(data_train$IS_BUY), trials = n_trees, costs = error_cost)
model <- C5.0(data_train[-8], as.factor(data_train$IS_BUY), trials = n_trees)
model
summary(model)

data_train = NULL
gc()

test = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/test-proc-basico/test-proc-basico-parte1.dat", sep = ",", header = F)
test = rbind(test, read.csv("/home/ubuntu/dev/RecSys-cariris/Data/test-proc-basico/test-proc-basico-parte2.dat", sep = ",", header = F))
test = rbind(test, read.csv("/home/ubuntu/dev/RecSys-cariris/Data/test-proc-basico/test-proc-basico-parte3.dat", sep = ",", header = F))
test = rbind(test, read.csv("/home/ubuntu/dev/RecSys-cariris/Data/test-proc-basico/test-proc-basico-parte4.dat", sep = ",", header = F))
test = rbind(test, read.csv("/home/ubuntu/dev/RecSys-cariris/Data/test-proc-basico/test-proc-basico-parte5.dat", sep = ",", header = F))
test = rbind(test, read.csv("/home/ubuntu/dev/RecSys-cariris/Data/test-proc-basico/test-proc-basico-parte6.dat", sep = ",", header = F))

bought = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/columns/test-column-bought.dat", sep = ",", header = F)
clicked = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/columns/test-column-clicked.dat", sep = ",", header = F)
#soldability = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/columns/test-column-soldability.dat", sep = ",", header = F)
same_cat = read.csv("/home/ubuntu/dev/RecSys-cariris/Data/columns/test-column-same-cat.dat", sep = ",", header = F)

#test = data.frame(test, bought, clicked, soldability, same_cat)
test = data.frame(test, bought, clicked, same_cat)

#bought = NULL
#clicked = NULL
soldability = NULL
same_cat = NULL
gc()

#colnames(test) <- c("SESSION", "DAY", "MONTH", "YEAR", "TIME", "ITEM", "CATEGORY", "CLICKED", "BOUGHT", "SOLDABILITY", "SAME_CAT")
colnames(test) <- c("SESSION", "DAY", "MONTH", "YEAR", "TIME", "ITEM", "CATEGORY","BOUGHT", "CLICKED", "SAME_CAT")

test$YEAR = NULL
test$CATEGORY = NULL
gc()

prediction <- predict(model, test)

test = data.frame(test$SESSION, test$ITEM, prediction)

colnames(test) <- c("SESSION", "ITEM", "PRED")

test = test[test$PRED == 1,]


write.table(test, "/home/ubuntu/dev/RecSys-cariris/Classifier/predicts/forest5-ss-da-mo-ti-it-cl-bo-sc.dat", sep=",", row.names=F, col.names=F, quote=F)

