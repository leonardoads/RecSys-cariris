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
no.buys.proportion = as.numeric(args[5])

#SET THE BALANCE STYLE (SESSION OR CLICK) BASED
balance = args[6]

#TEST SIMULATION OR REAL TEST
#TRUE IF YOU WANT TO GENERATE THE REAL TEST PREDICTION
simulation = args[7]

#SAVE summary(model)
save_sm = args[8]

#EXAMPLE OF A TERMINAL COMMAND LINE CALLING
#Rscript session-balanced--decision-tree-classification.R 5 1111 ss-da-mo-ti-it-wk-cl-bo-sd-sc-mn-df-md /home/tales/dev/RecSys-cariris/ session 1 TRUE FALSE
############################################

library("gmodels")
library("C50")
library("data.table")

clicks_source_path = paste(path, "/Data/clicks-proc-basico/", sep = "")

print("Loading data")
data = fread(paste(clicks_source_path, "clicks-proc-basico-parte1.dat", sep = ""), sep = ",", header = F)
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte2.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte3.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte4.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte5.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte6.dat", sep = ""), sep = ",", header = F))

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

if(!is.element("ct", columns_array)){
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
  data = data.frame(data, WEEKDAY = fread(paste(path, "Data/columns/clicks-column-weekday.dat", sep = ""), sep = "\n", header = F))

}

if(is.element("cl", columns_array)){
  column_names[i] <- "CLICKED"
  i = i + 1
  data = data.frame(data, CLICKED = fread(paste(path, "Data/columns/clicks-column-clicked.dat", sep = ""), sep = "\n", header = F))
}

if(is.element("bo", columns_array)){
  column_names[i] <- "BOUGHT"
  i = i + 1
  data = data.frame(data, BOUGHT = fread(paste(path, "Data/columns/clicks-column-bought.dat", sep = ""), sep = "\n", header = F))
}

if(is.element("sd", columns_array)){
  column_names[i] <- "SOLDABILITY"
  i = i + 1
  data = data.frame(data, SOLDABILITY = fread(paste(path, "Data/columns/clicks-column-soldability.dat", sep = ""), sep = "\n", header = F))
}

if(is.element("sc", columns_array)){
  column_names[i] <- "SAME_CAT"
  i = i + 1
  data = data.frame(data, SAME_CAT = fread(paste(path, "Data/columns/clicks-column-same-cat.dat", sep = ""), sep = "\n", header = F))
}

if(is.element("mn", columns_array)){
  column_names[i] <- "SOLD_MEAN"
  i = i + 1
  data = data.frame(data, SOLD_MEAN = fread(paste(path, "Data/columns/clicks-soldability_mean_by_session.dat", sep = ""), sep = "\n", header = F))
}

if(is.element("df", columns_array)){
  column_names[i] <- "SOLD_MEAN_DIFF"
  i = i + 1
  data = data.frame(data, SOLD_MEAN_DIFF = fread(paste(path, "Data/columns/clicks-soldability_mean_diff_by_session.dat", sep = ""), sep = "\n", header = F))
}

if(is.element("md", columns_array)){
  column_names[i] <- "SOLD_MEDIAN"
  i = i + 1
  data = data.frame(data, SOLD_MEAN_DIFF = fread(paste(path, "Data/columns/clicks-soldability_median_by_session.dat", sep = ""), sep = "\n", header = F))
}

if(is.element("sz", columns_array)){
  column_names[i] <- "SESSION_SIZE"
  i = i + 1
  data = data.frame(data, SESSION_SIZE = fread(paste(path, "Data/columns/clicks-column-session-size.dat", sep = ""), sep = "\n", header = F))
}

column_names[i] <- "IS_BUY"
data = data.frame(data, IS_BUY = fread(paste(path, "Data/columns/clicks-column-buy.dat", sep = ""), sep = "\n", header = F))
###################################################
print(column_names)
print(column_names[!is.na(column_names)])
colnames(data) = column_names[!is.na(column_names)]

data.buys = data[data$IS_BUY == 1,]
buy.sessions = data.buys$SESSION
buy.sessions = unique(buy.sessions)

data.no.buys = data[data$IS_BUY == 0,]

if(balance == "session"){
	#identificar as sessoes que nao compraram
	no.buy.sessions = data.no.buys[!is.element(data.no.buys$SESSION, buy.sessions),]$SESSION
	no.buy.sessions = unique(no.buy.sessions)

	#GENERATE data.train WITH SAME NUMBERS OF (SESSION WITH ANY BUY) AND (SESSIONS WITH NO BUY) 
	data.no.buys = data[is.element(data$SESSION, no.buy.sessions),]
	no.buy.subset.sessions = sample(no.buy.sessions)[0: ( no.buys.proportion * (length(buy.sessions)) ) ]
	data.no.buys.subset = data.no.buys[is.element(data.no.buys$SESSION, no.buy.subset.sessions),]
	data.no.buys = NULL
	gc()
	nrow(data.no.buys.subset)

	data.buys = data[is.element(data$SESSION, buy.sessions),]
	nrow(data.buys)

	data.train = rbind(data.buys, data.no.buys.subset)

else if(balance == "click"){
	data.no.buys.subset = sample(data.no.buys)[0: ( no.buys.proportion * (length(data.buys)) ) ]
	data.no.buys = NULL
	gc()
	data.train = rbind(data.buys, data.no.buys.subset)
}

#liberando memoria
data.buys = NULL
gc()

sapply(data.train, class)

#Checar se a o subset de no.buy.sessions preservou o aspecto geral de data.no.buys
#adicionar mais colunas a medida que o modelo cresce
summary(data)
summary(data.train)
data$MONTH = as.factor(data$MONTH)

#liberando memoria
data = NULL
data.no.buys.subset = NULL
data.no.buys = NULL
buy.sessions = NULL
no.buy.sessions = NULL
no.buy.subset.sessions = NULL

# THE COLUMNS SESSION ONLY CAN BE NULLED AFTER BEING USED TO SET DATA.BUYS AND DATA.NO.BUYS
if(!is.element("ss", columns_array)){
  data$SESSION = NULL
  column_names = column_names[column_names != "SESSION"]
}
gc()

################################

error_cost <- matrix(c(aa, ab, ba, bb), nrow = 2)
is_buy_index = length(data.train) * -1

sapply(data.train, class)
head(data.train)

print(paste("Column index to be used as classifier >", (is_buy_index * (-1)), "<"))

#excluding CATEGORY due to missing values from train
data.train$CATEGORY = NULL
gc()

model <- C5.0(data.train[is_buy_index], as.factor(data.train$IS_BUY), trials = n_trees, costs = error_cost)
model
#summary(model)

#head(data.train)

prediction.data.train <- predict(model, data.train)

CrossTable(data.train$IS_BUY, prediction.data.train, prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE, dnn = c('actual default', 'predicted default'))

output_filename = paste("session-based-", "report", "-train-", as.character(no.buys.proportion), "-", "forest", n_trees, "-", "costs", costs, "-", columns, sep = "")
complete_path = paste(path, "/Classifier/reports/", output_filename, ".dat", sep = "")
print(paste("Report saved as ", complete_path))
print("\n")
write(capture.output(CrossTable(data.train$IS_BUY, prediction.data.train, prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE, dnn = c('actual default', 'predicted default'))), complete_path)

data.train = NULL
prediction.data.test = NULL
gc()

if(simulation == "TRUE"){
	print("Trained model will be used to predict real test")
	print("\n")
	print("Loading test data")
	test = fread(paste(path, "/Data/test-proc-basico/test-proc-basico-parte1.dat", sep = ""), sep = ",", header = F)
	test = rbind(test, fread(paste(path, "/Data/test-proc-basico/test-proc-basico-parte2.dat", sep = ""), sep = ",", header = F))
	test = rbind(test, fread(paste(path, "/Data/test-proc-basico/test-proc-basico-parte3.dat", sep = ""), sep = ",", header = F))
	test = rbind(test, fread(paste(path, "/Data/test-proc-basico/test-proc-basico-parte4.dat", sep = ""), sep = ",", header = F))
	test = rbind(test, fread(paste(path, "/Data/test-proc-basico/test-proc-basico-parte5.dat", sep = ""), sep = ",", header = F))
	test = rbind(test, fread(paste(path, "/Data/test-proc-basico/test-proc-basico-parte6.dat", sep = ""), sep = ",", header = F))
	print("Test data loaded")
	print("\n")

	head(test)

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

	if(!is.element("ct", columns_array)){
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
	  test = data.frame(test, WEEKDAY = fread(paste(path, "Data/columns/test-column-weekday.dat", sep = ""), sep = "\n", header = F))
	}

	if(is.element("cl", columns_array)){
	  column_names[i] <- "CLICKED"
	  i = i + 1
	  test = data.frame(test, CLICKED = fread(paste(path, "Data/columns/test-column-clicked.dat", sep = ""), sep = "\n", header = F))
	}

	if(is.element("bo", columns_array)){
	  column_names[i] <- "BOUGHT"
	  i = i + 1
	  test = data.frame(test, BOUGHT = fread(paste(path, "Data/columns/test-column-bought.dat", sep = ""), sep = "\n", header = F))
	}

	if(is.element("sd", columns_array)){
	  column_names[i] <- "SOLDABILITY"
	  i = i + 1
	  test = data.frame(test, SOLDABILITY = fread(paste(path, "Data/columns/test-column-soldability.dat", sep = ""), sep = "\n", header = F))
	}

	if(is.element("sc", columns_array)){
	  column_names[i] <- "SAME_CAT"
	  i = i + 1
	  test = data.frame(test, SAME_CAT = fread(paste(path, "Data/columns/test-column-same-cat.dat", sep = ""), sep = "\n", header = F))
	}
	
	if(is.element("mn", columns_array)){
	  column_names[i] <- "SOLD_MEAN"
	  i = i + 1
	  test = data.frame(test, SOLD_MEAN = fread(paste(path, "Data/columns/test-soldability_mean_by_session.dat", sep = ""), sep = "\n", header = F))
	}
	
	if(is.element("df", columns_array)){
	  column_names[i] <- "SOLD_MEAN_DIFF"
	  i = i + 1
	  test = data.frame(test, SOLD_MEAN_DIFF = fread(paste(path, "Data/columns/test-soldability_mean_diff_by_session.dat", sep = ""), sep = "\n", header = F))
	}
	
	if(is.element("md", columns_array)){
	  column_names[i] <- "SOLD_MEDIAN"
	  i = i + 1
	  test = data.frame(test, SOLD_MEDIAN = fread(paste(path, "Data/columns/test-soldability_median_by_session.dat", sep = ""), sep = "\n", header = F))
	}

	if(is.element("sz", columns_array)){
	  column_names[i] <- "SESSION_SIZE"
	  i = i + 1
	  test = data.frame(test, SESSION_SIZE = fread(paste(path, "Data/columns/test-column-session-size.dat", sep = ""), sep = "\n", header = F))
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

	output_filename = paste("session-based-", as.character(no.buys.proportion), "-forest", n_trees, "-", "costs", costs, "-", columns, sep = "")
	complete_path = paste(path, "/Classifier/predicts/", output_filename, ".dat", sep = "")

	print (paste("Saving predictions as ", complete_path))
	print("\n")
	write.table(test, complete_path, sep=",", row.names=F, col.names=F)

	test = NULL
	prediction = NULL
}

#WARNING: THIS COULD TAKE *TWICE* MORE TIME THAN THE REST OF THE SCRIP, SERIOUSLY
if(save_sm == "TRUE"){
  summary_path = paste(path, "/Classifier/summary_model/", "model-summary-", "report", "-train-", as.character(no.buys.proportion), "-", "forest", n_trees, "-", "costs", costs, "-", columns, ".dat", sep = "")
  write(capture.output(summary(model)), summary_path)
}

model = NULL
gc()
