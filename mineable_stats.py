'''
Generating stats for mineable coins
'''

import requests

# 12 calls per min (data refreshes every 5-10 min)
class Mineable:
    def __init__(self, ticker):
        self.url = 'https://api.minerstat.com/v2/coins?list=' + ticker

    def get_algorithm(self):
        response = requests.get(self.url)
        try:
            return response.json()[0]['algorithm']
        except:
            return []
    def get_hashrate(self):
        response = requests.get(self.url)
        try:
            return response.json()[0]['network_hashrate']
        except:
            return []
    def get_difficulty(self):
        response = requests.get(self.url)
        try:
            return response.json()[0]['difficulty']
        except:
            return []
    def get_reward(self):
        response = requests.get(self.url)
        try:
            return response.json()[0]['reward']
        except:
            return []
    def get_reward_block(self):
        response = requests.get(self.url)
        try:
            return response.json()[0]['reward_block']
        except:
            return []
    def get_updated_time(self):
        response = requests.get(self.url)
        try:
            return response.json()[0]['updated']
        except:
            return []
