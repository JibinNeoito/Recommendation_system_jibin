import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# Function get the latest price of cryptocurrency
def latest_price(crypto_symbol_list, API_KEY):
    # CoinMarketCap latest Cryptocurrency price update api
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    # parameters to passed to fetch bitcoin latest price
    parameters = {
        'symbol': crypto_symbol_list,
        'convert': 'USD'
    }

    # CoinMarketCap API credentials
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    # for repeatedly to fetch data w.r.to parameters
    session = Session()
    session.headers.update(headers)

    # fetching response from the API
    try:
        response = session.get(url, params=parameters)
        jsn = json.loads(response.text)

        # handling api errors
        currency_status = json.loads(response.text)['status']['error_code']

        if currency_status == 0:
            # Extracting price from the fetched data
            key_list = list(json.loads(response.text)['data'].keys())
            price_list = []
            for key in key_list:
                price = json.loads(response.text)['data'][key]['quote']['USD']['price']
                price_list.append(price)

            currency_price_dict = {}
            currency_price_dict["currency_symbol"] = key_list
            currency_price_dict["currency_price"] = price_list

            return(currency_price_dict)
        else:
            # this command shows the errors if any
            error_message =  json.loads(response.text)['status']['error_message']
            return (error_message)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)