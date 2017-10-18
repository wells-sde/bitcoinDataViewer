import requests
import json

def getpricedata(url,filename=None):
    resp = requests.get(url,timeout=6.0)
    resp.encoding = 'utf-8'
    print(resp.text)
    #write to file
    if(resp.status_code==200 and filename):
        f = open(filename,'w')
        json.dump(resp.json(),f)
        f.close()
    else:
        print(resp.status_code)
    
if __name__ == "__main__":
    numIter=20000
    while numIter>0:
        try:
            print('CHBTC:')
            getpricedata('http://api.chbtc.com/data/v1/ticker?currency=btc_cny','data_chbtc.json')
            print('\nBITFINEX:')
            getpricedata("https://api.bitfinex.com/v1/pubticker/btcusd",'data_bitfex.json')
            numIter-=1
        except Exception as e:
            print(type(e))
            print(e)
    #input("press <enter> to exit...")
