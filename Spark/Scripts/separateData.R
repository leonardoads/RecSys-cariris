library("data.table")
clicks_source_path = "/local/data/recsysTales/"

data = fread(paste(clicks_source_path, "clicks-proc-basico-parte1.dat", sep = ""), sep = ",", header = F)
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte2.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte3.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte4.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte5.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte6.dat", sep = ""), sep = ",", header = F))

data = cbind(data,fread(paste(clicks_source_path, "clicks-column-weekday.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, CLICKED = fread(paste(clicks_source_path, "clicks-column-clicked.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, BOUGHT = fread(paste(clicks_source_path, "clicks-column-bought.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SOLDABILITY = fread(paste(clicks_source_path, "clicks-column-soldability.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SAME_CAT = fread(paste(clicks_source_path, "clicks-column-same-cat.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SOLD_MEAN = fread(paste(clicks_source_path, "clicks-soldability_mean_by_session.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SOLD_MEAN_DIFF = fread(paste(clicks_source_path, "clicks-soldability_mean_diff_by_session.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SOLD_MEDIAN = fread(paste(clicks_source_path, "clicks-soldability_median_by_session.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, IS_BUY = fread(paste(clicks_source_path, "clicks-column-buy.dat", sep = ""), sep = "\n", header = F))



colnames(data)[1] <- "SESSION"
colnames(data)[-1] <- "IS_BUY"


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


write.table(data.balanced,file=paste(clicks_source_path, "alldataFiltered.dat", sep = ""),sep=",",row.names=FALSE,col.names = FALSE,quote=FALSE)

