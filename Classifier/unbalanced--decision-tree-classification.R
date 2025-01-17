	###### get arguments from command line #####
options(echo=TRUE) # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE)

#NMBER OF TREES FOR TRIALS
n_trees = as.integer(args[1])

#MATRIX COSTS
#EXAMPLE 1234 MEANS: FISRT COLUMN 1,2 AND SECOND COLUMN 3,4
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
#Rscript unbalanced--decision-tree-classification.R 1 1133 ss-da-mo-ti-it-sd-sc /local/dev/RecSys-cariris/ 100 TRUE
############################################

library("gmodels")
library("C50")

clicks_source_path = paste(path, "/Data/clicks-proc-basico/", sep = "")

print("Loading data")
data = read.csv(paste(clicks_source_path, "clicks-proc-basico-parte1.dat", sep = ""), sep = ",", header = F)
data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte2.dat", sep = ""), sep = ",", header = F))
data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte3.dat", sep = ""), sep = ",", header = F))
data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte4.dat", sep = ""), sep = ",", header = F))
data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte5.dat", sep = ""), sep = ",", header = F))
data = rbind(data, read.csv(paste(clicks_source_path, "clicks-proc-basico-parte6.dat", sep = ""), sep = ",", header = F))

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

if(!is.element("da", columns_array)){
  data$DAY = NULL
  column_names = column_names[column_names != "DAY"]
}

if(!is.element("mo", columns_array)){
  data$MONTH = NULL
  column_names = column_names[column_names != "MONTH"]
}

if(!is.element("yr", columns_array)){
  data$YEAR = NULL
  column_names = column_names[column_names != "YEAR"]
}

if(!is.element("ti", columns_array)){
  data$TIME = NULL
  column_names = column_names[column_names != "TIME"]
}

if(!is.element("it", columns_array)){
  data$ITEM = NULL
  column_names = column_names[column_names != "ITEM"]
}

if(!is.element("ca", columns_array)){
  data$CATEGORY = NULL
  column_names = column_names[column_names != "CATEGORY"]
}
###################################################
gc()

head(data)

######## ADDING NEW COLUMNS TO BASIC DATA #########
if(is.element("wk", columns_array)){
  column_names[i] <- "WEEKDAY"
  i = i + 1
  data = data.frame(data, WEEKDAY = read.csv(paste(path, "Data/columns/clicks-column-weekday.dat", sep = ""), sep = ",", header = F))
}

if(is.element("cl", columns_array)){
  column_names[i] <- "CLICKED"
  i = i + 1
  data = data.frame(data, CLICKED = read.csv(paste(path, "Data/columns/clicks-column-clicked.dat", sep = ""), sep = ",", header = F))
}

if(is.element("bo", columns_array)){
  column_names[i] <- "BOUGHT"
  i = i + 1
  data = data.frame(data, BOUGHT = read.csv(paste(path, "Data/columns/clicks-column-bought.dat", sep = ""), sep = ",", header = F))
}

if(is.element("sd", columns_array)){
  column_names[i] <- "SOLDABILITY"
  i = i + 1
  data = data.frame(data, SOLDABILITY = read.csv(paste(path, "Data/columns/clicks-column-soldability.dat", sep = ""), sep = ",", header = F))
}

if(is.element("sc", columns_array)){
  column_names[i] <- "SAME_CAT"
  i = i + 1
  data = data.frame(data, SAME_CAT = read.csv(paste(path, "Data/columns/clicks-column-same-cat.dat", sep = ""), sep = ",", header = F))
}

column_names[i] <- "IS_BUY"
data = data.frame(data, IS_BUY = read.csv(paste(path, "Data/columns/clicks-column-buy.dat", sep = ""), sep = ",", header = F))
###################################################
print(column_names)
print(column_names[!is.na(column_names)])
colnames(data) = column_names[!is.na(column_names)]

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
column_names = NULL
gc()

#dados de sessoes com compras
data.buys = data[is.element(data$SESSION, buy.sessions),]

#dados de sessoes sem compras
data.no.buys = data[is.element(data$SESSION, no.buy.sessions),]

#60500 sessoes escolhidas
#levando em consideração a proporção original e as configurações da maquina
#####select.buy.sessions = 60500
#####set.seed(234); buy.sessions.selected = sample(buy.sessions)[0:select.buy.sessions]
#####data.buys.selected = data.buys[is.element(data.buys$SESSION, buy.sessions.selected),]
buy.sessions.selected = buy.sessions#####
data.buys.selected = data.buys#####

#1039500 sessoes escolhidas
#levando em consideração a proporção original e as configurações da maquina
#####select.no.buy.sessions = 1039500
#####set.seed(234); no.buy.sessions.selected = sample(no.buy.sessions)[0:select.no.buy.sessions]
#####data.no.buys.selected = data.no.buys[is.element(data.no.buys$SESSION, no.buy.sessions.selected),]
no.buy.sessions.selected = no.buy.sessions#####
data.no.buys.selected = data.no.buys#####

#Checar se a o comportamento foi preservado
#adicionar mais colunas a medida que o modelo cresce
summary(data.buys)
summary(data.buys.selected)
summary(data.no.buys)
summary(data.no.buys.selected)

#liberando memoria
data = NULL
data.buys = NULL
data.no.buys = NULL
buy.sessions = NULL
no.buy.sessions = NULL
gc()

# THE COLUMNS SESSION ONLY CAN BE NULLED AFTER BEING USED TO SET DATA.BUYS AND DATA.NO.BUYS
if(!is.element("ss", columns_array)){
  data$SESSION = NULL
  column_names = column_names[column_names != "SESSION"]
}
gc()

### TRAIN AND TEST PARTITIONS ##
if(train_partition_percent == 100){
	data.train = rbind(data.buys.selected, data.no.buys.selected)
	data.test = data.train
	print("Model will be trained with 100% of balanced data.set")
	print(paste(nrow(data.test), "test lines"))
	print("\n")

}else{
	#A RANDOM BUY SESSIONS SAMPLE IS TAKEN, CONSIDERING THE PERCENTUAL OF PARTITION TRAIN/TEST
	train_partition_size_buys = (train_partition_percent / 100) * length(buy.sessions.selected)

	#Random sessions
	set.seed(234); train.buy.sessions = sample(buy.sessions.selected)[0:train_partition_size_buys]
	
	data.buys.train = data.buys.selected[is.element(data.buys.selected$SESSION, train.buy.sessions),]
	data.buys.test = data.buys.selected[!is.element(data.buys.selected$SESSION, train.buy.sessions),]


	#A RANDOM NO.BUY SESSIONS SAMPLE IS TAKEN, CONSIDERING THE PERCENTUAL OF PARTITION TRAIN/TEST
	train_partition_size_no_buys = (train_partition_percent / 100) * length(no.buy.sessions.selected)
	
	#Random sessions
	set.seed(234); train.no.buy.sessions = sample(no.buy.sessions.selected)[0:train_partition_size_no_buys]

	data.no.buys.train = data.no.buys.selected[is.element(data.no.buys.selected$SESSION, train.no.buy.sessions),]
	data.no.buys.test = data.no.buys.selected[!is.element(data.no.buys.selected$SESSION, train.no.buy.sessions),]

	data.train = rbind(data.buys.train, data.no.buys.train)
	data.test = rbind(data.buys.test, data.no.buys.test)

	print(paste("Model will be trained with", train_partition_percent, "% of UNBALANCED data.set"))
	print(paste("Tests will be", 100 - train_partition_percent, "% of UNBALANCED data.set"))
	print(paste("It means", nrow(data.test), "lines of test data"))
	print("\n")
	
	data.buys.train = NULL 
	data.no.buys.train = NULL
	train.buy.sessions = NULL
	train.no.buy.sessions = NULL
	gc()
	print (paste(train_partition_percent, "% of training means ", nrow(data.train), " lines", sep = ""))
print("\n")
}

data.buys.selected = NULL
data.no.buys.selected = NULL
buy.sessions.selected = NULL
no.buy.sessions.selected = NULL
gc()

################################

error_cost <- matrix(c(aa, ab, ba, bb), nrow = 2)
is_buy_index = length(data.train) * -1

sapply(data.train, class)
head(data.train)

print(paste("Column index to be used as classifier >", (is_buy_index * (-1)), "<"))

model <- C5.0(data.train[is_buy_index], as.factor(data.train$IS_BUY), trials = n_trees, costs = error_cost)
model
#summary(model)

#head(data.test)
#head(data.balanced)

prediction.data.test <- predict(model, data.test)

CrossTable(data.test$IS_BUY, prediction.data.test, prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE, dnn = c('actual default', 'predicted default'))

output_filename = paste("report", "-ubalanced" ,"-train-", as.character(train_partition_percent), "-", as.character(100 - train_partition_percent), "-", "forest", n_trees, "-", "costs", costs, "-", columns, sep = "")
complete_path = paste(path, "/Classifier/reports/", output_filename, ".dat", sep = "")
print(paste("Report saved as ", complete_path))
print("\n")
write(capture.output(CrossTable(data.test$IS_BUY, prediction.data.test, prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE, dnn = c('actual default', 'predicted default'))), complete_path)

data.train = NULL
data.test = NULL
data.balanced = NULL
prediction.data.test = NULL
gc()

if(simulation == "TRUE" & train_partition_percent == 100){
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
	  column_names = column_names[column_names != "DAY"]
	}

	if(!is.element("mo", columns_array)){
	  test$MONTH = NULL
	  column_names = column_names[column_names != "MONTH"]
	}

	if(!is.element("yr", columns_array)){
	  test$YEAR = NULL
	  column_names = column_names[column_names != "YEAR"]
	}

	if(!is.element("ti", columns_array)){
	  test$TIME = NULL
	  column_names = column_names[column_names != "TIME"]
	}

	if(!is.element("ca", columns_array)){
	  test$CATEGORY = NULL
	  column_names = column_names[column_names != "CATEGORY"]
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
	
	sapply(test, class)
	head(test)

	column_names <- column_names[!is.na(column_names)]
	colnames(test) = column_names

	gc()
	print(column_names)
	sapply(test, class)
	head(test)

	print("Running prediction")
	head(test)
	prediction <- predict(model, test)
	print("Prediction done!")
	print("\n")

	test = data.frame(test$SESSION, test$ITEM, prediction)

	colnames(test) <- c("SESSION", "ITEM", "PRED")

	test = test[test$PRED == 1,]

	output_filename = paste("-ubalanced", "-forest", n_trees, "-", "costs", costs, "-", columns, sep = "")
	complete_path = paste(path, "/Classifier/predicts/", output_filename, ".dat", sep = "")

	print (paste("Saving predictions as ", complete_path))
	print("\n")
	write.table(test, complete_path, sep=",", row.names=F, col.names=F)

	test = NULL
	prediction = NULL
}

model = NULL
gc()
