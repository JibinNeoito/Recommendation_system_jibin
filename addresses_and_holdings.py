import requests
import json
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy import stats
import time
from requests import Request, Session

days = 30
#enter amount of past months to query

# accessToken = "BQYgFvJXE9xeSuB2zspmv4Cd8LW7WZCt"
accessToken = "BQYDBtrKMyQcLxfq0FtMDAzH2zxgeinh"
endpoint = 'https://graphql.bitquery.io'
headers = {"X-API-KEY": f"{accessToken}"}
#api endpoint and access

all_transactions = pd.DataFrame()
dates_list = pd.date_range(end = datetime.datetime.today(), periods = days)
    #creates date ranges to query


for i in dates_list:
    date_json = json.dumps(str(i.date()))
    query = f"""{{
      ethereum {{
        dexTrades(
          options: {{limit: 300, desc: "tradeAmount"}}
          date: {{is: {date_json}}}
          takerSmartContractType: {{is: None}}
        ) {{
          transaction {{
            hash
            txFrom {{
              address
            }}
          }}
          tradeAmount(in: USD)
          taker {{
            address
            }}
          }}
        }}
      }}"""
    #get queries for month range

    r = requests.post(endpoint, json={"query": query}, headers=headers)
    if r.status_code == 200:
        print(json.dumps(r.json(), indent=2))
    else:
        raise Exception(f"Query failed to run with a {r.status_code}.")
    transactions = pd.json_normalize(r.json()['data']['ethereum']['dexTrades'])

    all_transactions = all_transactions.append(transactions)

    time.sleep(0.05)

print(all_transactions)

unique_addresses = pd.unique(all_transactions['transaction.txFrom.address'])
print(len(unique_addresses))
#filter out duplicate addresses and convert to json format

splitedSize = 100
address_splits = [unique_addresses[x:x+splitedSize] for x in range(0, len(unique_addresses), splitedSize)]

all_holdings = pd.DataFrame()
for i in address_splits:
    addresses = json.dumps(list(i))

    query = f"""{{
      ethereum {{
        address(address: {{in:{addresses}}}) {{
          balances {{
            value
            currency {{
              name
              symbol
            }}
          }}
          address
        }}
      }}
        }}"""

    r = requests.post(endpoint, json={"query": query}, headers=headers)
    if r.status_code == 200:
        #         print(json.dumps(r.json(), indent=2))
        print(i.shape)
    else:
        raise Exception(f"Query failed to run with a {r.status_code}.")
    time.sleep(1)
    holdings = pd.json_normalize(r.json()['data']['ethereum']['address'], record_path=['balances'], meta=['address'])
    print(holdings)
    all_holdings = all_holdings.append(holdings)

# get currency balances for addresses

holdings_clean = all_holdings.loc[all_holdings['value']!=0.0, :].drop([0])

