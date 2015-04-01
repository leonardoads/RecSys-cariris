#loading data

data = read.csv("../Data/clicks_parte_1_proc_basico.dat", sep = ",", header = F)
data = rbind(data, read.csv("../Data/clicks_parte_2_proc_basico.dat", sep = ",", header = F))
data = rbind(data, read.csv("../Data/clicks_parte_3_proc_basico.dat", sep = ",", header = F))
data = rbind(data, read.csv("../Data/clicks_parte_4_proc_basico.dat", sep = ",", header = F))

colnames(data) = c("SESSION", "DAY", "MONTH", "YEAR", "TIME", "ITEM", "CATEGORY")

head(data)
