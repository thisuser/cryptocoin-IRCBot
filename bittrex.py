#! /usr/bin/env python
# updated for Python3.3 and newer
# added get_market_summary(market) to public methods (was not in API example)

from urllib.parse import urlencode
import certifi
import pycurl
from io import BytesIO
import json
import time
from datetime import datetime

BUY_ORDERBOOK = 'buy'
SELL_ORDERBOOK = 'sell'
BOTH_ORDERBOOK = 'both'
'''
   see https://bittrex.com/Home/Api
'''
class bittrex(object):
    def __init__(self, APIKey):
        self.APIKey = APIKey
        self.public_set = set(['getmarkets','getcurrencies','getticker','getmarketsummaries', 'getmarketsummary','getorderbook','getmarkethistory'])
        self.market_set = set(['getopenorders','cancel','sellmarket','selllimit','buymarket','buylimit'])
        self.account_set = set(['getbalances','getbalance','getdepositaddress','withdraw'])
        self.c = pycurl.Curl()
        
    def close_curl(self):
        self.c.close()
        del self.c

    def api_query(self, method, req={}):
        buffer = BytesIO()
        self.c.setopt(pycurl.CAINFO, certifi.where())
        if method in self.public_set:
            request_url = 'https://bittrex.com/api/v1.1/public/' + method + '?'
        elif method in self.market_set:
            request_url = 'https://bittrex.com/api/v1.1/market/' + method + '?'
        elif method in self.account_set:
            request_url = 'https://bittrex.com/api/v1.1/account/' + method + '?'
        
        request_url += urlencode(req)
            
        if method not in self.public_set:
            request_url += '&apikey=' + self.APIKey


        self.c.setopt(self.c.URL, request_url)
        self.c.setopt(self.c.WRITEDATA, buffer)
        self.c.perform()

        temp = json.loads(buffer.getvalue().decode('utf-8'))
        if not temp["success"]:
            print("ERRROR: API request unsuccessful - {0}".format(str(temp["message"])))
            return temp
        else:
            return temp

    
    #get_markets Used to get the open and available trading markets at Bittrex along with other meta data.
    #Parameters
    #None
    def get_markets(self):
        return self.api_query('getmarkets')
    
    #get_currencies Used to get all supported currencies at Bittrex along with other meta data.
    #Parameters
    #None
    def get_currencies(self):
        return self.api_query('getcurrencies')
    
    #get_ticker Used to get the current tick values for a market.
    #Parameters
    #parameter    required    description
    #market    required    a string literal for the market (ex: BTC-LTC)
    def get_ticker(self, market):
        return self.api_query('getticker', {'market': market})
    
    #get_market_summaries  Used to get the last 24 hour summary of all active exchanges
    #Parameters
    #None
    def get_market_summaries(self):
        return self.api_query('getmarketsummaries')

    #get_market_summary Used to get the last 24 hour summary for a given market
    #Parameters
    #parameter  required    description
    #market     required    a string leteral for the market (ex: BTC-LION)
    def get_market_summary(self, market):
        return self.api_query('getmarketsummary', {'market': market})
    
    #Used to get retrieve the orderbook for a given market
    #Parameters
    #parameter    required    description
    #market    required    a string literal for the market (ex: BTC-LTC)
    #type    required    buy, sell or both to identify the type of orderbook to return.  Use constants BUY_ORDERBOOK, SELL_ORDERBOOK, BOTH_ORDERBOOK
    #depth    optional    defaults to 20 - how deep of an order book to retrieve. Max is 100
    def get_orderbook(self, market, depth_type, depth=20):
        return self.api_query('getorderbook', {'market': market, 'type': depth_type, 'depth': depth})
    
    #/market/getmarkethistory
    #Used to retrieve the latest trades that have occured for a specific market.
    #
    #Parameters
    #parameter    required    description
    #market    required    a string literal for the market (ex: BTC-LTC)
    #count    optional    a number between 1-100 for the number of entries to return (default = 20)
    def get_market_history(self, market, count):
        return self.api_query('getmarkethistory', {'market': market, 'count': count})
        
    #/market/buymarket
    #Used to place a buy order in a specific market. Use buymarket to place market orders. Make sure you have the proper permissions set on your API keys for this call to work
    #
    #Parameters
    #parameter    required    description
    #market    required    a string literal for the market (ex: BTC-LTC)
    #quantity    required    the amount to purchase
    #rate    required    the rate at which to place the order. this is not needed for market orders
    def buy_market(self, market, quantity, rate):
        return self.api_query('buymarket', {'market': market, 'quantity': quantity, 'rate': rate})
    
    #/market/buylimit
    #Used to place a buy order in a specific market. Use buylimit to place limit orders Make sure you have the proper permissions set on your API keys for this call to work
    #
    #Parameters
    #parameter    required    description
    #market    required    a string literal for the market (ex: BTC-LTC)
    #quantity    required    the amount to purchase
    #rate    required    the rate at which to place the order. this is not needed for market orders
    def buy_limit(self, market, quantity, rate):
        return self.api_query('buylimit', {'market': market, 'quantity': quantity, 'rate': rate})
    
    #/market/sellmarket
    #Used to place a sell order in a specific market. Use sellmarket to place market orders. Make sure you have the proper permissions set on your API keys for this call to work
    #
    #Parameters
    #parameter    required    description
    #market    required    a string literal for the market (ex: BTC-LTC)
    #quantity    required    the amount to purchase
    #rate    required    the rate at which to place the order. this is not needed for market orders
    def sell_market(self, market, quantity, rate):
        return self.api_query('sellmarket', {'market': market, 'quantity': quantity, 'rate': rate})
    
    #/market/selllimit
    #Used to place a sell order in a specific market. Use selllimit to place limit orders Make sure you have the proper permissions set on your API keys for this call to work
    #
    #Parameters
    #parameter    required    description
    #market    required    a string literal for the market (ex: BTC-LTC)
    #quantity    required    the amount to purchase
    #rate    required    the rate at which to place the order. this is not needed for market orders
    def sell_limit(self, market, quantity, rate):
        return self.api_query('selllimit', {'market': market, 'quantity': quantity, 'rate': rate})
    
    #/market/cancel
    #Used to cancel a buy or sell order.
    #
    #Parameters
    #parameter    required    description
    #uuid    required    uuid of buy or sell order
    def cancel(self, uuid):
        return self.api_query('cancel', {'uuid': uuid})
    
    #/market/getopenorders
    #Get all orders that you currently have opened. A specific market can be requested
    #
    #Parameters
    #parameter    required    description
    #market    optional    a string literal for the market (ie. BTC-LTC)
    def get_open_orders(self, market):
        return self.api_query('getopenorders', {'market': market})

    #/account/getbalances
    #Used to retrieve all balances from your
    #
    #Parameters
    #None
    def get_balances(self):
        return self.api_query('getbalances', {})
    
    #/account/getbalance
    #Used to retrieve the balance from your account for a specific currency.
    #
    #Parameters
    #parameter    required    description
    #currency    required    a string literal for the currency (ex: LTC)
    def get_balance(self, currency):
        return self.api_query('getbalance', {'currency': currency})
    
    #/account/getdepositaddress
    #Used to generate or retrieve an address for a specific currency.
    #
    #Parameters
    #parameter    required    description
    #currency    required    a string literal for the currency (ie. BTC)
    def get_deposit_address(self, currency):
        return self.api_query('getdepositaddress', {'currency': currency})

    #/account/withdraw
    #Used to withdraw funds from your account.
    #
    #Parameters public ApiHelper.DefaultResponse Withdraw(string apiKey = null, string currency = null, decimal quantity = 0, string address = null)
    #parameter    required    description
    #currency    required    a string literal for the currency (ie. BTC)
    #quantity    required    the quantity of coins to withdraw
    #address    required    the address where to send the funds.
    def withdraw(self, currency, quantity, address):
        return self.api_query('withdraw', {'currency': currency, 'quantity':quantity, 'address':address})
