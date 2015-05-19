library("data.table")
clicks_source_path = "/local/data/recsysTales/"

data = fread(paste(clicks_source_path, "clicks-proc-basico-parte1.dat", sep = ""), sep = ",", header = F)
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte2.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte3.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte4.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte5.dat", sep = ""), sep = ",", header = F))
data = rbind(data, fread(paste(clicks_source_path, "clicks-proc-basico-parte6.dat", sep = ""), sep = ",", header = F))

#data = fread(paste(clicks_source_path, "clicks-proc-basico.dat", sep = ""), sep = ",", header = F)

#data = data[-1,]
data = cbind(data,fread(paste(clicks_source_path, "clicks-column-weekday.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, CLICKED = fread(paste(clicks_source_path, "clicks-column-clicked.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, BOUGHT = fread(paste(clicks_source_path, "clicks-column-bought.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SOLDABILITY = fread(paste(clicks_source_path, "clicks-column-soldability.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SAME_CAT = fread(paste(clicks_source_path, "clicks-column-same-cat.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SOLD_MEAN = fread(paste(clicks_source_path, "clicks-soldability_mean_by_session.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SOLD_MEAN_DIFF = fread(paste(clicks_source_path, "clicks-soldability_mean_diff_by_session.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SOLD_MEDIAN = fread(paste(clicks_source_path, "clicks-soldability_median_by_session.dat", sep = ""), sep = "\n", header = F))
data = cbind(data, SOLD_MEDIAN = fread(paste(clicks_source_path, "clicks-column-buy.dat", sep = ""), sep = "\n", header = F))


write.table(data,file=paste(clicks_source_path, "alldata.dat", sep = ""),sep=",",row.names=FALSE,col.names = FALSE,quote=FALSE)

