###### get arguments from command line #####
#options(echo=TRUE) # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE)

#NMBER OF TREES FOR TRIALS
n_trees = as.integer(args[1])

#MATRIX COSTS
#EXAMPLE 1234 MEANS: FISRT ROW 1,2 AND SECOND ROW 3,4
costs = args[2]
aa = as.integer(substring(costs, 1, 1))
ab = as.integer(substring(costs, 2, 2))
ba = as.integer(substring(costs, 3, 3))
bb = as.integer(substring(costs, 4, 4))

#COLUMNS TO BE USED IN THE MODEL
#USE THE TWO LETTER THAT INDICATES THE COLUMN IDENTIFIER
#BETWEEN EACH COLUMN IDENTIFIER, USE "-"
#EXAMPLE ss-da-mo-yr-ti-wk-it-ca-cl-bo-sd-sc
#RESPECTIVELY sessio, day, month, year, time, weekday, item, category, clicked, bought, soldability, same_category
columns = args[3]
columns_array = substring(columns, seq(1,nchar(columns),3), seq(2,nchar(columns),3))

#PATH TO THE PROJECT, YOU MUST INCLUDE PROJECT'S ROOT DIRECTORY
path = args[4]

#TRAIN PARTITION
#IF YOU SET IT TO 100, THE TEST PARTITION WILL BE THE SAME AS TRAIN PARTITION
train_partition_percent = as.integer(args[5])

#TEST SIMULATION OR REAL TEST
#TRUE IF YOU WANT TO GENERATE THE REAL TEST PREDICTION
simulation = args[6]

#EXAMPLE OF A TERMINAL COMMAND LINE CALLING
#Rscript decision-tree-classification.R 1 1133 ss-da-mo-ti-sd-sc /local/dev/RecSys-cariris/ 70 TRUE
############################################

library("gmodels")
library("C50")

clicks_source_path = paste(path, "/Data/clicks-proc-basico/", sep = "")

print("Loading data")
data = read.csv(paste(clicks_source_path, "clicks-proc-basico-parte6.dat", sep = ""), sep = ",", header = F)
#data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte2.dat", sep = ""), sep = ",", header = F))
#data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte3.dat", sep = ""), sep = ",", header = F))
#data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte4.dat", sep = ""), sep = ",", header = F))
#data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte5.dat", sep = ""), sep = ",", header = F))
#data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte6.dat", sep = ""), sep = ",", header = F))

print(paste(nrow(data), "lines loaded"))
print("\n")

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
print (paste("balanced dataset has", n.data, "lines"))
print("\n")
data.balanced <- data.balanced[order(runif(nrow(data.balanced))), ]

train_partition_size = (train_partition_percent / 100) * n.data

print (paste(train_partition_percent, "% of training means ", train_partition_size, " lines", sep = ""))
print("\n")

if(train_partition_percent == 100){
	data.train = data.balanced
	data.test = data.balanced
	print("Model will be trained with 100% of balanced data.set")
	print("\n")

}else{
	data.train = data.balanced[0:train_partition_size,]
	data.test = data.balanced[train_partition_size + 1 : n.data,]
	print(paste("Model will be trained with", train_partition_size, "% of balanced data.set"))
	print(paste("Tests will be", 100 - train_partition_size, "% of balanced data.set"))
	print("\n")
}

################################

error_cost <- matrix(c(aa, ab, ba, bb), nrow = 2)
is_buy_index = length(data.train) * -1

model <- C5.0(data.train[is_buy_index], as.factor(data.train$IS_BUY), trials = n_trees, costs = error_cost)
model
#summary(model)

#head(data.test)
#head(data.balanced)

prediction.data.test <- predict(model, data.test)

CrossTable(data.test$IS_BUY, prediction.data.test, prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE, dnn = c('actual default', 'predicted default'))

output_filename = paste("report", "-train-", as.character(train_partition_percent), "-", as.character(100 - train_partition_percent), "-", "forest", n_trees, "-", "costs", costs, "-", columns, sep = "")
complete_path = paste(path, "/Classifier/reports/", output_filename, ".dat", sep = "")
print(paste("Report saved as ", complete_path))
print("\n")
write(capture.output(CrossTable(data.test$IS_BUY, prediction.data.test, prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE, dnn = c('actual default', 'predicted default'))), complete_path)

data.train = NULL
data.test = NULL
data.balanced = NULL
prediction.data.test = NULL
gc()

if(simulation == "TRUE"){
	print("Trained model will be used to predict real test")
	print("\n")
	print("Loading test data")
	test = read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte1.dat", sep = ""), sep = ",", header = F)
	test = rbind(test, read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte2.dat", sep = ""), sep = ",", header = F))
	test = rbind(test, read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte3.dat", sep = ""), sep = ",", header = F))
	test = rbind(test, read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte4.dat", sep = ""), sep = ",", header = F))
	test = rbind(test, read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte5.dat", sep = ""), sep = ",", header = F))
	test = rbind(test, read.csv(paste(path, "/Data/test-proc-basico/test-proc-basico-parte6.dat", sep = ""), sep = ",", header = F))
	print("Test data loaded")
	print("\n")

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

	if(!is.element("ca", columns_array)){
	  test$CATEGORY = NULL
	}
	###################################################
	gc()

	print("Loading additional columns")
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
	print("Aditional columns loaded")
	print("\n")

	gc()

	print("Running prediction")
	prediction <- predict(model, test)
	print("Prediction done!")
	print("\n")

	test = data.frame(test$SESSION, test$ITEM, prediction)

	colnames(test) <- c("SESSION", "ITEM", "PRED")

	test = test[test$PRED == 1,]

	output_filename = paste("forest", n_trees, "-", "costs", costs, "-", columns, sep = "")
	complete_path = paste(path, "/Classifier/predicts/", output_filename, ".dat", sep = "")

	print (paste("Saving predictions as ", complete_path))
	print("\n")
	write.table(test, complete_path, sep=",", row.names=F, col.names=F)

	test = NULL
	prediction = NULL
}

model = NULL
gc()
