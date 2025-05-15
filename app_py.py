#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
from data_loader import fetch_macro_data
from data_transformer import transform_data
import plotly.graph_objects as go


# In[ ]:


# Title
st.title("Macro Dashboard")

# Load & transform data
df = fetch_macro_data()
df = transform_data(df)

# Display data
st.subheader("Data Preview")
st.dataframe(df.tail())

# User selects which variables to plot
selected_columns = st.multiselect("Select variables to plot (separate plots):", df.columns.tolist())

if selected_columns:
    for col in selected_columns:
        st.subheader(col)
        st.line_chart(df[[col]].dropna())
else:
    st.info("Please select at least one variable.")


# In[ ]:


# ----------------------------
# FRED Series for Federal Debt
# ----------------------------
federal_debt_series = {
    'Federal Debt Total Public Debt': 'GFDEBTN',
    'Held by Federal Reserve Banks': 'FDHBFRBN',
    'Held by Private Investors': 'FDHBPIN',
    'Held by the Public': 'FYGFDPUN',
    'Held by Foreign/Intl Investors': 'FDHBFIN'
}

# ----------------------------
# Fetch Federal Debt Data
# ----------------------------
@st.cache_data
def fetch_federal_debt_data():
    df = pd.DataFrame()
    for name, series_id in federal_debt_series.items():
        df[name] = fred.get_series(series_id)
    return df.dropna()

# ----------------------------
# Streamlit App Start
# ----------------------------
st.set_page_config(layout="wide")
st.title("💸 Macro Dashboard – United States Federal Debt")

# ----------------------------
# Section 1: Federal Debt Area Chart
# ----------------------------
st.header("📊 Federal Debt Composition Over Time")

df_debt = fetch_federal_debt_data()

fig = go.Figure()

for col in df_debt.columns:
    fig.add_trace(go.Scatter(
        x=df_debt.index,
        y=df_debt[col],
        mode='lines',
        name=col,
        stackgroup='one',
        line=dict(width=0.5),
        hoverinfo='x+y'
    ))

fig.update_layout(
    title="Federal Debt Components (Stacked Area Chart)",
    xaxis_title="Date",
    yaxis_title="USD (raw values)",
    legend_title="Debt Category",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Add more charts below this
# ----------------------------
st.markdown("---")
st.subheader("📈 Add other macro charts below...")
# Example: st.line_chart(df[['GDP']])

