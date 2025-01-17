library(data.table)
path = "/local/data/recsys/data/"


notBought = fread(paste(path,"clicks_notbought.dat",sep=""))
bought = fread(paste(path,"clicks_bought.dat",sep=""))
numBought = nrow(bought)
index <- 1:nrow(notBought)
trainindex <- sample(index, trunc(numBought*2*0.5))
sampleNotBought = notBought[trainindex,]
numsampleNotBought = nrow(sampleNotBought)

index <- 1:numBought
train_bought_i <- sample(index, trunc(numBought*0.9))
index <- 1:numsampleNotBought
train_notbought_i <- sample(index, trunc(numsampleNotBought*0.9))

train_bought <- bought[train_bought_i,]
test_bought <- bought[-train_bought_i,]

train_notBought <- sampleNotBought[train_notbought_i,]
test_notBought <- sampleNotBought[-train_notbought_i,]


train = rbind(train_bought,train_notBought)
test = rbind(test_bought,test_notBought)

train_v = train[,c(2,3,5,8,9,10,11,12,13,14,15,16),with=FALSE]
test_v = test[,c(2,3,5,8,9,10,11,12,13,14,15,16),with=FALSE]

test_i = test[,c(1,6,16),with=FALSE]
head(train_v)
write.table(rbind(train_v,test_v),paste(path,"trains_tests/sample_50nb.dat",sep=""),row.names = FALSE,col.names = FALSE,quote = FALSE,sep = ",")
write.table(train_v,paste(path,"trains_tests/train_50nb_90_v.dat",sep=""),row.names = FALSE,col.names = FALSE,quote = FALSE,sep = ",")
write.table(test_v,paste(path,"trains_tests/test_50nb_90_v.dat",sep=""),row.names = FALSE,col.names = FALSE,quote = FALSE,sep = ",")

#write.table(test_i[V16 == 1,c(1,2),with=FALSE],"/local/data/recsysTales/all_samples/trains_tests/test_70nb_90_s.dat",row.names = FALSE,col.names = FALSE,quote = FALSE,sep = ",")
