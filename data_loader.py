from fredapi import Fred
import pandas as pd
import streamlit as st
import concurrent.futures

# Load API key from Streamlit secrets
FRED_API_KEY = st.secrets["api_key"]
fred = Fred(api_key=FRED_API_KEY)

# Quarterly series
quarterly_series = {
    'GDP': 'GDP',
    'Real GDP': 'GDPC1',
    'Imports': 'IMPGS',
    'Exports': 'EXPGS',
    'Federal Debt Total Public Debt': 'GFDEBTN',
    'Federal Debt Held by Federal Reserve Banks': 'FDHBFRBN',
    'Federal Debt Held by Private Investors': 'FDHBPIN',
    'Federal Debt Held by the Public': 'FYGFDPUN',
    'Federal Debt Held by Foreign and International Investors': 'FDHBFIN',
    'Federal Debt Held by Agencies and Trusts': 'FDHBATN',
    'Federal Debt: Total Public Debt as Percent of GDP': 'GFDEGDQ188S',
    'Delinquency Rate on Business Loans, All Commercial Banks': 'DRBLACBS',
    'Delinquency Rate on Credit Card Loans, All Commercial Banks': 'DRCCLACBS',
    'Delinquency Rate on Consumer Loans, All Commercial Banks': 'DRCLACBS',
    'Delinquency Rate on All Loans, All Commercial Banks': 'DRALACBN'
}

# Monthly series
monthly_series = {
    'Unemployment Rate': 'UNRATE',
    'CPI': 'CPIAUCSL',
    'PCE': 'PCE',
    'Labor Force Participation Rate': 'CIVPART',
    'Job Openings Total Nonfarm': 'JTSJOL',
    'Unemployment Level': 'UNEMPLOY',
    'Federal Funds Effective Rate': 'FEDFUNDS',
    'M1': 'M1SL',
    'M2': 'M2SL',
    'Monthly Transition Rate of All U.S. Workers From Employment to Non-Employment Due to a Layoff': 'EMELASA',
    'Monthly Transition Rate of Prime-Age U.S. Workers From Employment to Non-Employment Due to a Layoff': 'EMELPSA',
    'Monthly Transition Rate of All U.S. Workers From Employment to Non-Employment Due to a Quit': 'EMEQASA',
    'Monthly Transition Rate of Prime-Age U.S. Workers From Employment to Non-Employment Due to a Quit': 'EMEQPSA',
    'Monthly Share of All U.S. Workers Who Leave the Labor Force After a Layoff': 'EMSHRNLA',
    'Monthly Share of Prime-Age U.S. Workers Who Leave the Labor Force After a Layoff': 'EMSHRNLP',
    'Monthly Share of All U.S. Workers Who Leave the Labor Force After a Quit': 'EMSHRNQA',
    'Monthly Share of Prime-Age U.S. Workers Who Leave the Labor Force After a Quit': 'EMSHRNQP',
    'University of Michigan: Consumer Sentiment': 'UMCSENT',
    'University of Michigan: Inflation Expectation': 'MICH',
    'Economic Policy Uncertainty Index for United States': 'USEPUINDXM',
    'Average Hourly Earnings of All Employees, Total Private': 'CES0500000003',
    'Average Weekly Hours of All Employees, Total Private': 'AWHAETP',
    'All Employees Total Nonfarm': 'PAYEMS'
}

# Weekly series
weekly_series = {
    'Initial Claims': 'ICSA',
    'Continued Claims (Insured Unemployment)': 'CCSA',
    '4-Week Moving Average of Initial Claims': 'IC4WSA',
    '4-Week Moving Average of Continued Claims (Insured Unemployment)': 'CC4WSA'
}

# Fetch a single series (used in parallel)
def fetch_single_series(name_code_tuple):
    name, code = name_code_tuple
    try:
        series = fred.get_series(code)
        print(f"{name} latest date: {series.index[-1]}")
        return (name, series)
    except Exception as e:
        print(f"Failed to load {name} ({code}): {e}")
        return (name, None)

# Fetch series in parallel
def fetch_series(series_dict):
    data = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_single_series, series_dict.items())
    for name, series in results:
        if series is not None and not series.empty:
            data[name] = series
        else:
            print(f"⚠️ {name} returned empty or failed.")
    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df.index)
    return df

# Master loader function for all frequencies
def fetch_data_by_frequency():
    df_quarterly = fetch_series(quarterly_series)
    df_monthly = fetch_series(monthly_series)
    df_weekly = fetch_series(weekly_series)
    return df_quarterly, df_monthly, df_weekly
