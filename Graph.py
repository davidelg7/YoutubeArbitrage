
import pandas as pd 

class Graph:

    def __init__(self,coins: list, prices: pd.DataFrame):

        self.coins=coins
        self.prices=prices

        self.buy_edges=self.buyEdges(prices)
        self.sell_edges=self.sellEdges(prices)


    @staticmethod
    def buyEdges(prices: pd.DataFrame):
        edges={}

        for index,row in prices.iterrows():
            c1= row["baseAsset"]
            c2= row["quoteAsset"]

            ask=row["ask"]

            if c2 in edges:
                edges[c2][c1]={"price":ask,"type":"BUY","ticker":c1+c2,"c1":c1,"c2":c2}
            else:
                edges[c2] = {c1: {"price": ask, "type": "BUY", "ticker": c1 + c2, "c1": c1, "c2": c2}}

        return edges

    @staticmethod
    def sellEdges(prices: pd.DataFrame):
        edges = {}
        for index, row in prices.iterrows():
            c1 = row["baseAsset"]
            c2 = row["quoteAsset"]
            bid = row["bid"]
            if c1 in edges:
                edges[c1][c2] = {"price": bid, "type": "SELL", "ticker": c1 + c2, "c1": c1, "c2": c2}
            else:
                edges[c1] = {c2: {"price": bid, "type": "SELL", "ticker": c1 + c2, "c1": c1, "c2": c2}}
        return edges

    def outerEdgesOf(self,vertex):
        outer_edges=[]
        if vertex in self.sell_edges:
            for edge in self.sell_edges[vertex]:
                outer_edges.append({"out": edge, "edge":self.sell_edges[vertex][edge]})
        if vertex in self.buy_edges:
            for edge in self.buy_edges[vertex]:
                outer_edges.append({"out": edge, "edge":self.buy_edges[vertex][edge]})
        return outer_edges



def path(G: Graph, start, end, limit=3, p=None, all_paths=None, max_l=10):
    #inizializziamo se è la prima invocazione
    if all_paths==None:
        all_paths=[]
    
    if p==None:
        p=[]

    p.append(start)
    #valido, quindi lo aggiungo alla lista delle possibili soluzioni
    if start==end and len(p)==limit+1:
        all_paths.append(p)
        return all_paths
    #non valido quindi non lo aggiungo
    if len(p)==limit+1:
        return all_paths
    
    for outer_edges in G.outerEdgesOf(start)[:max_l]:
        out= outer_edges["out"]

        if out not in p or len(p)==limit:
            path(G,out,end,limit,p.copy(),all_paths,max_l)
    return all_paths



def calcProfit(pt):
    p=1

    for op in pt:
        if op["type"]=="BUY":
            p*=1/op["exchange_rate"]
        else:
            p*=op["exchange_rate"]

    return p



def enrich(G: Graph,paths: list):

    p=[]
    for path in paths:
        plan=[]
        for c1,c2 in zip(path[:-1],path[1:]):
            d=None
            if c1 in G.buy_edges and c2 in G.buy_edges[c1]:
                d={"from":c1,"to":c2, "c1": G.buy_edges[c1][c2]["c1"], "c2":G.buy_edges[c1][c2]["c2"],
                 "exchange_rate": G.buy_edges[c1][c2]["price"],  "type": G.buy_edges[c1][c2]["type"]}
            if c1 in G.sell_edges and c2 in G.sell_edges[c1]:
                d = {"from": c1, "to": c2, "c1": G.sell_edges[c1][c2]["c1"], "c2": G.sell_edges[c1][c2]["c2"],
                     "exchange_rate": G.sell_edges[c1][c2]["price"], "type": G.sell_edges[c1][c2]["type"]}
            plan.append(d)

        p.append({"plan": plan, "profit": calcProfit(plan), "path": path, "start": path[0]})
    return p
