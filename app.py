import streamlit as st
import pandas as pd
import numpy as np
from yahoofinancials import YahooFinancials as yho
import ffn
from datetime import datetime as dt
import pandas_datareader as web
import yfinance


start = dt(2021,1,1)
 
def hist_data():
    data = []    
    r = web.DataReader(inputTicker,'yahoo',start)
    r['Stock'] = inputTicker
    data.append(r)
        
    df = pd.concat(data)  
    df = df.reset_index()
    df = df[['Date','Stock','Close','Volume']]
    df['% change'] = df['Close'].pct_change()*100
    
    return df
    


def price():
    yf = yho(inputTicker)
    cp = yf.get_current_price()
    return cp

def pr_change():
    yf = yho(inputTicker)
    cng = str(round(yf.get_current_percent_change()*100,2))+"%"
    return cng

def volume():
    yf = yho(inputTicker)
    vlm = yf.get_current_volume()
    return vlm

def vlm_change():
    yf = yho(inputTicker)
    vlm = yf.get_current_volume()
    td_vol = yf.get_ten_day_avg_daily_volume()
    vlm_cng = str(round(vlm/td_vol-1,2))+"%"
    return vlm_cng

st.title('Stock Data')
tickerForm = st.form('Input Stock Ticker')
inputTicker = tickerForm.text_input('Enter Stock Symbol','aapl')
stock = inputTicker.upper()

yf = yho(inputTicker)
fst = yf.get_key_statistics_data()
sr = fst[stock]['shortRatio']
curr_si = round(fst[stock]['shortPercentOfFloat']*100,2)
evr = round(fst[stock]['enterpriseToRevenue'],2)
ev_ebitda = round(fst[stock]['enterpriseToEbitda'],2)
fwd_pe = round(fst[stock]['forwardPE'],2)

symbol = yfinance.Ticker('aapl')
summary = symbol.info['longBusinessSummary']
curr_rat = symbol.info['currentRatio']
roe = symbol.info['returnOnEquity']  
fcf = round(symbol.info['freeCashflow']/symbol.info['totalRevenue']*100,2)

infoType = tickerForm.radio(
        "Choose an info type",
        ('Current Data', 'Fundamental/Historical Data','All')
    ) 
prices = ffn.get(inputTicker,start='2021-01-01')
statistics = prices.calc_stats()
stata = statistics.display()
button = tickerForm.form_submit_button('Go')

if button:
    if(infoType == 'Current Data'):
        col1, col2 = st.columns(2)
        col1.metric(label='Most Recent Price', value=price(),delta=pr_change())
        col2.metric(label="Day's Volume vs 10d Avg Volume",value=volume(),delta=vlm_change())
        st.header('Company Overview')
        st.write(summary)
        st.header('Key Stats')
        col_1,col_2,col_3 = st.columns(3)
        col_1.subheader('Forward P/E: '+str(fwd_pe))
        col_2.subheader('EV/Revenue: '+str(evr))
        col_3.subheader('EV/EBITDA: '+str(ev_ebitda))
        
        col4,col5,col6 = st.columns(3)
        col4.subheader('Return on Equity: '+str(round(roe,2)))
        col5.subheader('Current Ratio: '+str(curr_rat))
        col6.subheader('Free Cash Flow/Revenue: '+str(fcf)+'%')
    elif (infoType == 'Fundamental/Historical Data'):
        st.write(stata)
        st.write(hist_data())
    elif (infoType == 'All'):
        col1, col2 = st.columns(2)
        col1.metric(label='Most Recent Price', value=price(),delta=pr_change())
        col2.metric(label="Day's Volume vs 10d Avg Volume",value=volume(),delta=vlm_change())
        st.header('Company Overview')
        st.write(summary)
        st.header('Key Stats')
        col_1,col_2,col_3 = st.columns(3)
        col_1.subheader('Forward P/E: '+str(fwd_pe))
        col_2.subheader('EV/Revenue: '+str(evr))
        col_3.subheader('EV/EBITDA: '+str(ev_ebitda))
        
        col4,col5,col6 = st.columns(3)
        col4.subheader('Return on Equity: '+str(round(roe,2)))
        col5.subheader('Current Ratio: '+str(curr_rat))
        col6.subheader('Free Cash Flow/Revenue: '+str(fcf)+'%')          
        st.write(hist_data())