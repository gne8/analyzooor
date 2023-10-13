import requests
import datetime
import csv

address = '0xCa6868F11a099295Fe7F3BDD705d2d7a1c2214B7'
api = f'https://explorer.mantle.xyz/api?module=account&action=txlist&address={address}'

response = requests.get(api)
with open('data/test_transaction_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'datetime', 'nonce', 'blockNumber', 'from', 'to', 'gasUsed', 'hash'])
    for i in response.json()['result']:
        timestamp = i['timeStamp']
        dt = datetime.datetime.fromtimestamp(int(timestamp))
        nonce = i['nonce']
        blockNumber = i['blockNumber']
        address_from = i['from']
        address_to = i['to']
        gasUsed = i['gasUsed']
        hash_txn = i['hash']
        writer.writerow([timestamp,dt,nonce,blockNumber,address_from,address_to,gasUsed,hash_txn])
