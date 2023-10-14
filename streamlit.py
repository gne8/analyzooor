import streamlit as st
import pandas as pd
import ast
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random

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
tabs = st.selectbox("Choose a mode:", ["Lonely Pepe Mode", "Pepe vs Friends Mode", "Honorary Pepe-board"])

if tabs == "Lonely Pepe Mode":
    if st.button('Connect Wallet'):
        st.write('Wallet Connected!')

    st.title("Lonely Pepe Mode")
    with st.container():
        token_address = st.text_input('Insert Token Address', key='token_address')
        if st.button('Summon the Pepe Analyst'):
            st.markdown(f'Ahh yes, **{token_address}**')

            # Construct the file path based on token_address
            token_data_path = os.path.join('data', token_address)
            file_path = os.path.join(token_data_path, 'mnt_debank_token_data.csv')
            basic_stats_file = os.path.join(token_data_path, 'mnt_basic_stats.csv')
            date_count_txn = os.path.join(token_data_path, 'mnt_date_count_txn.csv')
            # file_path = os.path.join('data', token_address, 'mnt_debank_token_data.csv')

            try:
                with open(file_path, 'r') as file:
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
                # st.dataframe(df)  # to comment out

                # Portfolio Value
                df['total_value'] = df['amount'] * df['price']
                total_amount = df['total_value'].sum()
                st.title(f'Portfolio Value: ${total_amount:,.2f}')

                tweet_text_whale = "🐋 WOW WOW WHALE ALERT, OTHER PEOPLE'S NETWORTH IS BASICALLY GAS MONEY. COME JOIN ME ON @0xMantle"
                tweet_text_low_port = "🤡 PORTFOLIO IS DOWN BAD, PROBABLY DEGEN TOO MUCH? MAYBE JOIN ME TO DEGEN ON @0xMantle"

                if total_amount > 50:
                    st.markdown(
                        f"""
                        <div style='background-color: #add8e6; padding: 10px; border-radius: 5px;'>
                            <p style='font-weight: bold; color: black;'>{tweet_text_whale}</p>
                            <a href='https://twitter.com/intent/tweet?text={tweet_text_whale}' target='_blank'>
                                Share on Twitter
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div style='background-color: #add8e6; padding: 10px; border-radius: 5px;'>
                            <p style='font-weight: bold; color: black;'>{tweet_text_low_port}</p>
                            <a href='https://twitter.com/intent/tweet?text={tweet_text_low_port}' target='_blank'>
                                Share on Twitter
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Additional Stats
                stats = pd.read_csv(basic_stats_file)
                # stats = pd.read_csv('data/test_basic_stats.csv')
                max_datetime = stats['max_datetime'].values[0]
                min_datetime = stats['min_datetime'].values[0]
                total_transactions_count = stats['total_transactions_count'].values[0]
                total_unique_days = stats['total_unique_days'].values[0]
                total_unique_month_years = stats['total_unique_month_years'].values[0]
                st.markdown(
                    f'''
                    <div style="background-color:#98FB98;padding:20px;border-radius:10px;">
                        You last wasted your money on {max_datetime}.
                        You decided to embark on the journey to lose money on {min_datetime}.
                        You have made {total_transactions_count} transactions, with {total_unique_days} active days, and {total_unique_month_years} active months.
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

                col1, col2 = st.columns(2)
                # Token Distribution pie chart
                with col1:
                    selected_columns = ['optimized_symbol', 'amount']
                    selected_df = df[selected_columns]
                    grouped_df = selected_df.groupby('optimized_symbol').sum().reset_index()
                    st.subheader("Token Distribution")
                    fig = px.pie(grouped_df, values='amount', names='optimized_symbol')
                    st.plotly_chart(fig, use_container_width=True)

                # Digital footprint
                with col2:
                    df = pd.read_csv(date_count_txn)                
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

                image_choices = ['lonely_ape.jpg', 'lonely_clown.jpg', 'lonely_fool.jpg']
                random_image = random.choice(image_choices)
                st.title("The Wizard Pepe has granted you the title of:")
                st.image(random_image, width=500)                                    

            except FileNotFoundError:
                st.write("File not found.")

elif tabs == 'Pepe vs Friends Mode':
    if st.button('Connect Wallet'):
        st.write('Wallet Connected!')

    st.title("Pepe vs Friends Mode")    
    with st.container():
        token_address = st.text_input('Insert Token Address', key='token_address')
        opponent_address = st.text_input('Insert Opponent Address', key='opponent_address')        

        if st.button('Duel'):
            st.markdown(
                f"""
                <div style='background-color: #FFD3D3; padding: 10px; border-radius: 5px;'>
                    <p style='font-weight: bold; color: darkred;'>Ahh yes, the duel between <span style='color: darkred;'>{token_address}</span> and <span style='color: darkred;'>{opponent_address}</span> shall begin!</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            token_data_path = os.path.join('data', token_address)
            file_path = os.path.join(token_data_path, 'mnt_debank_token_data.csv')
            opponent_data_path = os.path.join('data', opponent_address)
            file_path2 = os.path.join(opponent_data_path, 'mnt_debank_token_data.csv')

            total_amount = 0
            total_amount2 = 0

            try:
                with open(file_path, 'r') as file:
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

                # Portfolio Value
                df['total_value'] = df['amount'] * df['price']
                total_amount = df['total_value'].sum()

            except FileNotFoundError:
                st.write(f"File not found: {file_path}")

            # Process file_path2
            try:
                with open(file_path2, 'r') as file:
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

                df2 = pd.DataFrame(data_list)

                # Portfolio Value
                df2['total_value'] = df2['amount'] * df2['price']
                total_amount2 = df2['total_value'].sum()

            except FileNotFoundError:
                st.write(f"File not found: {file_path2}")

            if total_amount > total_amount2:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(
                        f"""
                        <div style='background-color: #FFFF99; padding: 0px; border-radius: 0px;'>
                            <p style='font-weight: bold; color: black;'>{token_address} Portfolio Value: ${total_amount:,.2f}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )                    
                    # st.write(f'{token_address} Portfolio Value: ${total_amount:,.2f}')
                    st.image('goodlife.png', width = 360, caption='Living the good life')

                with col2:
                    st.image('vs_logo.png', width=380)                    

                with col3:
                    st.markdown(
                        f"""
                        <div style='background-color: #FFFF99; padding: 0px; border-radius: 0px;'>
                            <p style='font-weight: bold; color: black;'>{opponent_address} Portfolio Value: ${total_amount2:,.2f}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )                    
                    # st.write(f'{opponent_address} Portfolio Value: ${total_amount2:,.2f}')
                    st.image('downbad.png', width = 360, caption='Down bad')
            else:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(
                        f"""
                        <div style='background-color: #FFFF99; padding: 0px; border-radius: 0px;'>
                            <p style='font-weight: bold; color: black;'>{token_address} Portfolio Value: ${total_amount:,.2f}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )                       
                    # st.write(f'{token_address} Portfolio Value: ${total_amount:,.2f}')
                    st.image('downbad.png', width = 360, caption='Down bad')

                with col2:
                    st.image('vs_logo.png', width=380)

                with col3:
                    st.markdown(
                        f"""
                        <div style='background-color: #FFFF99; padding: 0px; border-radius: 0px;'>
                            <p style='font-weight: bold; color: black;'>{opponent_address} Portfolio Value: ${total_amount2:,.2f}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )                       
                    # st.write(f'{opponent_address} Portfolio Value: ${total_amount2:,.2f}')
                    st.image('goodlife.png', width = 360, caption='Living the good life')
else:
    st.title("Honorary Pepe-Board")
    gas_spending = pd.read_csv('data/leaderboard/clean_gas_spent_leaderboard.csv')
    txn_count = pd.read_csv('data/leaderboard/clean_txn_count_leaderboard.csv')

# Search
    token_address = st.text_input('Enter Token Address:')
    token_address = token_address.strip().lower()  
    search_button = st.button('Search')

    if search_button:
        filtered_gas_spending = gas_spending[gas_spending['tx_sender'].str.lower() == token_address]
        filtered_txn_count = txn_count[txn_count['tx_sender'].str.lower() == token_address]

        if not filtered_gas_spending.empty:
            index_gas_spending = filtered_gas_spending.index[0]
            st.write(f"You are ranked {index_gas_spending + 1} in the gas spending leaderboard for @0xMantle.")
            gas_spending_tweet = f"I am ranked {index_gas_spending + 1} in the gas spending leaderboard for @0xMantle."
        else:
            st.write("You are not in the gas spending leaderboard for @0xMantle.")
            gas_spending_tweet = "I am not on the gas spending leaderboard for @0xMantle."

        if not filtered_txn_count.empty:
            index_txn_count = filtered_txn_count.index[0]
            st.write(f"You are ranked {index_txn_count + 1} in the transaction count leaderboard for @0xMantle.")
            txn_count_tweet = f"I am ranked {index_txn_count + 1} in the transaction count leaderboard for @0xMantle."
        else:
            st.write("You are not in the transaction count leaderboard for @0xMantle.")
            txn_count_tweet = "I am not on the transaction count leaderboard for @0xMantle."

        if filtered_txn_count.empty and filtered_gas_spending.empty:
            st.image('ngmi.jpg', width = 200)
        else:
            st.image('leader.jpg', width = 200)    

        tweet_text = gas_spending_tweet if not filtered_gas_spending.empty else txn_count_tweet
        tweet_url = f"https://twitter.com/intent/tweet?text={tweet_text}"

        # Custom HTML div for Twitter share
        st.markdown(
            f"""
            <div style='background-color: #add8e6; padding: 10px; border-radius: 5px;'>
                <p style='font-weight: bold; color: black;'></p>
                <a href='{tweet_url}' target='_blank'>
                    Share on Twitter
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )                  

# Leaderboard
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Gas Spending")
        st.dataframe(gas_spending.head(10))

    with col2:
        st.subheader("Top 10 Transaction Count")
        st.dataframe(txn_count.head(10))