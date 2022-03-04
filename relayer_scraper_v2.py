import time
import csv
import json
import urllib3

def main():
    transferMS()
    receiveMS()

def transferMS():

    start_time = time.time()
    offset = 0
    txSet = set()
    csvTransfer = open('transfer_transactions.csv', 'w+')

    try:
        writer = csv.writer(csvTransfer, lineterminator='\n')
        writer.writerow(('txHash', 'SenderAddress', 'ReceiverAddress', 'Amount', 'Asset', 'Time'))
        while offset <= 37800:
            http = urllib3.PoolManager()
            
            #https://api.mintscan.io/v1/relayer/cosmoshub-4/channel-207/txs?limit=45&offset=0&messageType=TRANSFER JUNO
            #https://api.mintscan.io/v1/relayer/cosmoshub-4/channel-235/txs?limit=45&offset=0&messageType=TRANSFER SCRT
            #osmo
            urlTransfer = "https://api.mintscan.io/v1/relayer/cosmoshub-4/channel-141/txs?limit=45&offset={}&messageType=TRANSFER".format(str(offset))
            r = http.request('GET', urlTransfer)
            data_json = json.loads(r.data.decode('utf8'))

            for i in range(45):
                if r.status == 200 and data_json["txs"][i]["data"]["code"] == 0:
                    txhash = data_json["txs"][i]["data"]["txhash"]
                    if txhash not in txSet:
                        txSet.add(txhash)
                        timestamp = data_json["txs"][i]["header"]["timestamp"]
                        amount = data_json["txs"][i]["data"]["tx"]["body"]["messages"][0]["token"]["amount"]
                        senderAddress = data_json["txs"][i]["data"]["tx"]["body"]["messages"][0]["sender"]
                        receiverAddress = data_json["txs"][i]["data"]["tx"]["body"]["messages"][0]["receiver"]
                        uAsset = data_json["txs"][i]["data"]["tx"]["body"]["messages"][0]["token"]["denom"]
                        
                        #ibc/CDAB23DA5495290063363BD1C3499E26189036302DC689985A7E23F8DF8D8DB0 JUNO
                        #ibc/1542F8DC70E7999691E991E1EDEB1B47E65E3A217B1649D347098EE48ACB580F SCRT
                        if uAsset == "ibc/14F9BC3E44B8A9C1BE1FB08980FAB87034C9905EF17CF2F5008FC085218811CC":
                            asset = "osmo"
                        else:
                            asset = uAsset[1:]

                        writer.writerow((txhash, senderAddress, receiverAddress, float(amount)*.000001, asset, timestamp))
            time.sleep(8)
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
        writer.writerow(('txHash', 'SenderAddress', 'ReceiverAddress', 'Amount', 'Asset', 'Time'))
        while offset <= 42885:
            http = urllib3.PoolManager()
            urlReceive = "https://api.mintscan.io/v1/relayer/cosmoshub-4/channel-141/txs?limit=45&offset={}&messageType=RECEIVE".format(str(offset))
            r = http.request('GET', urlReceive)
            data_json = json.loads(r.data.decode('utf8'))

            for i in range(45):
                if r.status == 200 and data_json["txs"][i]["data"]["code"] == 0:
                    txhash = data_json["txs"][i]["data"]["txhash"]
                    if txhash not in txSet:
                        txSet.add(txhash)
                        timestamp = data_json["txs"][i]["header"]["timestamp"]
                        for j in range(1, len(data_json["txs"][i]["data"]["logs"])):
                            for k in range(len(data_json["txs"][i]["data"]["logs"][j]["events"])):
                                if data_json["txs"][i]["data"]["logs"][j]["events"][k]["type"] == "message" and data_json["txs"][i]["data"]["logs"][j]["events"][k]["attributes"][0]["value"] == "/ibc.core.channel.v1.MsgRecvPacket":
                                    jsonString = data_json["txs"][i]["data"]["logs"][j]["events"][k+1]["attributes"][0]["value"]
                                    aDict = json.loads(jsonString)
                                    amount = aDict["amount"]
                                    senderAddress = aDict["sender"]
                                    receiverAddress = aDict["receiver"]
                                    uAsset = aDict["denom"].split("/")
                                    if uAsset[0] == "uosmo":
                                        asset = "osmo"
                                    else:
                                        asset = "atom"

                                    writer.writerow((txhash, senderAddress, receiverAddress, float(amount)*.000001, asset, timestamp))
            time.sleep(8)
            offset = offset + 45
        print("--- %s seconds ---" % (time.time() - start_time))
    finally:
        print('Done.')
        csvReceived.close()

if __name__ == '__main__':
    main()
