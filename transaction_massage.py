import pandas as pd

df = pd.read_csv('data/test_transaction_data.csv')
df['datetime'] = pd.to_datetime(df['datetime'])
max_datetime = df['datetime'].max()
min_datetime = df['datetime'].min()
df['date'] = df['datetime'].dt.date
total_unique_days = df['date'].nunique()
total_transactions_count = df['hash'].nunique()
df['month_year'] = df['datetime'].dt.to_period('M')
total_unique_month_years = df['month_year'].nunique()

new_df = pd.DataFrame({
    'max_datetime': [max_datetime],
    'min_datetime': [min_datetime],
    'total_transactions_count': [total_transactions_count],
    'total_unique_days': [total_unique_days],
    'total_unique_month_years': [total_unique_month_years]
})

new_df.to_csv('data/test_basic_stats.csv', index=False)

# df['date'] = df['datetime'].dt.date
# unique_hash_counts = df.groupby('date')['hash'].nunique()

# Convert the Series to a DataFrame
# df_unique_hash_counts = unique_hash_counts.reset_index()

# Rename the columns
# df_unique_hash_counts.columns = ['date', 'count']

# Save the DataFrame as a CSV file
# df_unique_hash_counts.to_csv('data/test_date_count_txn.csv', index=False)
