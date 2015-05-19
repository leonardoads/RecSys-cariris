awk -F','  -v OFS=”,” '{if ($16 == "1") {print }  }' alldata.dat > all_clicks_bought.dat
awk -F','  -v OFS=”,” '{if ($16 == "0") {print }  }' alldata.dat > all_clicks_notbought.dat
split -l 1809679 all_clicks_notbought.dat all_clicks_notbought
mv all_clicks_notboughtaa all_clicks_notbought1.dat
cat all_clicks_bought.dat all_clicks_notbought1.dat > all_clicks_sample.dat
cut -d, all_clicks_sample.dat -f 1,6,16 > all_clicks_sample_i.dat
cut -d, all_clicks_sample.dat -f 2,3,5,9,10,11,12,13,14,15,16 > all_clicks_sample_v.dat


split -l 1628711 all_clicks_bought.dat all_clicks_bought_t
split -l 1628711 all_clicks_notbought1.dat all_clicks_notbought_t


cat all_clicks_bought_train all_clicks_notbought_train > all_clicks_train.dat
cat all_clicks_bought_test all_clicks_notbought_test > all_clicks_test.dat
cut -d, all_clicks_train.dat -f 2,3,5,9,10,11,12,13,14,15,16 > all_clicks_train_v.dat
cut -d, all_clicks_test.dat -f 2,3,5,9,10,11,12,13,14,15,16 > all_clicks_test_v.dat

cut -d, all_clicks_train.dat -f 1,6,16 > all_clicks_train_i.dat
cut -d, all_clicks_test.dat -f 1,6,16 > all_clicks_test_i.dat



awk -F','  -v OFS=',' '{if ($3 == "1") {print $1,$2 }  }' all_clicks_test_i.dat > items_bought_test.dat
sort items_bought_test.dat | uniq > items_bought_test_uniq.dat
mv items_bought_test_uniq.dat items_bought_test.dat



mv output/part-00000 output.csv
