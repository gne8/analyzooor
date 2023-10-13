import requests
import csv

token = '0x201eba5cc46d216ce6dc03f6a759e8e766e956ae'
token_top_holders_api = f'https://explorer.mantle.xyz/api?module=token&action=getTokenHolders&contractaddress={token}&page=1&offset=100'
token_total_supply_api = f'https://explorer.mantle.xyz/api?module=stats&action=tokensupply&contractaddress={token}'
#response = requests.get(token_top_holders_api)

token_top_holders_response = requests.get(token_top_holders_api) 
print(f"Top Token Holders: {token_top_holders_response.json()['result'][0:5]}")

token_total_supply_response = requests.get(token_total_supply_api) 
print(f"Token Total Supply: {token_total_supply_response.json()['result']}")
