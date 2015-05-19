#!/bin/sh

path_input="/local/data/recsys/predictions/predicitions_real_10_50/part-*"
path_predictions="/local/data/recsys/predictions/predicitions_real_10_50/predictionsTeste.dat"
path_bought_data="/local/data/recsys/predictions/outputs/compras_10_50.dat"
cat $path_input > $path_predictions
Rscript saveToOutroOutput.R $path_predictions $path_bought_data
python convertToOutput.py $path_bought_data

