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
import os
import plotly.express as px

st.title('12 day Milestone Ticker app')
st.write('Stock data test: IBM')

key = os.environ['key']


# In[ ]:


def request_stock_price_hist(symbol, token, year_stop, sample = False):
    if sample == False:
        q_string = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=full&apikey={}'
    else:
        q_string = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'

    st.write("Starting stock price data retrieval from Alpha Vantage (This may take a while)...")
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
        year_stop = str(int(year_stop)-1)
        if i[0:4]=='2009' or i[0:4]==str(year_stop): # only load data from 2010 onward
            bar.progress(100)
            break
    df.columns = ["open", "high", "low", "close", "adjusted close", "volume", "dividend amount", "split cf"]
    df['date'] = date
    return df


# In[ ]:


# add user input
ticker_symbol=[]
year_select=[]
month_select=[]
ticker_symbol = st.text_input("Pick a stock ticker label (e.g., IBM, AAPL, GOOGL):")
year_select = st.selectbox('Pick a year:',list(['Select']) + list(range(2010,2021)))
month_select = st.selectbox('Pick a month:',list(range(1,13)))


# In[ ]:


if len(ticker_symbol)!=0 and year_select!='Select' and month_select>1:
    df = request_stock_price_hist(ticker_symbol, key,year_select)
    df['adjusted close']=pd.to_numeric(df['adjusted close'], errors='coerce')
    df['date']=pd.to_datetime(df['date'],format='%Y-%m-%d')
    # plots     
    date_start = str(year_select) + '-' + str(month_select) + '-' + '01'
    date_end =  str(year_select) + '-' + str(int(month_select)+1) + '-' + '01'
    df = df[(df['date'] > pd.to_datetime(date_start)) & (df['date'] < pd.to_datetime(date_end))]
    fig = px.line(df, x="date", y="adjusted close",hover_name="date",render_mode="svg")
    st.plotly_chart(fig)


# In[ ]:


# convert date to year and month variables
#date_time_obj = datetime.strptime(df['date'], '%d/%m/%y %H:%M:%S')

