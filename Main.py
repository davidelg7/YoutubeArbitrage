from Arbitrage import *
import time
from Graph import *



if __name__=="__main__":

    allCoins=getAllCoins()

    start_coin="USDT"
    end_coin="USDT"
    intervallo_controllo=10
    soglia_profittabilità=0.00001

    I=0
    


    while True:
        curr_time=time.time()

        prices= getPrices()

        price_time=time.time()

        G=Graph(allCoins,prices)
        graph_time=time.time()

        soluzioni_possibili=path(G,start_coin,end_coin)
        soluzioni_arricchite=enrich(G,soluzioni_possibili)
        paths_time=time.time()

        print(f"Run {I}")
        print(f"Tempo necessario all'ottenimento dei prezzi :{price_time-curr_time:.2f}")
        print(f"Tempo necessario al calcolo del grafo :{graph_time-price_time:.2f}")
        print(f"Tempo necessario al calcolo delle possibili soluzioni :{paths_time-graph_time:.2f}")


        for i,percorso in enumerate(soluzioni_arricchite[:5]):
            if percorso["profit"]>soglia_profittabilità+1:
                print(i,percorso["path"],percorso["profit"])

        time.sleep(intervallo_controllo)
        I+=1

