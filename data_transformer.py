#!/usr/bin/env python
# coding: utf-8

# In[1]:


def transform_data(df):
    df = df.copy()

    # Convert millions to billions
    df['Federal Debt: Total Public Debt'] /= 1_000
    df['Federal Debt Held by the Public'] /= 1_000

    # Feature engineering
    df['Real GDP'] = df['GDP'] / df['CPI']
    df['y-o-y inflation']= (df['CPI']-df['CPI'].shift(4))/df['CPI'].shift(4)
    df['y-o-y inflation']= (df['CPI']-df['CPI'].shift(1))/df['CPI'].shift(1)
    df['Net Exports'] = df['Imports'] - df['Exports']

    return df

