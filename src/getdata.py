import requests
import json

def getdata(url,datatype=None,filename=None):
    try:
        resp = requests.get(url,timeout=6.0)
        #write to file
        if resp.status_code==200:
            print(resp.text)
            if filename and datatype=='json':
                #resp.encoding = 'utf-8'
                f = open(filename,'w',encoding='utf-8')
                json.dump(resp.json(),f)
                f.close()  
            elif filename and datatype=='txt':
                unicstr=resp.content.decode(resp.encoding)
                f = open(filename,'w',encoding='utf-8')
                f.write(unicstr)
                f.close()
                #print(unicstr)
    except Exception as e:
            print(type(e))
            print(e)

    
if __name__ == "__main__":
    numIter=100000
    while numIter>0:
            numIter-=1
            print('CHBTC:')
            getdata('http://api.chbtc.com/data/v1/ticker?currency=btc_cny','json','data_chbtc.json')
            print('\nBITFINEX:')
            getdata("https://api.bitfinex.com/v1/pubticker/btcusd",'json','data_bitfex.json')
            getdata('http://hq.sinajs.cn/list=USDCNY','txt','data_usdcny.txt')
    #input("press <enter> to exit...")
