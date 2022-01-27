'''
Generating PoW and PoS Coins
'''

import requests
from bs4 import BeautifulSoup

url_pos = 'https://coinmarketcap.com/view/pos/'
r_pos = requests.get(url_pos)

soup_pos = BeautifulSoup(r_pos.content, 'html5lib')

# list of PoS coins
pos = []

table_1 = soup_pos.findAll('p', attrs = {'color': 'text3', 'class': 'sc-1eb5slv-0 gGIpIK coin-item-symbol', 'font-size': '1'})
table_2 = soup_pos.findAll('span', attrs = {'class': 'crypto-symbol'})

for row in table_1:
    pos.append(row.text)
for row in table_2:
    pos.append(row.text)

url_pow_1 = 'https://coinmarketcap.com/view/pow/'
url_pow_2 = 'https://coinmarketcap.com/view/pow/?page=2'
r_pow_1 = requests.get(url_pow_1)
r_pow_2 = requests.get(url_pow_2)

soup_pow_1 = BeautifulSoup(r_pow_1.content, 'html5lib')
soup_pow_2 = BeautifulSoup(r_pow_2.content, 'html5lib')

# list of PoW coins
pow = []

table_1 = soup_pow_1.findAll('p', attrs = {'color': 'text3', 'class': 'sc-1eb5slv-0 gGIpIK coin-item-symbol', 'font-size': '1'})
table_2 = soup_pow_1.findAll('span', attrs = {'class': 'crypto-symbol'})

for row in table_1:
    pow.append(row.text)
for row in table_2:
    pow.append(row.text)

table_1 = soup_pow_2.findAll('p', attrs = {'color': 'text3', 'class': 'sc-1eb5slv-0 gGIpIK coin-item-symbol', 'font-size': '1'})
table_2 = soup_pow_2.findAll('span', attrs = {'class': 'crypto-symbol'})

for row in table_1:
    pow.append(row.text)
for row in table_2:
    pow.append(row.text)
