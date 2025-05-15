#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fredapi import Fred
import pandas as pd


# In[3]:


FRED_API_KEY  ='11f924d3790c425dfbe96b3381aa0b3b'
fred = Fred(api_key=FRED_API_KEY)


# In[4]:


series_ids = {
    'GDP': 'GDP',
    'CPI': 'CPIAUCSL',
    'Unemployment Rate': 'UNRATE',
    'Fed Funds Rate': 'FEDFUNDS',
    'Imports': 'IMPGS',
    'Exports': 'EXPGS',
    'Federal Debt Total Public Debt':'GFDEBTN',
    'Federal Debt Held by Federal Reserve Banks':'FDHBFRBN',
    'Federal Debt Held by Private Investors':'FDHBPIN',
    'Federal Debt Held by the Public':'FYGFDPUN',
    'Federal Debt Held by Foreign and International Investors':'FDHBFIN',
    'Delinquency Rate on Business Loans, All Commercial Banks':'DRBLACBS',
    'Delinquency Rate on Credit Card Loans, All Commercial Banks': 'DRCCLACBS',
}


# In[5]:


def fetch_macro_data():
    data = {}
    for name, series_id in series_ids.items():
        data[name] = fred.get_series(series_id)
    df = pd.DataFrame(data)
    return df

