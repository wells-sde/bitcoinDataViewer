import os
import sys
import requests

def getpricedata(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    print(resp.text)
    
if __name__ == "__main__":
    getpricedata('http://api.chbtc.com/data/v1/ticker?currency=eth_cny')
