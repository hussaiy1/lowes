import requests
import random
import threading
import json
import time
import os

requests.adapters.DEFAULT_RETRIES = 10

if os.path.exists('Data.csv'):
    os.remove('Data.csv')
else:
    pass

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

storeId = []
productid = []

proxyList = []

csvList = []



def loadProxyUserPass():
    global proxyList
    with open('proxy.txt') as f:
        file_content = f.read()
    file_rows = file_content.split('\n')
    for i in range(0, len(file_rows)):
        if ':' in file_rows[i]:
            tmp = file_rows[i]
            tmp = tmp.split(':')
            proxies = {'http': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/',
                       'https': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/'}
            proxyList.append(proxies)

with open('store_id.txt', 'r') as f:
    for line in f:
        line = line.replace('\n', '')
        storeId.append(line)
    f.close()

with open('prodid.txt', 'r') as f:
    for link in f:
        link = link.replace('\n', '')
        productid.append(link)

urlList = []
retryUrl = []

for i in range(len(storeId)):
    for j in range(len(productid)):
        url  = 'https://www.lowes.com/pd/{}/productdetail/{}/Guest'.format(productid[j], storeId[i])
        urlList.append(url)

#print(len(urlList))  =  112385


def excelWrite(product, wasPrice, price, priceType, availabilityQuantity, store, link, title):
        with open('Data.csv', 'a') as f:
            f.write('{}||{}|{}|||{}|{}|{}|{}|{} \n'.format(product, wasPrice, price, priceType, availabilityQuantity, store, link, title))
            f.close()

def prodData(data, link):
    if data != None:
        urlSplit = link.split('/')
        product = urlSplit[4]
        store = urlSplit[6]
        pricing = data['productDetails'][product]['price']
        title = data['productDetails'][product]['product']['title']
        url = 'https://www.lowes.com' + data['productDetails'][product]['product']['pdURL']
        if pricing != None:
            price = pricing['itemPrice']
            wasPrice = pricing['wasPrice']
            priceType = pricing['displayType']
            availabilityQuantity = data['inventory']['totalAvailableQty']
            print('{} - {}'.format(store, title))
            csvList.append('{}||{}|{}|||{}|{}|{}|{}|{} \n'.format(product, wasPrice, price, priceType, availabilityQuantity, store, url, title))
        else:
            price = '-'
            wasPrice = '-'
            priceType = '-'
            availabilityQuantity = 'Out Of Stock'
            csvList.append('{}||{}|{}|||{}|{}|{}|{}|{} \n'.format(product, wasPrice, price, priceType, availabilityQuantity, store, url, title))
            print('{} - {}'.format(store, title))

def getPrice(link):
    try:
        r = client.get(link, headers=headers, proxies=random.choice(proxyList))
        productData = json.loads(r.text)
        prodData(productData, link)
    except requests.exceptions.ProxyError:
        try :
            print('Proxy Error - Rotating Proxy')
            r = client.get(link, headers=headers, proxies=random.choice(proxyList))
            productData = json.loads(r.text)
            prodData(productData, link)
        except requests.exceptions.ProxyError:
            print('Proxy Error - save for later')
            retryUrl.append(link)


with open('Data.csv', 'w') as f:
    f.write('product_Id | max_price | price_was |price_selling|price_savings_total|price_savings_totalPercentage|price_typeIndicator|availabilityQuantity|storeNumber|urls|title \n')



loadProxyUserPass()

threads=[]

for k in range(len(urlList)):
    client = requests.Session()
    p1 = threading.Thread(target=getPrice, args=(urlList[k],))

    while threading.active_count() > 100:
        time.sleep(25)
    p1.start()
    threads.append(p1)
for thread in threads:
    thread.join()

threads = []

for j in range(len(retryUrl)):
    client = requests.Session()
    p1 = threading.Thread(target=getPrice, args=(retryUrl[j],))

    while threading.active_count() > 200:
        time.sleep(25)
    p1.start()
    threads.append(p1)

for thread in threads:
    thread.join()

for line in csvList:
    with open('data.csv','a') as f:
        f.write(line)

#OpenSSL.SSL.Error: [('system library', 'fopen', 'Too many open files'), ('BIO routines', 'BIO_new_file', 'system lib'), ('x509 certificate routines', 'X509_load_cert_crl_file', 'system lib')]
