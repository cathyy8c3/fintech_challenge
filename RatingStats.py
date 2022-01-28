import pandas as pd
import numpy as np
import os
import statsmodels.api as sm

class OneCryptoStats:
    ## Crypto and Benchmark are pandas series indexed with daily datetime
    def __init__(self, crypto, benchmark):
        self.crypto = crypto
        self.benchmark = benchmark
        self.RegressionStatus = 'Pass'

    def CAPMRegression(self):
        dummy = self.benchmark.merge(self.crypto, how='left', left_index=True, right_index=True)
        dummy.dropna(how='any', inplace=True)

        ### Assert that regression is atleast for last 6 months else give a result.
        try:
            assert dummy.shape[0] > 180
        except AssertionError:
            self.RegressionStatus = 'Fail'

        ## Doing the regression
        X = dummy['Benchmark']
        Y = dummy.drop('Benchmark', axis=1)
        X = sm.add_constant(X)
        linreg = sm.OLS(Y, X).fit()
        return linreg.params[0], linreg.params[1]

    def LastRollingStds(self):
        ## Rolling over 1 month, 2 month, 3 month, 6 months and 1 year
        dummy = pd.DataFrame()
        dummy['Std_1M'] = self.crypto.rolling(30).std()
        dummy['Std_2M'] = self.crypto.rolling(60).std()
        dummy['Std_3M'] = self.crypto.rolling(90).std()
        dummy['Std_6M'] = self.crypto.rolling(180).std()
        dummy['Std_1Y'] = self.crypto.rolling(360).std()

        return dummy.iloc[-1].to_dict()

    def LastReturns(self):
        ## Returns over last 1 month, 2 months, 3 months, 6 months and 1 year
        dummy = pd.DataFrame()
        dummy['Ret_1M'] = self.crypto.rolling(30).mean()
        dummy['Ret_2M'] = self.crypto.rolling(60).mean()
        dummy['Ret_3M'] = self.crypto.rolling(90).mean()
        dummy['Ret_6M'] = self.crypto.rolling(180).mean()
        dummy['Ret_1Y'] = self.crypto.rolling(360).mean()

        return dummy.iloc[-1].to_dict()

### Import the data for the crypto and benchmark
bench = pd.read_csv('Benchmark.csv', index_col = 0)
bench.index = pd.to_datetime(bench.index, infer_datetime_format=True)

## Reading the file
path = r'/Users/rajanand/Documents/Github/Data/archive'
def ReadFile(name):
    dummy = pd.read_csv(os.path.join(path,name+'.csv'))#,index_col=0, infer_datetime_format=True)
    dummy['time'] = pd.to_datetime(dummy['time'], unit='ms')
    dummy.set_index('time',inplace=True)
    ## Aggregating over days
    dummy = dummy.resample('1D').mean()
    return dummy

cry = pd.DataFrame(ReadFile('btcusd')['close']).rename(columns={'close':'BTC'})
cry = cry.pct_change().dropna(how='all', axis=0)

btc = OneCryptoStats(cry, bench)
alpha, beta = btc.CAPMRegression()
std_dict = btc.LastRollingStds()
ret_dict = btc.LastReturns()

