import requests
import pandas as pd
import ast
import json

class Debank:

    def __init__(self, address):
        self.headers = {}
        self.address = address
        self.urls = {
            'token'     : f'https://api.debank.com/token/cache_balance_list?user_addr={self.address}',
            'protocol'  : f'https://api.debank.com/portfolio/project_list?user_addr={self.address}',
        }
        self.api_result = {
            'token'     : '',
            'protocol'  : '',
        }

    def get_debank(self, type_, proxies=''):
        if proxies == '':
           resp = requests.get(self.urls[type_],headers=self.headers)
        else:
            resp = requests.get(self.urls[type_], proxies=proxies,headers=self.headers)
        if resp.status_code == 200:
            resp_json = resp.json()
            self.api_result[type_] = resp_json['data']
        else:
            print(f"Error API: {resp.status_code}")

    def convert_dataframe(self, type_):
        if type_ == 'Token':
            df = pd.DataFrame(columns=['amount', 'price', 'optimized_symbol'])
            for i in self.api_result[type_]:
                df= df.append({'amount': i['amount'], 'price': i['price'], 'optimized_symbol': i['optimized_symbol']})
        return df
    
