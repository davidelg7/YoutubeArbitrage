#USDT->BTC->ETH->USDT 10->10.1

from binance.client import Client 
import numpy as np 
import pandas as pd
price_client=Client()

info=price_client.get_exchange_info()

ALL_SYMBOLS=[]
SYMBOLS_COINS_PAIR={}

for s in info["symbols"]:
    isFuture="UP" in s["symbol"] or "DOWN" in s["symbol"]
 
    if s["status"] =="TRADING" and not isFuture:
        ALL_SYMBOLS.append((s["baseAsset"],s["quoteAsset"]))
        SYMBOLS_COINS_PAIR[s["symbol"]]={"baseAsset":s["baseAsset"],"quoteAsset":s["quoteAsset"]}


ALL_COINS=list(set([baseAsset for baseAsset,quoteAsset in ALL_SYMBOLS]+[quoteAsset for baseAsset,quoteAsset in ALL_SYMBOLS]))

print("Correntemente stiamo considerando ",len(ALL_COINS)," Coins")
print("Correntemente stiamo considerando ",len(ALL_SYMBOLS)," Mercati")

DATA={d["baseAsset"]+d["quoteAsset"]:d for d in info["symbols"]}

def getSymbols():
    return ALL_SYMBOLS
def getData():
    return DATA
def getAllCoins():
    return ALL_COINS
def getSymbolsCoinsPairs():
    return SYMBOLS_COINS_PAIR

def orderbookTickers():
    data=price_client.get_orderbook_tickers()
    data=[d for d in data if float(d["askQty"])>0 and d["symbol"] in SYMBOLS_COINS_PAIR]
    return data


def getPrices():
    prices=orderbookTickers()
    symbols=[p["symbol"] for p in prices]
    ask=[float(p["askPrice"]) for p in prices]
    bid=[float(p["bidPrice"]) for p in prices]
    prices=np.array([(float(p["askPrice"])+float(p["bidPrice"]))/2 for p in prices])
    df=pd.DataFrame()
    df["s"]=symbols
    df["quoteAsset"]=[getSymbolsCoinsPairs()[symbol]["quoteAsset"] for symbol in symbols]
    df["baseAsset"]=[getSymbolsCoinsPairs()[symbol]["baseAsset"] for symbol in symbols]
    df["prices"]=np.array(prices,dtype=float)
    df["bid"]=np.array(bid,dtype=float)
    df["ask"]=np.array(ask,dtype=float)
    df.index=df.s
    return df

# print(getPrices())