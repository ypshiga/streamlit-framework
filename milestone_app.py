#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# test stock API 
# Your API key is: IRC9K9I0TMTQZPK7
import requests
import pandas as pd
import numpy as np
import streamlit as st
import time
from datetime import datetime
from boto.s3.connection import S3Connection
import os

st.title('12 day Milestone Ticker app')
st.write('Stock data test: IBM')

key = S3Connection(os.environ['key'])
#key = 'IRC9K9I0TMTQZPK7'
ticker_symbol = 'IBM'


# In[ ]:


def request_stock_price_hist(symbol, token, sample = False):
    if sample == False:
        q_string = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=full&apikey={}'
    else:
        q_string = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'

    st.write("Retrieving stock price data from Alpha Vantage (This may take a while)...")
    r = requests.get(q_string.format(symbol, token))
    st.write("Data has been successfully downloaded...")
    date = []
    colnames = list(range(0, 7))
    df = pd.DataFrame(columns = colnames)
    st.write("Sorting the retrieved data into a dataframe...")
    latest_iteration = st.empty()
    bar = st.progress(0)
    i_tick = 0
    df_len = (len( r.json()['Time Series (Daily)'].keys()))
    for i in r.json()['Time Series (Daily)'].keys():
        date.append(i)
        row = pd.DataFrame.from_dict(r.json()['Time Series (Daily)'][i], orient='index').reset_index().T[1:]
        df = pd.concat([df, row], ignore_index=True)
        latest_iteration.text('Iteration ' + str((i_tick + 1)))
        bar.progress((i_tick + 1)/df_len)
        i_tick+=1
        if i_tick%500==0:
            time.sleep(0.1)
        if i[0:4]=='2009': # only load data from 2010 onward
            break
    df.columns = ["open", "high", "low", "close", "adjusted close", "volume", "dividend amount", "split cf"]
    df['date'] = date
    return df


# In[ ]:


'Here we go...'

df = request_stock_price_hist('IBM', key)
'...all done!'


# In[ ]:


year = 2020
month = 'June'


# In[ ]:


#date_time_obj = datetime.strptime(df['date'], '%d/%m/%y %H:%M:%S')


# In[ ]:


st.line_chart(df[['close', 'date']].loc[:365])

