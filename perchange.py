# Bittrex API class testing
# Updated to python 3.3 by Alexsei:
# 
#from urllib.parse import urlencode
#import certifi
#import pycurl
#from io import BytesIO
import json
import time
from datetime import datetime
from operator import itemgetter
from bittrex import bittrex

'''
   see https://bittrex.com/Home/Api
'''

"""
    PyCurl example
>>> import certifi
>>> import pycurl
>>> from io import BytesIO
>>> buffer = BytesIO()
>>> c = pycurl.Curl()
>>> c.setopt(pycurl.CAINFO, certifi.where())
>>> c.setopt(c.URL, 'https://bittrex.com/api/v1.1/public/getticker?market=BTC-ESC')
>>> c.setopt(c.WRITEDATA, buffer)
>>> c.perform()
>>> c.close
>>> buffer.getvalue()
"""

# perchg / percentagechange
# Used to return the percantage of change between two user specified values
def perchg(last, prevday):
    try:
        return (float(last)-float(prevday)) / float(prevday) * 100
    except:
        print('DEBUG::percentchange: float conversion error\nDEBUG::percentchange: last-{0} prevday-{1}'.format(last, prevday))
        return -99999.99

def listmarketsprice(testAPI):
    themMarkets = testAPI.get_markets() #this is a json element with dictionaries sorted (default from server data) by created by date

    ltcmarks = []
    btcmarks = []
                        
    for marks in themMarkets["result"]:
        if 'Litecoin' in marks["BaseCurrencyLong"]:
            ltcmarks.append(marks)
        if 'Bitcoin' in marks["BaseCurrencyLong"]:
            btcmarks.append(marks)

    #and then print table of the following:
    # Date Created - Base Currency - Market Currency - Is Sponsored - Is Active
    # single quote string (ex. 'x') does not process escape characters,
    # to use \t TAB and \n NEWLINE you need to use double quotes (ex. "test\nLineUp")
    # str.format() works on both types of strings '' & ""
    print ("\t{0}\t\t{1}\t{2}\t{3}\t{4}\t{5}".format('Created', 'BaseCurrency', 'MarketCurrency', 'IsSponsored', 'IsActive', 'LastPrice'))

    # debugging: show names of values in the processed market record
    #print(ltcmarks[0].keys())
    """
    dict_keys(['MinTradeSize', 'BaseCurrency', 'Created', 'BaseCurrencyLong', 'MarketCurrency', 'IsSponsored', 'Notice', 'IsActive', 'MarketName', 'MarketCurrencyLong', 'LogoUrl'])
    """

    for i,v in enumerate(ltcmarks):
        curPrice = testAPI.get_ticker(ltcmarks[i]['MarketName'])
        if not (curPrice["success"]):
            curPrice["result"] = {'Last': 'Unavailable'}
        print ("{0}\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}".format(str(ltcmarks[i]["Created"]), str(ltcmarks[i]["BaseCurrency"]), str(ltcmarks[i]["MarketCurrency"]), str(ltcmarks[i]["IsSponsored"]), str(ltcmarks[i]["IsActive"]), str(curPrice["result"]["Last"])))
    #### UPDATE here for python3.3 comptibility
    for i,v in enumerate(btcmarks):
        curPrice = testAPI.get_ticker(btcmarks[i]['MarketName'])
        if not (curPrice["success"]):
            curPrice["result"] = {'Last': 'Unavailable'}
        print ("{0}\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}".format(str(btcmarks[i]["Created"]), str(btcmarks[i]["BaseCurrency"]), str(btcmarks[i]["MarketCurrency"]),str(btcmarks[i]["IsSponsored"]), str(btcmarks[i]["IsActive"]), str(curPrice["result"]["Last"])))

    # cleanup our curl instance and other objects used
    testAPI.close_curl()
    del i, v, ltcmarks, btcmarks, marks, curPrice, themMarkets, self.testAPI

# NEW exercise:
# pull all the market changes and list the top 3 most +% and top 3 most -% and print to user-friendly output in irc (count=0 returns all markets)
def topmarkchange(testAPI, count=3):
    themMarkets = testAPI.get_markets()["result"]
    themMarkets.sort(key=itemgetter('BaseCurrencyLong'))
    for i, marks in enumerate(themMarkets):
        marksum = testAPI.get_market_summary(marks["MarketName"])["result"][0]
        if marksum["PrevDay"] is None:
            prevday = 0.00
        else:
            prevday = float(marksum["PrevDay"])

        if marksum["Last"] is None:
            last = 0.00
        else:
            last = marksum["Last"]
        try:   
            themMarkets[i]["DayChange"] = ( (last-prevday) / prevday  * 100)
        except:
            themMarkets[i]["DayChange"] = 0.00
            
    #    print('{!s}   \t\t{:+f}'.format(marks["MarketName"], marks["DayChange"]))
        #enumerate marks to print(count)
    #print('\n \n \n')
    themMarkets.sort(key=itemgetter('DayChange'),reverse=True)
    top = []
    bottom = []

    e = 0
    while e<count:
        top.append({"MarketName" : themMarkets[e]["MarketName"], "DayChange" : themMarkets[e]["DayChange"]})
    #    print('{!s}  \t{:+f}'.format(themMarkets[e]["MarketName"], themMarkets[e]["DayChange"]))
        e=e+1

    e = -1 # re-initialize counter and store bottom 3 %changes
    while e>-(count+1):
        bottom.append({"MarketName" : themMarkets[e]["MarketName"], "DayChange" : themMarkets[e]["DayChange"]})
    #    print('{!s}  \t{:+f}'.format(themMarkets[e]["MarketName"], themMarkets[e]["DayChange"]))
        e=e-1
    # to reverse order of lowest coin changes uncomment the following line
    #bottom.sort(key=itemgetter('DayChange'), reverse=True)

    # example irc output
    # Highest 3 Coin Changes: BTC-LION 240% // BTC-ESC 219% // BTC-ING 197%
    # Lowest 3 Coin Changes: BTC-MIN -120% // BTC-NANO -93% // BTC-EXS -53%
    tempstr = [
            str('Highest 3 Coin Changes (24h): {!s} {:+.2f}% // {!s} {:+.2f}% // {!s} {:+.2f}%'.format(top[0]["MarketName"],top[0]["DayChange"],top[1]["MarketName"],top[1]["DayChange"],top[2]["MarketName"],top[2]["DayChange"])),
            str('Lowest 3 Coin Changes (24h): {!s} {:+.2f}% // {!s} {:+.2f}% // {!s} {:+.2f}%'.format(bottom[0]["MarketName"],bottom[0]["DayChange"],bottom[1]["MarketName"],bottom[1]["DayChange"],bottom[2]["MarketName"],bottom[2]["DayChange"]))
            ]
    
    # cleanup objects before ending
    del bottom, top, e, marksum, marks, i, themMarkets

    return tempstr

# NEW exercise
# For a specified coin return baseVolume (usually BTC) & spotVolume (coin)
def getmarketvolume(testAPI,market):
    base = "BTC-"
    market = market.upper()
    result = testAPI.get_market_summary(str(base+market.upper()))["result"][0]
    volstr = "Bittrex: Volume in last 24h for {!s}: {:.8f}btc and {:.8f}{!s}".format(str(base+market),result["BaseVolume"], result["Volume"], market.lower())
    del base, result
    return [volstr]

# NEW exercise:
# For a specified coin, return latest (non-cache) ticker
def getmarketticker(testAPI,market):
    base = "BTC-"
    market = market.upper()
    result = testAPI.get_ticker(str(base+market.upper()))["result"]
    tickerstr = "{!s}:: Bittrex - Bid: {:.8f}  Ask: {:.8f}  Last: {:.8f}".format(str(base+market), result["Bid"], result["Ask"], result["Last"])
    del base, result
    return [tickerstr]

# create a bittrex instance for accessing the API
testAPI = bittrex('doestmatteritispublic')

#listmarketsprice(testAPI)
#topmarkchange(testAPI)