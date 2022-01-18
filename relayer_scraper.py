import requests
import pandas as pd
import numpy as np
import json
import time

def main():
    transferMS()
    # receiveMS()

def transferMS():
    start_time = time.time()
    offset = 0

    while offset <= 37800:
        urlTransfer = "https://api.mintscan.io/v1/relayer/cosmoshub-4/channel-141/txs?limit=45&offset={}&messageType=TRANSFER".format(str(offset))
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(urlTransfer, headers = headers)
        data_json = response.json()

        txSet = set()

        for i in range(45):
            if response.status_code == 200 and data_json["txs"][0]["data"]["code"] == 0:
                print("Counter:", i)

                txhash = data_json["txs"][i]["data"]["txhash"]
                if txhash not in txSet:
                    txSet.add(txhash)
                    timestamp = data_json["txs"][i]["header"]["timestamp"]
                    amount = data_json["txs"][i]["data"]["tx"]["body"]["messages"][0]["token"]["amount"]
                    senderAddress = data_json["txs"][i]["data"]["tx"]["body"]["messages"][0]["sender"]
                    receiverAddress = data_json["txs"][i]["data"]["tx"]["body"]["messages"][0]["receiver"]

                    print("Time", timestamp)
                    print("TxHash", txhash)
                    print("Amount", float(amount)*.000001)
                    print("Sender Address", senderAddress)
                    print("Receiver Address", receiverAddress)
        offset = offset + 45
    print("--- %s seconds ---" % (time.time() - start_time))

def receiveMS():
    ...

if __name__ == '__main__':
    main()