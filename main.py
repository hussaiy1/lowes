import requests
import json
import os
import threading
import math
import random

headers={
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.38 Safari/537.36',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'connection':'keep-alive',
    'Host': 'www.lowes.com'
}

if os.path.exists('testData.csv'):
    os.remove('testData.csv')
else:
    pass


storeId = []
productid = []

with open('store_id.txt', 'r') as f:
    for line in f:
        line = line.replace('\n', '')
        storeId.append(line)
    f.close()

with open('prodid.txt', 'r') as f:
    for link in f:
        link = link.replace('\n', '')
        productid.append(link)

total_tasks = len(productid) * len(storeId)

proxyList=[]

def loadProxyUserPass():
    global proxyList
    with open('proxies.txt') as f:
        file_content = f.read()
    file_rows = file_content.split('\n')
    for i in range(0, len(file_rows)):
        if ':' in file_rows[i]:
            tmp = file_rows[i]
            tmp = tmp.split(':')
            proxies = {'http': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/',
                       'https': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/'}
            proxyList.append(proxies)

def excelWrite(store, title, price):
        with open('testData.csv', 'a') as f:
            f.write('{} | {} | {} \n'.format(store, title, price))
        


def response(product, store):
    client = requests.Session()
    client.proxies = random.choice(proxyList)
    url = 'https://www.lowes.com/pd/{}/productdetail/{}/Guest'.format(product, store)
    r =client.get(url, headers=headers)
    return r

def getPrice(r, product, store):
    productData = json.loads(r.text)
    pricing = productData['productDetails'][product]['price']
    title = productData['productDetails'][product]['product']['title']
    if pricing != None:
        price = pricing['itemPrice']
        print('{} - {}'.format(store, title))
    else:
        price = '-'
        print('{} - {}'.format(store, title))

    excelWrite(store, title, price)


with open('testData.csv', 'w') as f:
    f.write('Store | Title | Price \n')
        


loadProxyUserPass()
threads = []


if len(storeId)%100 != 0:
    maxVal = math.ceil(len(storeId)/100)
else:
    maxVal = len(storeId)/100

x = 0
y=0
while x<=maxVal/2 and y<=maxVal:
    y = int(maxVal/2)
    for i in range(0,50):
        for j in range(len(productid)):
            storeId_2 = storeId[(x*100):(x+1)*100]
            storeId_3 = storeId[(y*100):(y+1)*100]
            if len(storeId_3)==0:
                print('Process Complete')
            else:
                try:
                    t0 = threading.Thread(target=getPrice, args=(response(productid[j], storeId_2[(2*i)+1]), productid[j], storeId_2[(2*i)+1],))
                    t1 = threading.Thread(target=getPrice, args=(response(productid[j], storeId_2[(2*i)]), productid[j], storeId_2[(2*i)],))
                    t2 = threading.Thread(target=getPrice, args=(response(productid[j], storeId_3[(2*i)+1]), productid[j], storeId_3[(2*i)+1],))
                    t3 = threading.Thread(target=getPrice, args=(response(productid[j], storeId_3[(2*i)]), productid[j], storeId_3[(2*i)],))
                    t0.start()
                    t1.start()
                    t2.start()
                    t3.start()
                    t0.join()
                    t1.join()
                    t2.join()
                    t3.join()
                except IndexError:
                    print('List out of range')
                except requests.exceptions.ProxyError:
                    print("Proxy Error")
                
    y+=1
    x += 1
    
print('Process Complete')
exit()


#index error
#def getPrice(product, store):
#    #client = requests.Session()
#    #url = 'https://www.lowes.com/pd/{}/productdetail/{}/Guest'.format(product, store)
#    #r =client.get(url, headers=headers)
#    productData = json.loads(r.text)
#    pricing = productData['productDetails'][product]['price']
#    title = productData['productDetails'][product]['product']['title']
#    if pricing != None:
#        price = pricing['itemPrice']
#        print('{} - {}'.format(store, title))
#    else:
#        price = '-'
#        print('{} - {}'.format(store, title))
#
#    with open('testData.csv','a') as f:
#        f.write('{} | {} | {} \n'.format(store, title, price))
#        f.close()
#
#with open('testData.csv', 'w') as f:
#    f.write('Store | Title | Price \n')
#    f.close()



#for i in range(len(storeId)):
#    for j in range(len(productid)):
#        getPrice(productid[j], storeId[i])
#
#STORE INFO:
#https://www.lowesforpros.com/wcs/resources/store/10151/storelocation/v1_0?maxResults=1&query=1055
