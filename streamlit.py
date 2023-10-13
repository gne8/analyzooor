import streamlit as st
import pandas as pd
import ast
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

columns = [
    'amount', 'chain', 'credit_score', 'decimals', 'display_symbol', 'id',
    'is_core', 'is_verified', 'is_wallet', 'logo_url', 'name', 'optimized_symbol',
    'price', 'price_24h_change', 'protocol_id', 'raw_amount', 'raw_amount_hex_str',
    'raw_amount_str', 'symbol', 'time_at'
]

empty_df = pd.DataFrame(columns=columns)

st.set_page_config(layout="wide")
# st.sidebar.image('analyzooor_logo.png', caption='Pepe will analyze your fate', use_column_width=True)
col1, col2, col3 = st.columns(3)

col1.image('analyzooor_logo.png', width=250, use_column_width=False)
col2.title('Analyzooor')
col2.markdown('*The analytics platform for meme lords*')

if st.button('Connect Wallet'):
    st.write('Wallet Connected!')

with st.container():
    token_address = st.text_input('Insert Token Address', key='token_address')
    if st.button('Go'):
        st.write('Token Address:', token_address)

        try:
            with open('data/test_token_data.csv', 'r') as file:
                lines = file.readlines()
            data_list = []

            for line in lines:
                try:
                    data_dict = ast.literal_eval(line)
                    data_list.append(data_dict)
                except (SyntaxError, ValueError) as e:
                    st.write(f"Error decoding line: {line}")
                    st.write(f"Error: {e}")

            data_list = [ast.literal_eval(entry) for entry in data_list]

            df = pd.DataFrame(data_list)
            # st.dataframe(df) # to comment out 

# Portfolio Value 
            df['total_value'] = df['amount'] * df['price']
            total_amount = df['total_value'].sum()
            st.title(f'Portfolio Value: ${total_amount:,.2f}') 
            if total_amount > 1000: 
                st.write("🐋 OH WOW WHALE ALERT, WANNA DONATE SOME?")
            else:
                st.write("🤡 YOUR PORT IS LOW BRO, DID YOU DEGEN TOO MUCH?")

# Token Distribution pie chart
            selected_columns = ['optimized_symbol', 'amount']
            selected_df = df[selected_columns]
            grouped_df = selected_df.groupby('optimized_symbol').sum().reset_index()
            st.subheader("Token Distribution")
            fig = px.pie(grouped_df, values='amount', names='optimized_symbol')
            st.plotly_chart(fig, use_container_width=True)

# Digital footprint
            df = pd.read_csv('data/test_date_count_txn.csv')
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df['week'] = df.index.to_period('W').strftime('%U').astype(int)            
            df['dayofweek'] = df.index.strftime('%a') 
            days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            df['dayofweek'] = pd.Categorical(df['dayofweek'], categories=days_order, ordered=True)            

            weeks_order = sorted(df['week'].unique())
            df['week'] = pd.Categorical(df['week'], categories=weeks_order, ordered=True)

            daily_activity = df.groupby(['week', 'dayofweek']).sum()
            heatmap_data = daily_activity.pivot_table(values='count', index='dayofweek', columns='week')
            heatmap_data = heatmap_data.reindex(columns=np.roll(heatmap_data.columns, shift=1))

            st.subheader("Digital Footprint on Mantle")
            fig, ax = plt.subplots(figsize=(7, 3))
            sns.heatmap(heatmap_data, cmap='Greens', annot=True, fmt='g', cbar=False, linewidths=0.5, ax=ax)
            ax.set_xlabel('Week of Year')
            ax.set_ylabel('Day of Week')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)  
            st.pyplot(fig, use_container_width=True)

# When it fails
        except FileNotFoundError:
            st.write("File not found.")
