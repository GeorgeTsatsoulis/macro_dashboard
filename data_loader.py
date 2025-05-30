from fredapi import Fred
import pandas as pd

FRED_API_KEY = '11f924d3790c425dfbe96b3381aa0b3b'

def fetch_data_by_frequency():
    fred = Fred(api_key=FRED_API_KEY)
    
    # Quarterly series (including all federal debt series)
    quarterly_series = {
        'GDP': 'GDP',
        'Real GDP':'GDPC1',
        'Imports': 'IMPGS',
        'Exports': 'EXPGS',
        'Federal Debt Total Public Debt': 'GFDEBTN',
        'Federal Debt Held by Federal Reserve Banks': 'FDHBFRBN',
        'Federal Debt Held by Private Investors': 'FDHBPIN',
        'Federal Debt Held by the Public': 'FYGFDPUN',
        'Federal Debt Held by Foreign and International Investors': 'FDHBFIN',
        'Federal Debt Held by Agencies and Trusts': 'FDHBATN',
        'Federal Debt: Total Public Debt as Percent of GDP':'GFDEGDQ188S',
        'Delinquency Rate on Business Loans, All Commercial Banks': 'DRBLACBS',
        'Delinquency Rate on Credit Card Loans, All Commercial Banks': 'DRCCLACBS',
        'Delinquency Rate on Consumer Loans, All Commercial Banks':'DRCLACBS',
        'Delinquency Rate on All Loans, All Commercial Banks':'DRALACBN'

    }
    
    # Monthly series
    monthly_series = {
        'Unemployment Rate': 'UNRATE',
        'CPI': 'CPIAUCSL',
        'PCE':'PCE',
        'Labor Force Participation Rate':'CIVPART',
        'Job Openings Total Nonfarm':'JTSJOL', ## in thousands
        'Unemployment Level':'UNEMPLOY', ##in thousands,
        'Federal Funds Effective Rate':'FEDFUNDS', ##percent
        'M1':'M1SL', ###in billions
        'M2':'M2SL', #in billions,
        'Monthly Transition Rate of All U.S. Workers From Employment to Non-Employment Due to a Layoff':'EMELASA',
        'Monthly Transition Rate of Prime-Age U.S. Workers From Employment to Non-Employment Due to a Layoff':'EMELPSA',
        'Monthly Transition Rate of All U.S. Workers From Employment to Non-Employment Due to a Quit':'EMEQASA',
        'Monthly Transition Rate of Prime-Age U.S. Workers From Employment to Non-Employment Due to a Quit':'EMEQPSA',
        'Monthly Share of All U.S. Workers Who Leave the Labor Force After a Layoff':'EMSHRNLA',
        'Monthly Share of Prime-Age U.S. Workers Who Leave the Labor Force After a Layoff':'EMSHRNLP',
        'Monthly Share of All U.S. Workers Who Leave the Labor Force After a Quit':'EMSHRNQA',
        'Monthly Share of Prime-Age U.S. Workers Who Leave the Labor Force After a Quit':'EMSHRNQP',
        'University of Michigan: Consumer Sentiment':'UMCSENT', ##Index 1966:Q1=100
        'University of Michigan: Inflation Expectation':'MICH',
        'Economic Policy Uncertainty Index for United States':'USEPUINDXM'

    }
    
    weekly_series = {'Initial Claims':'ICSA' ## number
    }

    def fetch_series(series_dict):
        data = {}
        for name, code in series_dict.items():
            try:
                data[name] = fred.get_series(code)
            except Exception as e:
                print(f"Failed to load {name} ({code}): {e}")
        df = pd.DataFrame(data)
        df.dropna(inplace=True)
        df.index = pd.to_datetime(df.index)
        return df
    
    df_quarterly = fetch_series(quarterly_series)
    df_monthly = fetch_series(monthly_series)
    df_weekly= fetch_series(weekly_series)
    
    return df_quarterly, df_monthly,df_weekly

