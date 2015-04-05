__author__ = 'rodolfo'


# This programm has the fist pre-preocessing
# at the end the file will have the format
# session   item    clicks  bought


import pandas as pd

# Buys Table
def buysTable():
    buys = pd.read_csv("data/yoochoose-buys.dat",
                   names=["session", "timestamp", "item", "price", "qty"],
                   parse_dates=["timestamp"])

    print "\n Buys head \n \n"
    return buys

# Clicks Table
def clicksTable():
    clicks = pd.read_csv("data/yoochoose-clicks.dat",
                     names=["session", "timestamp", "item", "category"],
                     parse_dates=["timestamp"],
                     converters={"category": lambda c: -1 if c == "S" else c})

    print "\n Clicks head \n \n"
    return clicks


# Tell how many itens was bought
def sessionItemBuys():
    buys = buysTable()
    session_item_buys = buys[["session", "item", "qty"]].groupby(["session", "item"]).sum()
    session_item_buys = session_item_buys["qty"]
    session_item_buys = session_item_buys.to_frame("bought")

# So far we have

# session item           bought
# 11      214821371       2
# 12      214717867       4
# 21      214548744       1
# 21      214838503       1
# 33      214706441       2

    print "comecou cliks"
    clicks = clicksTable()
    session_item_clicks = clicks[["session", "item", "timestamp"]].groupby(["session", "item"]).count()
    session_item_clicks = session_item_clicks["timestamp"]
    session_item_clicks = session_item_clicks.to_frame(name="clicks")
    print session_item_clicks

# session item clicks is

# session item         clicks
# 1       214536500       1
# 1       214536502       1
# 1       214536506       1
# 1       214577561       1
# 2       214551617       1
# 2       214662742       2
# 2       214757390       1
# 2       214757407       1


    print "comecou merge"
    session_item_merge = pd.merge(session_item_clicks, session_item_buys, how='outer', left_index=True, right_index=True)
    session_item_merge.fillna(0, inplace=True)
    session_item_merge.to_csv("clicksvsbought.csv")

# Now we have a table like this

# session   item         clicks  bought
# 490437  214716975       0       6
# 490459  214639327       0       1
# 490783  214706460       0       2
# 490792  214821277       0       2



    print "\n fim"

# Main
def main():
    sessionItemBuys()
    pass


if __name__ == '__main__':
    main()