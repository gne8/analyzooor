import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
address_list = [
    os.getenv("ADDRESS_1"),
    os.getenv("ADDRESS_2"),
    os.getenv("ADDRESS_3"),
    os.getenv("ADDRESS_4"),
    os.getenv("ADDRESS_5")
]

def basic_stats_extractor(df):
    df['datetime'] = pd.to_datetime(df['datetime'])
    max_datetime = df['datetime'].max()
    min_datetime = df['datetime'].min()
    df['date'] = df['datetime'].dt.date
    total_unique_days = df['date'].nunique()
    total_transactions_count = df['hash'].nunique()
    df['month_year'] = df['datetime'].dt.to_period('M')
    total_unique_month_years = df['month_year'].nunique()

    return pd.DataFrame({
        'max_datetime': [max_datetime],
        'min_datetime': [min_datetime],
        'total_transactions_count': [total_transactions_count],
        'total_unique_days': [total_unique_days],
        'total_unique_month_years': [total_unique_month_years]
    })

def date_active_stats_extractor(df):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = df['datetime'].dt.date
    unique_hash_counts = df.groupby('date')['hash'].nunique()

    #Convert the Series to a DataFrame
    df_unique_hash_counts = unique_hash_counts.reset_index()

    #Rename the columns
    df_unique_hash_counts.columns = ['date', 'count']

    #Save the DataFrame as a CSV file
    return df_unique_hash_counts

for address in address_list:
    dir_name = f'data/{address}'
    df = basic_stats_extractor(pd.read_csv(f'{dir_name}/mnt_transactions_data.csv'))
    df.to_csv(f'{dir_name}/mnt_basic_stats.csv', index=False)

    df = date_active_stats_extractor(pd.read_csv(f'{dir_name}/mnt_transactions_data.csv')) 
    df.to_csv(f'{dir_name}/mnt_date_count_txn.csv', index=False)