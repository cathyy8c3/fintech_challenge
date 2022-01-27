import websocket
import json
import math
import statistics
import os
from httplib2 import Http
import datetime
from time import sleep
from coinbase.wallet.client import Client
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import psycopg2

# https://docs.pro.coinbase.com/

# CoinMarketCap API Key
key = "7c99e273-214a-46f5-8768-51ae9b51e58a"

conn = psycopg2.connect(
    database="tsdb",
    user="tsdbadmin",
    password="s076ypajb1f2sx6z",
    host="sjlvg6tey5.y7ed71zc7s.tsdb.cloud.timescale.com",
    port="39863"

)

conn.autocommit = True
cursor = conn.cursor()

class Stats:
    def __init__(self, name, slug, id):
        self.name = name.upper()
        self.slug = slug
        self.id = id
        self.client = Client('no_key', 'no_secret')
    def today(self):
        return datetime.date.today()
    def request_ticker(self):
        h = Http(".cache")
        rsp, cnt = h.request('https://api.pro.coinbase.com/products/' + self.name + '-USD/ticker', 'GET')
        cntx = json.loads(cnt)
        return cntx
    def request_stats(self):
        h = Http(".cache")
        rsp, cnt = h.request('https://api.pro.coinbase.com/products/' + self.name + '-USD/stats', 'GET')
        cntx = json.loads(cnt)
        return cntx
    def price(self, date='today'):
        if not date == 'today':
            return self.client.get_spot_price(currency_pair=self.name+'-USD', date=date)['amount']
        return self.request_ticker()['price']
    def volume(self, p30=False):
        if p30:
            return self.request_stats()['volume_30day']
        return self.request_ticker()['volume']
    def market_cap(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        parameters = {
          'id':self.id,
          # id should be assigned to name via slug/symbol?
          'aux':  "market_cap_by_total_supply"
        }
        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': key,
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        return data['data'][str(self.id)]['quote']['USD']['market_cap_by_total_supply']
    def percent_gain(self, tp=1):
        period = datetime.timedelta(days = tp)
        fetch_price = self.price(self.today() - period)
        return str((float(self.price())/float(fetch_price) -1)*100)+'%'
    def approval_status(self):
        return status

def get_slug_from_id(coin_id):
    return ('bicoin', '1', '1')

def post_to_db(coin_id):
    coin = Stats(*get_slug_from_id(coin_id))
    cursor.execute('''SET SESSION CHARACTERISTICS AS TRANSACTION READ WRITE''')
    cursor.execute('''INSERT INTO test_table(timestamp, coin_id, price, percentage_gain_1d, volume_1d, mkt_cap) VALUES('%s', '%s', '%s', '%s', '%s', '%s')'''%(str(datetime.datetime.now()), coin_id, 432423.23, 100.04, 23049823.2343, 230493))
    conn.commit()
    print("Pushed To Dataframe....................")
    conn.close()

post_to_db('1')
