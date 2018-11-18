import csv
import os
import math
import pickle
import sys
from NewsGraph import NewsGraph
from datetime import date
from datetime import timedelta

csv.field_size_limit(1310720)

names=[]

for filename in os.listdir(os.getcwd()+'/items_list'):
    with open(os.getcwd()+'/items_list/'+filename) as namefile:
        for name in namefile:
            names.append(name.replace('\n',''))

names = list(set(names)) # unique the name list

cnt = 1

if not os.path.isfile('hk01.news_graph'):
    ng = NewsGraph()
    with open('data/hk01.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            find = []
            for name in names:
                if row[1].find(name) >= 0 or row[2].find(name) >= 0:
                    contribution = max(( 1 if row[1].find(name) != -1 else 0 ), ( ( 1 - row[2].find(name) * 1.0 / ( len(row[2]) + 1) ) if row[2].find(name) != -1 else 0 ))
                    find.append ((name, contribution))
                    #print name, contribution
            if len(find) > 1:
                for x in find:
                    for y in find:
                        if x[0] != y[0]:
                            ng.add_day_news_count( x[0], y[0], math.pow(x[1]*y[1], 2), int(row[0]) )
            cnt += 1
    pickle.dump(ng, open('hk01.news_graph', 'wb'))
else:
    ng = pickle.load(open('hk01.news_graph', 'rb'))

rank = ng.get_importance(1)
names = [name for name, v in rank.iteritems()]
print "Day\t"+"\t".join(names)

d0 = date(2015,1,1)
for i in xrange(1040,1416):
    rank = ng.get_importance(i)
    values = [str(v*10000) for k, v in rank.iteritems()]
    d1 = d0 + timedelta(days=i-1)
    print d1.strftime("%Y-%m-%d") + "\t" + "\t".join(values)
