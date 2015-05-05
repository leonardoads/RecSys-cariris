###### get arguments from command line #####
options(echo=TRUE) # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE)

#NMBER OF TREES FOR TRIALS
n_trees = as.integer(args[1])

#MATRIX COSTS
costs = args[2]
aa = as.integer(substring(costs, 1, 1))
ab = as.integer(substring(costs, 2, 2))
ba = as.integer(substring(costs, 3, 3))
bb = as.integer(substring(costs, 4, 4))

#COLUMNS TO BE USED IN THE MODEL
columns = args[3]
columns_array = substring(columns, seq(1,nchar(columns),3), seq(2,nchar(columns),3))

#PATH TO THE PROJECT
path = args[4]

#TRAIN PARTITION
train_partition_percent = as.integer(args[5])

#TEST SIMULATION OR REAL TEST
simulation = args[6]

############################################


library("gmodels")
library("C50")

clicks_source_path = paste(path, "/Data/clicks-proc-basico/", sep = "")

data = read.csv(paste(clicks_source_path, "clicks-proc-basico-parte1.dat", sep = ""), sep = ",", header = F)
data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte2.dat", sep = ""), sep = ",", header = F))
data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte3.dat", sep = ""), sep = ",", header = F))
data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte4.dat", sep = ""), sep = ",", header = F))
data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte5.dat", sep = ""), sep = ",", header = F))
data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte6.dat", sep = ""), sep = ",", header = F))

print(nrow(data))

print (columns_array)
column_names = c()
i = 1

##### BASIC ATTRIBUTES #####
column_names[i] <- "SESSION"
i = i + 1
column_names[i] <- "DAY"
i = i + 1
column_names[i] <- "MONTH"
i = i + 1
column_names[i] <- "YEAR"
i = i + 1
column_names[i] <- "TIME"
i = i + 1
column_names[i] <- "ITEM"
i = i + 1
column_names[i] <- "CATEGORY"
i = i + 1

colnames(data) = column_names
###########################


##### REMOVE NOT ASKED COLUMNS FROM BASIC DATA #####
if(!is.element("ss", columns_array)){
  data$SESSION = NULL
}

if(!is.element("da", columns_array)){
  data$DAY = NULL
}

if(!is.element("mo", columns_array)){
  data$MONTH = NULL
}

if(!is.element("yr", columns_array)){
  data$YEAR = NULL
}

if(!is.element("ti", columns_array)){
  data$TIME = NULL
}

if(!is.element("it", columns_array)){
  data$ITEM = NULL
}

if(!is.element("ca", columns_array)){
  data$CATEGORY = NULL
}
###################################################
gc()

######## ADDING NEW COLUMNS TO BASIC DATA #########
if(is.element("wk", columns_array)){
  column_names[i] <- "WEEKDAY"
  i = i + 1
  data = data.frame(data, WEEKDAY = read.csv(paste(path, "Data/columns/clicks-column-weekday.dat", sep = ""), sep = ",", header = F)[0:nrow(data),])
}

if(is.element("cl", columns_array)){
  column_names[i] <- "CLICKED"
  i = i + 1
  data = data.frame(data, CLICKED = read.csv(paste(path, "Data/columns/clicks-column-clicked.dat", sep = ""), sep = ",", header = F)[0:nrow(data),])
}

if(is.element("bo", columns_array)){
  column_names[i] <- "BOUGHT"
  i = i + 1
  data = data.frame(data, BOUGHT = read.csv(paste(path, "Data/columns/clicks-column-bought.dat", sep = ""), sep = ",", header = F)[0:nrow(data),])
}

if(is.element("sd", columns_array)){
  column_names[i] <- "SOLDABILITY"
  i = i + 1
  data = data.frame(data, SOLDABILITY = read.csv(paste(path, "Data/columns/clicks-column-soldability.dat", sep = ""), sep = ",", header = F)[0:nrow(data),])
}

if(is.element("sc", columns_array)){
  column_names[i] <- "SAME_CAT"
  i = i + 1
  data = data.frame(data, SAME_CAT = read.csv(paste(path, "Data/columns/clicks-column-same-cat.dat", sep = ""), sep = ",", header = F)[0:nrow(data),])
}

column_names[i] <- "IS_BUY"
data = data.frame(data, IS_BUY = read.csv(paste(path, "Data/columns/clicks-column-buy.dat", sep = ""), sep = ",", header = F)[0:nrow(data),])
###################################################


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


#GENERATE data.balanced WITH SAME NUMBERS OF (SESSION WITH ANY BUY) AND (SESSIONS WITH NO BUY) 
data.no.buys = data[is.element(data$SESSION, no.buy.sessions),]
no.buy.subset.sessions = sample(no.buy.sessions)[0:length(buy.sessions)]
data.no.buys.subset = data.no.buys[is.element(data.no.buys$SESSION, no.buy.subset.sessions),]

data.buys = data[is.element(data$SESSION, buy.sessions),]

data.balanced = rbind(data.buys, data.no.buys.subset)
sapply(data.balanced, class)

#Checar se a o subset de no.buy.sessions preservou o aspecto geral de data.no.buys
#adicionar mais colunas a medida que o modelo cresce
summary(data)
summary(data.balanced)

#liberando memoria
data = NULL
data.no.buys.subset = NULL
data.no.buys = NULL
buy.sessions = NULL
no.buy.sessions = NULL
no.buy.subset.sessions = NULL
gc()

### TRAIN AND TEST PARTITIONS ##
set.seed(23456)
n.data = nrow(data.balanced)
data.balanced <- data.balanced[order(runif(nrow(data.balanced))), ]

print (train_partition_percent)

train_partition_size = (train_partition_percent / 100) * n.data

print(train_partition_size)

if(train_partition_size == 100){
        data.train = data.balanced
        data.test = data.balanced

}else{
        data.train = data.balanced[0:train_partition_size,]
        data.test = data.balanced[train_partition_size + 1 : n.data,]

}

################################


error_cost <- matrix(c(aa, ab, ba, bb), nrow = 2)
is_buy_index = length(data.train) * -1

print(is_buy_index)

model <- C5.0(data.train[is_buy_index], as.factor(data.train$IS_BUY), trials = n_trees, costs = error_cost)
model

prediction.data.test <- predict(model, data.test)

CrossTable(data.test$IS_BUY, prediction.data.test, prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE, dnn = c('actual default', 'predicted default'))

output_filename = paste("report", as.character(train_partition_percent), "-", as.character(100 - train_partition_percent), "-", "forest", n_trees, "-", "costs", costs, "-", columns, sep = "")
complete_path = paste(path, "/Classifier/reports/", output_filename, ".dat", sep = "")
write(capture.output(CrossTable(data.test$IS_BUY, prediction.data.test, prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE, dnn = c('actual default', 'predicted default'))), complete_path)

data.train = NULL
data.test = NULL
data.balanced = NULL
prediction.data.test = NULL
gc()

test = read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte1.dat", sep = ""), sep = ",", header = F)
test = rbind(test, read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte2.dat", sep = ""), sep = ",", header = F))
test = rbind(test, read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte3.dat", sep = ""), sep = ",", header = F))
test = rbind(test, read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte4.dat", sep = ""), sep = ",", header = F))
test = rbind(test, read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte5.dat", sep = ""), sep = ",", header = F))
test = rbind(test, read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte6.dat", sep = ""), sep = ",", header = F))

column_names = c()
i = 1
##### BASIC ATTRIBUTES #####
column_names[i] <- "SESSION"
i = i + 1
column_names[i] <- "DAY"
i = i + 1
column_names[i] <- "MONTH"
i = i + 1
column_names[i] <- "YEAR"
i = i + 1
column_names[i] <- "TIME"
i = i + 1
column_names[i] <- "ITEM"
i = i + 1
column_names[i] <- "CATEGORY"
i = i + 1

colnames(test) = column_names
###########################

##### REMOVE NOT ASKED COLUMNS FROM BASIC DATA #####
if(!is.element("ss", columns_array)){
  test$SESSION = NULL
}

if(!is.element("da", columns_array)){
  test$DAY = NULL
}

if(!is.element("mo", columns_array)){
  test$MONTH = NULL
}

if(!is.element("yr", columns_array)){
  test$YEAR = NULL
}

if(!is.element("ti", columns_array)){
  test$TIME = NULL
}

if(!is.element("it", columns_array)){
  test$ITEM = NULL
}

if(!is.element("ca", columns_array)){
  test$CATEGORY = NULL
}
###################################################
gc()


######## ADDING NEW COLUMNS TO BASIC DATA #########
if(is.element("wk", columns_array)){
  column_names[i] <- "WEEKDAY"
  i = i + 1
  test = data.frame(test, WEEKDAY = read.csv(paste(path, "Data/columns/test-column-weekday.dat", sep = ""), sep = ",", header = F))
}

if(is.element("cl", columns_array)){
  column_names[i] <- "CLICKED"
  i = i + 1
  test = data.frame(test, CLICKED = read.csv(paste(path, "Data/columns/test-column-clicked.dat", sep = ""), sep = ",", header = F))
}

if(is.element("bo", columns_array)){
  column_names[i] <- "BOUGHT"
  i = i + 1
  test = data.frame(test, BOUGHT = read.csv(paste(path, "Data/columns/test-column-bought.dat", sep = ""), sep = ",", header = F))
}

if(is.element("sd", columns_array)){
  column_names[i] <- "SOLDABILITY"
  i = i + 1
  test = data.frame(test, SOLDABILITY = read.csv(paste(path, "Data/columns/test-column-soldability.dat", sep = ""), sep = ",", header = F))
}

if(is.element("sc", columns_array)){
  column_names[i] <- "SAME_CAT"
  i = i + 1
  test = data.frame(test, SAME_CAT = read.csv(paste(path, "Data/columns/test-column-same-cat.dat", sep = ""), sep = ",", header = F))
}
###################################################
gc()

head(test)

print (column_names)

prediction <- predict(model, test)

test = data.frame(test$SESSION, test$ITEM, prediction)

colnames(test) <- c("SESSION", "ITEM", "PRED")

test = test[test$PRED == 1,]

output_filename = paste("forest", n_trees, "-", "costs", costs, "-", columns, sep = "")
complete_path = paste(path, "/Classifier/predicts/", output_filename, ".dat", sep = "")

print (complete_path)
write.table(test, complete_path, sep=",", row.names=F, col.names=F)

test = NULL
prediction = NULL
model = NULL
gc()
