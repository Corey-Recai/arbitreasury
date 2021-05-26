import pymongo
from pymongo import MongoClient
from pprint import pprint
import datetime

client = MongoClient("mongodb://localhost:27017/", connect=True)
db = client['cryptodb']
def insertBTCETHSignal(btc_usdLastPrice, eth_usdLastPrice, eth_btcLastPrice, eth_btcImpliedPrice, eth_btcProfitMargin, eth_btcProfitMarginPercent, isTradable, initalInvestment, Profit):
    
    collection = db['btc_ethSignal']

    new_record = {
        'Timestamp': datetime.datetime.now(),
        'btc_usdLastPrice': btc_usdLastPrice,
        'eth_usdLastPrice': eth_usdLastPrice,
        'eth_btcLastPrice': eth_btcLastPrice,
        'eth_btcImpliedPrice': eth_btcImpliedPrice,   
        'eth_btcProfitMargin': eth_btcProfitMargin,  
        'eth_btcProfitMarginPercent': eth_btcProfitMarginPercent,
        'isTradable': isTradable, 
        'intialInvestment': initalInvestment,
        'Profit': Profit,
        }

    collection.insert_one(new_record)

def insertBTCLTCSignal(btc_usdLastPrice, ltc_usdLastPrice, ltc_btcLastPrice, ltc_btcImpliedPrice, ltc_btcProfitMargin, ltc_btcProfitMarginPercent, isTradable, initalInvestment, Profit):
    
    collection = db['btc_ltcSignal']

    new_record = {
        'Timestamp': datetime.datetime.now(),
        'btc_usdLastPrice': btc_usdLastPrice,
        'ltc_usdLastPrice': ltc_usdLastPrice,
        'ltc_btcLastPrice': ltc_btcLastPrice,
        'ltc_btcImpliedPrice': ltc_btcImpliedPrice,   
        'ltc_btcProfitMargin': ltc_btcProfitMargin,  
        'ltc_btcProfitMarginPercent': ltc_btcProfitMarginPercent,
        'isTradable': isTradable, 
        'intialInvestment': initalInvestment,
        'Profit': Profit,
        }

    collection.insert_one(new_record)

def insertBTCXRPSignal(btc_usdLastPrice, ltc_usdLastPrice, ltc_btcLastPrice, ltc_btcImpliedPrice, ltc_btcProfitMargin, ltc_btcProfitMarginPercent, isTradable, initalInvestment, Profit):
    db = client['cryptodb']
    collection = db['btc_xrpSignal']

    new_record = {
        'Timestamp': datetime.datetime.now(),
        'btc_usdLastPrice': btc_usdLastPrice,
        'ltc_usdLastPrice': ltc_usdLastPrice,
        'ltc_btcLastPrice': ltc_btcLastPrice,
        'ltc_btcImpliedPrice': ltc_btcImpliedPrice,   
        'ltc_btcProfitMargin': ltc_btcProfitMargin,  
        'ltc_btcProfitMarginPercent': ltc_btcProfitMarginPercent,
        'isTradable': isTradable, 
        'intialInvestment': initalInvestment,
        'Profit': Profit,
        }

    collection.insert_one(new_record)

def insertBTCETCSignal(btc_usdLastPrice, etc_usdLastPrice, etc_btcLastPrice, etc_btcImpliedPrice, etc_btcProfitMargin, etc_btcProfitMarginPercent, isTradable, initalInvestment, Profit):
    
    collection = db['btc_etcSignal']

    new_record = {
        'Timestamp': datetime.datetime.now(),
        'btc_usdLastPrice': btc_usdLastPrice,
        'etc_usdLastPrice': etc_usdLastPrice,
        'etc_btcLastPrice': etc_btcLastPrice,
        'etc_btcImpliedPrice': etc_btcImpliedPrice,   
        'etc_btcProfitMargin': etc_btcProfitMargin,  
        'etc_btcProfitMarginPercent': etc_btcProfitMarginPercent,
        'isTradable': isTradable, 
        'intialInvestment': initalInvestment,
        'Profit': Profit,
        }

    collection.insert_one(new_record)