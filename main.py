import requests
import json


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

with open('store_id.txt', 'r') as f:
    for line in f:
        storeId.append(line)
    f.close()

print(len(storeId))

productid = ['1000672643']

for i in range(len(storeId)):
    storeid = storeId[i].replace('\n','')
    client = requests.Session()
    url = 'https://www.lowes.com/pd/1000672643/productdetail/{}/Guest'.format(storeid)
    r =requests.get(url, headers=headers)
    print(url)
    productData = json.loads(r.text)
    print(productData['productDetails']['1000672643']['price'])

