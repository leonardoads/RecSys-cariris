#loading data

data = read.csv("../Data/clicks-proc-basico//clicks-proc-basico-parte1.dat", sep = ",", header = F)
data = rbind(data, read.csv("../Data/clicks-proc-basico/clicks-proc-basico-parte2.dat", sep = ",", header = F))
data = rbind(data, read.csv("../Data/clicks-proc-basico/clicks-proc-basico-parte3.dat", sep = ",", header = F))
data = rbind(data, read.csv("../Data/clicks-proc-basico/clicks-proc-basico-parte4.dat", sep = ",", header = F))
data = rbind(data, read.csv("../Data/clicks-proc-basico/clicks-proc-basico-parte5.dat", sep = ",", header = F))
data = rbind(data, read.csv("../Data/clicks-proc-basico/clicks-proc-basico-parte6.dat", sep = ",", header = F))

colnames(data) = c("SESSION", "DAY", "MONTH", "YEAR", "TIME", "ITEM", "CATEGORY")

head(data)
