import modules
from modules.utils import custom_csv
import pandas as pd
from dotenv import load_dotenv
import os
import requests
import csv
import datetime

# Load Proxy
load_dotenv()
proxies = {
    'http': os.getenv("PROXY"),
    'https': os.getenv("PROXY"), 
}

# Test Random Address
address_list = [
    os.getenv("ADDRESS_1"),
    os.getenv("ADDRESS_2"),
    os.getenv("ADDRESS_3"),
    os.getenv("ADDRESS_4"),
    os.getenv("ADDRESS_5")
]

def call_debank_api_and_write_csv(address='',proxies='',token_csv='',protocol_csv=''):
    # initialize debank module
    temp_ = modules.Debank(address)
    
    # Call Debank API
    temp_.get_debank('token')
    temp_.get_debank('protocol')

    # Write CSV 
    custom_csv.write_csv_filter_mnt_as_it_is(temp_.api_result['token'],token_csv)
    custom_csv.write_csv_filter_mnt_as_it_is(temp_.api_result['protocol'],protocol_csv)

def call_mantle_scan_api_and_write_csv(address='',proxies='',transaction_csv=''):

    # Call Transactions API
    transactions_api = f'https://explorer.mantle.xyz/api?module=account&action=txlist&address={address}'
    response = requests.get(transactions_api)

    # Write CSVs
    with open(transaction_csv, 'w', newline='') as f:
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

for address in address_list:
    # Create address DIR if it doesn't exist
    dir_name = f'data/{address}'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    # Functions Calling For Data Extraction
    call_debank_api_and_write_csv(address,proxies,f"{dir_name}/mnt_debank_token_data.csv",f"{dir_name}/mnt_debank_protocol_data.csv")
    call_mantle_scan_api_and_write_csv(address,proxies,f"{dir_name}/mnt_transactions_data.csv")
