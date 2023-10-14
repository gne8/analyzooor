select 
    tx_sender, 
    total_txn_gas_spent
from(
  select 
    hex(tx_sender) as tx_sender, 
    SUM(tx_gas_spent) as total_txn_gas_spent, 
    SUM(fees_paid) as total_fees_paid,
    count(distinct tx_hash) as txn_count, 
    min(signed_at) as first_txn_date, 
    max(signed_at) as last_txn_date
  from blockchains.all_chains
  where chain_name = 'mantle_mainnet'
  and successful = 1
  group by 1
)
order by 2 desc
limit 1000