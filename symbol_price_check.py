# importing libraries
from crypto_to_USD import latest_price
import pandas as pd
import numpy as np
import coinmarketcapapi

# function to get unique values
def unique(data_list):
    x = np.array(data_list)
    unique_list = np.unique(x).tolist()
    return(unique_list)

# Loading csv file
data = pd.read_csv("holdings_clean.csv")
symbol_list = data['currency.symbol'].tolist()
symbol_unique = unique(symbol_list)

# cleaning the symbols(removing unwanted spaces)
symbol_unique_updated = [i.split()[0] for i in symbol_unique]

# Fetching all active cryptocurrencies
cmc_api_key = "provide your coinmarketcap api key here" # CoinMarketCap API key
cmc = coinmarketcapapi.CoinMarketCapAPI(cmc_api_key)
data_id_map = cmc.cryptocurrency_map()
cmc_df = pd.DataFrame(data_id_map.data, columns =['id','name','symbol']) #active crptocurrency data frame

cmc_symbols = cmc_df['symbol'].tolist()
cmc_id = cmc_df['id'].tolist()

# matching the common crypto symbols
crypto_in_cmc = list(set(cmc_symbols) & set(symbol_unique_updated))

# break points setting up for including maximum number of crypto symbols
break_points = list(range(0,len(crypto_in_cmc),1100))
break_points.append(len(crypto_in_cmc))

# batch wise price fetching for avoiding "414 Request-URI Too Large" error
full_price_list = []
full_key_list = []
for i in range(0,len(break_points)-1):
    print(break_points[i])
    print("##############")
    print(break_points[i + 1])
    # preparing input to the latest price fetching function
    joined_string = [",".join(crypto_in_cmc[break_points[i]:break_points[i + 1]])]
    price_dict = latest_price(joined_string, cmc_api_key)
    print(price_dict)
    full_price_list.append(price_dict['currency_price'])
    full_key_list.append(price_dict['currency_symbol'])

    if i == (len(break_points)-1):
        print(break_points[i])
        print("##############")
        print(break_points[i+1])
        joined_string = [",".join(crypto_in_cmc[break_points[i]:break_points[i + 1]])]
        price_dict = latest_price(joined_string, cmc_api_key)
        full_price_list.append(price_dict['currency_price'])
        full_key_list.append(price_dict['currency_symbol'])

