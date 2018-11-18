# -*- coding: utf-8 -*-
import networkx as nx
import math
import pickle

class NewsGraph:

    def __init__(self):
        self.edges = {}
        self.alias = {}
        self.nodes = {}
        self.news_exp = 0.25
        self.stable_lamda = 8
        self.forgetting_lamda = 20
        self.projection_factor = 500

    def dist_func ( self, day, cnt, others, N ):
        if N <= day:
            return None
        stable = 0
        for t_day, t_cnt in others.items():
            if N <= t_day: continue
            stable += - self.stable_lamda * math.pow(t_cnt, self.news_exp) / ( N - t_day ) if ( t_day, t_cnt ) !=  ( day, cnt ) else 0
        stable = 2 - math.exp( stable )
        return self.projection_factor * ( 1 - math.exp( - (N-day) /( self.forgetting_lamda * stable * math.pow(cnt, self.news_exp)) ))

    def get_min_dist (self, days, N):
        min_dist = 100000
        for day, cnt in days.items():
            dist = self.dist_func ( day, cnt, days, N )
            min_dist = dist if min_dist > dist and dist != None else min_dist
        return min_dist if min_dist < 100000 else None
        
    def get_unified_name(self, name):
        if self.alias[name] == name:
            return name
        self.alias[name] = get_unified_name(self.alias[name])
        return self.alias[name]

    def add_day_news_count(self, u, v, cnt, day):
        if u > v:
            tmp = u
            u = v
            v = tmp
        self.nodes[u] = u
        self.nodes[v] = v
        self.edges[u] = {} if u not in self.edges else self.edges[u]
        self.edges[u][v] = {} if v not in self.edges[u] else self.edges[u][v]
        self.edges[u][v][day] = cnt if day not in self.edges[u][v] else self.edges[u][v][day] + cnt

    def add_names(self, names):
        # add node for each name
        for name in names:
            self.nodes.append(name)

    def condense_graph(self, N):
        D=nx.Graph()
        for node in self.nodes:
            D.add_node(node)
        for u in self.edges:
            for v in self.edges[u]:
                dist = self.get_min_dist(self.edges[u][v], N)
                if dist == None: continue
                D.add_edge( u, v, weight=dist )
                #D.add_edge(u,v,weight=1)
        return D

    def get_importance(self, N):
        D = self.condense_graph(N)
        return nx.closeness_centrality(D, distance="weight")

if __name__ == "__main__":
    ng = NewsGraph()
    ng.add_day_news_count('林鄭', '李卓人', 3, 40)
    ng.add_day_news_count('林鄭', '馮檢基', 10, 40)
    ng.add_day_news_count('李卓人', '馮檢基', 10, 40)
    ng.add_day_news_count('馮檢基', '楊彧', 2, 40)
    #ng.add_day_news_count('林鄭', '楊彧', 1, 40)
    ng.add_day_news_count('梁耀忠', '林鄭', 1, 40)
    ng.add_day_news_count('梁耀忠', '李卓人', 2, 40)
    #ng.add_day_news_count('梁耀忠', '李卓人', 2, 40)
    ng.add_day_news_count('林鄭', '楊彧', 1, 60)

    pickle.dump(ng, open('hk01.news_graph', 'wb'))
    #ng = pickle.load(open('hk01.news_graph', 'rb'))
    rank = ng.get_importance(1)
    names = [name for name, v in rank.iteritems()]
    print "Day"+"\t"+ '\t'.join(names)
    for i in xrange(41, 100):
        rank = ng.get_importance(i)
        values = [str(v*1000) for k, v in rank.iteritems()]
        print str(i)+"\t"+ '\t'.join( values )
