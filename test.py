import urllib3

http = urllib3.PoolManager()
r = http.request('GET', 'https://api.mintscan.io/v1/relayer/cosmoshub-4/channel-141/txs?limit=45&offset=0&messageType=TRANSFER')
print(r.status)