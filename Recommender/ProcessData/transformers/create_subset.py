import csv

clicksPath = "/home/andryw/Documents/yoochoose/new_clicks"
buysPath = "/home/andryw/Documents/yoochoose/yoochoose-buys.dat"
buysOutputPath = ""
clickOutputPath = ""

def get_sessions(numberSessionBuy):
    sessions = set()
    rows = []
    with open(buysPath, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            sessions.add(row[0])
            if len(sessions) > numberSessionBuy:
                sessions.remove(row[0])
                return sessions,rows
            rows.append(row)

    return rows

def get_clicks(sessions,numberSessionNotBuy):
    sessionsNotBuy = set()
    rows = []

    with open(clicksPath, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            print "oi"
sessions,rows = get_sessions(5)
clicks = get_clicks(sessions,995)

save(sessions,buysOutputPath)
save(sessions,clickOutputPath)