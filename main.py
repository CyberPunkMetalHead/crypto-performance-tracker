from binancedata import *
import threading


import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import numpy as np
import pandas as pd

# needed for the binance API and websockets
from binance.client import Client
import csv
import os
import time
from datetime import datetime, date


threads = []
coins = get_coins()
for coin in coins:

    t = threading.Thread(target=get_historical_data, args=(coin, '1 Jan 2017', Client.KLINE_INTERVAL_1DAY) ) #'get_historical_data('ETHUSDT', '1 Jan 2021', Client.KLINE_INTERVAL_1MINUTE)
    t.start()
    threads.append(t)


[thread.join() for thread in threads]

def get_all_filenames():
    return [get_historical_data(coin, '1 Jan 2017', Client.KLINE_INTERVAL_1DAY) for coin in coins]


def main():
    historical_data = get_all_filenames()

    for file in historical_data:
        data = pd.read_csv(f'data/{file}')

        rolling_percentage = data['close']
        rolling_percentage = [(item - rolling_percentage[0]) / rolling_percentage[0]*100 for item in rolling_percentage ]

        timestamp = data['timstamp']
        timestamp = [datetime.fromtimestamp(item/1000) for item in timestamp]

        plt.legend()
        plt.plot(timestamp, rolling_percentage, label=file)
        plt.xlabel("Date")
        plt.ylabel("% gain")

    plt.show()

if __name__ == "__main__":
    main()
