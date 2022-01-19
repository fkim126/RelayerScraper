import requests
import time
import csv
import json

def main():
    # transferMS()
    receiveMS()

def transferMS():

    start_time = time.time()
    offset = 0
    txSet = set()
    csvTransfer = open('transfer_transactions.csv', 'w+')

    try:
        writer = csv.writer(csvTransfer, lineterminator='\n')
        writer.writerow(('txHash', 'SenderAddress', 'ReceiverAddress', 'Amount', 'Time'))
        while offset <= 37800:
            urlTransfer = "https://api.mintscan.io/v1/relayer/cosmoshub-4/channel-141/txs?limit=45&offset={}&messageType=TRANSFER".format(str(offset))
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            response = requests.get(urlTransfer, headers = headers)
            data_json = response.json()

            for i in range(45):
                if response.status_code == 200 and data_json["txs"][i]["data"]["code"] == 0:
                    txhash = data_json["txs"][i]["data"]["txhash"]
                    if txhash not in txSet:
                        txSet.add(txhash)
                        timestamp = data_json["txs"][i]["header"]["timestamp"]
                        amount = data_json["txs"][i]["data"]["tx"]["body"]["messages"][0]["token"]["amount"]
                        senderAddress = data_json["txs"][i]["data"]["tx"]["body"]["messages"][0]["sender"]
                        receiverAddress = data_json["txs"][i]["data"]["tx"]["body"]["messages"][0]["receiver"]

                        writer.writerow((txhash, senderAddress, receiverAddress, float(amount)*.000001, timestamp))
            offset = offset + 45
        print("--- %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        print("Error: " + str(e))
    finally:
        print('Done.')
        csvTransfer.close()

def receiveMS():
    start_time = time.time()
    offset = 0
    txSet = set()
    csvReceived = open('received_transactions.csv', 'w+')

    try:
        writer = csv.writer(csvReceived, lineterminator='\n')
        writer.writerow(('txHash', 'SenderAddress', 'ReceiverAddress', 'Amount', 'Time'))
        while offset <= 42885:
            urlReceive = "https://api.mintscan.io/v1/relayer/cosmoshub-4/channel-141/txs?limit=45&offset={}&messageType=RECEIVE".format(str(offset))
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            response = requests.get(urlReceive, headers = headers)
            data_json = response.json()

            for i in range(45):
                if response.status_code == 200 and data_json["txs"][i]["data"]["code"] == 0:
                    txhash = data_json["txs"][i]["data"]["txhash"]
                    if txhash not in txSet:
                        txSet.add(txhash)
                        timestamp = data_json["txs"][i]["header"]["timestamp"]
                        for j in range(1, len(data_json["txs"][i]["data"]["logs"])):
                                if data_json["txs"][i]["data"]["logs"][j]["events"][0]["attributes"][0]["value"] == "/ibc.core.channel.v1.MsgRecvPacket":
                                    jsonString = data_json["txs"][i]["data"]["logs"][j]["events"][1]["attributes"][0]["value"]
                                    aDict = json.loads(jsonString)
                                    amount = aDict["amount"]
                                    senderAddress = aDict["sender"]
                                    receiverAddress = aDict["receiver"]

                        writer.writerow((txhash, senderAddress, receiverAddress, float(amount)*.000001, timestamp))
            offset = offset + 45
        print("--- %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        print("Error: " + str(e))
    finally:
        print('Done.')
        csvReceived.close()

if __name__ == '__main__':
    main()