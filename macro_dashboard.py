#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fredapi import Fred
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px


# ## Data Fetching

# In[2]:


fred = Fred(api_key='11f924d3790c425dfbe96b3381aa0b3b')


# In[3]:


# Define series IDs for the indicators
series_ids = {
    'GDP': 'GDP',
    'CPI': 'CPIAUCSL',
    'Unemployment Rate': 'UNRATE',
    'Fed Funds Rate': 'FEDFUNDS',
    'Imports': 'IMPGS',
    'Exports': 'EXPGS',
    'Federal Debt: Total Public Debt':'GFDEBTN',
    'Federal Debt Held by Federal Reserve Banks':'FDHBFRBN',
    'Federal Debt Held by Private Investors':'FDHBPIN',
    'Federal Debt Held by the Public':'FYGFDPUN',
    'Federal Debt Held by Foreign and International Investors':'FDHBFIN',
    'Delinquency Rate on Business Loans, All Commercial Banks':'DRBLACBS',
    'Delinquency Rate on Credit Card Loans, All Commercial Banks': 'DRCCLACBS',
}

# Fetch data
data = {}
for indicator, series_id in series_ids.items():
    data[indicator] = fred.get_series(series_id)

# Convert to DataFrame
df = pd.DataFrame(data)
df.head()


# ## Check the first non-nan value

# In[4]:


# Find the index of the first non-NaN in each column
first_valid_indices = df.apply(lambda col: col.first_valid_index())

print("First non-NaN indices in each column:")
print(first_valid_indices)


# In[5]:


#df.dropna(inplace=True)
#df.head()


# ## Data conversion and creation of new variables

# In[6]:


# Convert millions to billions
df['Federal Debt: Total Public Debt'] /= 1_000
df['Federal Debt Held by the Public'] /= 1_000


# In[7]:


df['Real GDP'] = df['GDP']/df['CPI']
df['y-o-y inflation']= (df['CPI']-df['CPI'].shift(4))/df['CPI'].shift(4)
df['y-o-y inflation']= (df['CPI']-df['CPI'].shift(1))/df['CPI'].shift(1)
df['Net Exports'] = df['Imports'] - df['Exports']
df.head()


# In[8]:


pip freeze > requirements.txt


# In[10]:


import plotly.graph_objects as go


st.title("Macro Dashboard (Test Plotting)")

# Show preview
st.subheader("Data Preview")
st.dataframe(df.tail())

# Let user choose which columns to plot
columns_to_plot = st.multiselect("Select columns to plot:", df.columns.tolist(), default=df.columns.tolist())

if columns_to_plot:
    st.subheader("Line Chart")

    fig = go.Figure()
    for col in columns_to_plot:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))

    fig.update_layout(title="Selected Indicators", xaxis_title="Date", yaxis_title="Value")
    st.plotly_chart(fig)
else:
    st.info("Select at least one variable to plot.")

