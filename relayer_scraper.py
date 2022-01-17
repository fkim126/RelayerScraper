import requests
import pandas as pd
import numpy as np
import json

def main():
    transferMS()
    # receiveMS()

def transferMS():
    offset = 0
    while offset <= 0:
        urlTransfer = "https://api.mintscan.io/v1/relayer/cosmoshub-4/channel-141/txs?limit=45&offset={}&messageType=TRANSFER".format(str(offset))
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(urlTransfer, headers = headers)
        data_json = response.json()
        
        if response.status_code == 200 and data_json["txs"][0]["data"]["code"] == 0:
            time = data_json["txs"][0]["header"]["timestamp"]
            txhash = data_json["txs"][0]["data"]["txhash"]
            amount = data_json["txs"][0]["data"]["tx"]["body"]["messages"][0]["token"]["amount"]
            senderAddress = data_json["txs"][0]["data"]["tx"]["body"]["messages"][0]["sender"]
            receiverAddress = data_json["txs"][0]["data"]["tx"]["body"]["messages"][0]["receiver"]
            print("Time", time)
            print("TxHash", txhash)
            print("Amount", float(amount)*.000001)
            print("Sender Address", senderAddress)
            print("Receiver Address", receiverAddress)


        offset = offset + 45

def receiveMS():
    ...

if __name__ == '__main__':
    main()