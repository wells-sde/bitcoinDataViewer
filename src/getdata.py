import requests
import json

def getpricedata(url,filename=None):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    print(resp.text)
    #write to file
    if(filename):
        f = open(filename,'w')
        json.dump(resp.json(),f)
        f.close()
    
if __name__ == "__main__":
    print('CHBTC:')
    getpricedata('http://api.chbtc.com/data/v1/ticker?currency=btc_cny','data_chbtc.json')
    print('\nBITFINEX:')
    getpricedata("https://api.bitfinex.com/v1/pubticker/btcusd",'data_bitfex.json')
    input("press <enter> to exit...")
