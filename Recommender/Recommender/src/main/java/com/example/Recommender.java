package com.example;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.common.FastIDSet;
import org.apache.mahout.cf.taste.impl.common.LongPrimitiveIterator;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.similarity.EuclideanDistanceSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.LogLikelihoodSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;

class Recommender {
    public static void main(String[] args) throws IOException, TasteException {
        String pathClicks = "/home/andryw/Documents/yoochoose/new_clicks";
        String pathBuys = "/home/andryw/Documents/yoochoose/buys_filt.dat";

        DataModel dataModelClicks = new FileDataModel(new File(pathClicks));
        DataModel dataModelBuys = new FileDataModel(new File(pathBuys));


        UserSimilarity similarity = new LogLikelihoodSimilarity(dataModelClicks);
        long USER_ID = 12;

        for (Double thresSim : new Double[]{0.5,0.6,0.7,0.8,0.9}){
            UserNeighborhood neighborhood = new NearestNUserNeighborhood(20,thresSim,similarity,dataModelClicks);
            long[] neighborhoodS = neighborhood.getUserNeighborhood(USER_ID);
            HashMap<Long,Long> buyables = buyable(dataModelBuys, neighborhoodS);
            for (Double thresPred : new Double[]{0.5,0.6,0.7,0.8,0.9}) {

                List<Long> predictions = prediction(USER_ID, dataModelClicks, buyables,thresPred);
                System.out.println(thresSim + " " + thresPred + " " + predictions);
            }
        }


    }

    private static List<Long> prediction(Long userID, DataModel dataModelClicks, HashMap<Long, Long> buyables, Double threshold) throws TasteException {
        FastIDSet clicks = dataModelClicks.getItemIDsFromUser(userID);

        LongPrimitiveIterator it = clicks.iterator();
        HashMap<Long, Long> buyOfClcks = new HashMap<>();

        while(it.hasNext()){
            long click = it.nextLong();
            long value = buyables.get(click) == null ? 0 : buyables.get(click);
            buyOfClcks.put(click,value);
        }
        int size = buyOfClcks.size();
        List<Long> predictions = new ArrayList<Long>();

        for (long key : buyOfClcks.keySet()){
            long count = buyOfClcks.get(key);
            Double prob = count*1.0 / size;

            if (prob >= threshold){
                predictions.add(key);
            }
        }

        return predictions;
    }

    private static HashMap<Long, Long> buyable(DataModel dataModelBuys, long[] neighborhoodS)  {
        HashMap<Long,Long> numberOfItems = new HashMap<Long,Long>();

        for (long l :neighborhoodS){
            FastIDSet buys = null;
            try {
                buys = dataModelBuys.getItemIDsFromUser(l);
            } catch (TasteException e) {
                continue;
            }
            LongPrimitiveIterator it = buys.iterator();
            while(it.hasNext()){
                long next = it.next();
                Long total = numberOfItems.get(next);
                if (total == null){
                    numberOfItems.put(next,0l);
                }
                numberOfItems.put(next,numberOfItems.get(next)+ 1);
            }
        }
        return numberOfItems;
    }
}
