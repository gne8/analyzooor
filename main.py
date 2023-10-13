import requests
import csv

# Test Random Address
address = '0xCa6868F11a099295Fe7F3BDD705d2d7a1c2214B7'
urls = {
    'token': f'https://api.debank.com/token/cache_balance_list?user_addr={address}',
    'protocol': f'https://api.debank.com/portfolio/project_list?user_addr={address}' 
}

response = requests.get(urls['token'])
print(response)

with open('data/test_token_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in response.json()['data']:
        if i['chain'] == 'mnt':
            writer.writerow([i])

response = requests.get(urls['protocol'])
print(response)
with open('data/test_protocol_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in response.json()['data']:
        if i['chain'] == 'mnt':
            writer.writerow([i]) 