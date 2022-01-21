import requests
import random
import csv
import concurrent.futures

proxylist = []

with open('proxylist.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        proxylist.append(row[0])

def extract(proxy):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        r = requests.get("https://api.mintscan.io/v1/relayer/cosmoshub-4/channel-141/txs?limit=45&offset=0&messageType=RECEIVE", headers=headers, proxies={'http':proxy, 'https':proxy}, timeout=2)
        print(r.json(), ' | Works')
    except:
        print('none')
        pass
    return proxy

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(extract, proxylist)