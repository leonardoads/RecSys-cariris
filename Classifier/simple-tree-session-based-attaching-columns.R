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

data = data.frame(data, bought, clicked, is_buy)

colnames(data) <- c("SESSION", "DAY", "MONTH", "YEAR", "TIME", "ITEM", "CATEGORY", "BOUGHT", "CLICKED", "IS_BUY")

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

data_train = rbind(data.buys, data.no.buys.subset)
sapply(data_train, class)

#finalizando o modelo
data_train$YEAR = NULL

#liberando memoria
data = NULL
data.buys = NULL
data.no.buys = NULL
data.no.buys.subset = NULL
buy.sessions = NULL
no.buy.sessions = NULL
no.buy.subset.sessions = NULL
is_buy = NULL
gc()

#data_train$CATEGORY <- as.factor(data_train$CATEGORY)

model <- C5.0(data_train[-9], as.factor(data_train$IS_BUY))
model
summary(model)

pred = predict(model, data_test[-9])

CrossTable(data_train$IS_BUY, pred, prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE, dnn = c('actual default', 'predicted default'))

write(capture.output(CrossTable(data_train$IS_BUY, pred, prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE, dnn = c('actual default', 'predicted default'))), "/home/ubuntu/dev/RecSys-cariris/Data/reports/basic+clicked+bought.txt")
