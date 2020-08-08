import requests
import json
import threading
import os


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

with open('store_id.txt', 'r') as f:
    for line in f:
        line = line.replace('\n', '')
        storeId.append(line)
    f.close()

productid = ['1000967']

#for i in range(len(storeId)):

def getPrice(store):
    client = requests.Session()
    url = 'https://www.lowes.com/pd/1000967/productdetail/{}/Guest'.format(store)
    r =client.get(url, headers=headers)
    
    productData = json.loads(r.text)
    price = productData['productDetails'][productid[0]]['price']
    title = productData['productDetails'][productid[0]]['product']['title']

    print('{} - {}'.format(store, title))
    with open('testData.csv','a') as f:
        f.write('{} | {} | {} \n'.format(store, title, price))
        f.close()

with open('testData.csv', 'w') as f:
    f.write('Store | Title | Price \n')
    f.close()

for i in range(len(storeId)):
    getPrice(storeId[i])

#STORE INFO:
#https://www.lowesforpros.com/wcs/resources/store/10151/storelocation/v1_0?maxResults=1&query=1055
