import os
import pandas as pd
import numpy as np

## Creating a benchmark made of top 10 crypto currencies based on market capitalization.

filename = ['btcusd','ethusd','ustusd','adausd','solusd','xrpusd','luna-usd','doge-usd','dotusd']

## Reading the file
path = r'/Users/rajanand/Documents/Github/Data/archive'

def ReadFile(name):
    dummy = pd.read_csv(os.path.join(path,name+'.csv'))#,index_col=0, infer_datetime_format=True)
    dummy['time'] = pd.to_datetime(dummy['time'], unit='ms')
    dummy.set_index('time',inplace=True)
    ## Aggregating over days
    dummy = dummy.resample('1D').mean()
    return dummy

### Function to aggregate the closing price for all the cryptos and making a equally weighted index.

def MergeAll(col, filelist):
    master_df = pd.DataFrame(ReadFile(filelist[0])[col]).rename(columns = {col:filelist[0]})
    master_df = master_df.loc[master_df.index >= '2017-01-01']
    for name in filelist[1:]:
        master_df = master_df.merge(pd.DataFrame(ReadFile(name)[col]).rename(columns = {col:name}), how='left', right_index=True, left_index=True)

    return master_df.pct_change().dropna(how='all', axis=0)

def BenchmarkCreation(filename):
    return_df = MergeAll('close',filename)
    weight_col = pd.DataFrame(1/(len(filename) - return_df.isna().sum(axis=1)), index=return_df.index)
    weighted_df = pd.DataFrame(np.array(return_df) * np.array(weight_col), index=return_df.index, columns=return_df.columns)
    return pd.DataFrame(weighted_df.sum(axis=1), index=weighted_df.index, columns=['Benchmark'])

BenchmarkCreation(filename).to_csv('Benchmark.csv')