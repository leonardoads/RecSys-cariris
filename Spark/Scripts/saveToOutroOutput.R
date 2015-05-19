library(data.table)
path = "/local/data/recsys/"
path_data = paste(path,"data/",sep="")
path_predictions = paste(path,"predictions/",sep="")
args <- commandArgs(trailingOnly = TRUE)
predic_file = args[1] #"predicitions_real_10.dat/tudo.dat"
output = args[2] #outputs/compras_10.dat/
test = fread(paste(path_data,"real_test_i.dat",sep=""))
predictions = fread(predic_file)
test_predic = cbind(test,predictions)
colnames(test_predic) <- c("session","item","predic")
bought_data = test_predic[predic == 1,]
write.table(bought_data, output,
            row.names = FALSE,col.names = FALSE,quote = FALSE,sep = ",")
