## Cryptocurrency Recommendation System

### Objective
Recommend cryptocurrencies to the user

### Installing Libraries

Environment : _Ubuntu 20.10 and Python 3.8_

All python libraries used are listed in `requirements.txt`. For installing all required libraries, run the following commands in terminal

`pip3 install -r requirements.txt`

### How to run ?

Run the Python file `symbol_price_check.py` is for fetching the price details for the cryptocurrencies provided ith GraphQL API. Input file used is `holdings_clean.csv` and provide the API key for CoinMarketCap

The python file `crypto_to_USD.py` is the function used in `symbol_price_check.py` for fetching the price for cryptocurrency. It expects the input as `crypto_symbol_list`(list of cryptocurrency symbols) and `API_KEY`(API key for CoinMarketCap) 

