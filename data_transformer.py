def transform_quarterly_data(df):
    df = df.copy()
    
    # scale federal debt columns to billions
    scale_to_billions = [
    'Federal Debt Total Public Debt',
    'Federal Debt Held by the Public',
    'Federal Debt Held by Agencies and Trusts'
    ]   
    
    for col in scale_to_billions:
       if col in df.columns:
        df[col] /= 1_000  # Convert millions to billions
    
    # compute GDP deflator
    if 'GDP' in df.columns and 'Real GDP' in df.columns:
       df['GDP deflator'] = (df['GDP'] / df['Real GDP']) * 100

    if 'Real GDP' in df.columns:
       df['Real GDP Growth'] = (df['Real GDP'] / df['Real GDP']) * 100

    if 'Exports' in df.columns and 'Imports' in df.columns:
       df['Net Exports'] = df['Exports'] / df['Imports']

    return df

def transform_monthly_data(df):
    df = df.copy()

    # compute inflations
    if 'CPI' in df.columns:
        df['CPI YoY Inflation'] = (df['CPI']-df['CPI'].shift(12))/df['CPI'].shift(12)

    if 'PCE' in df.columns:
        df['PCE YoY Inflation'] = (df['PCE']-df['PCE'].shift(12))/df['PCE'].shift(12)

    if 'Job Openings Total Nonfarm' in df.columns and 'Unemployment Level' in df.columns:
       df['Job Vacancy-to-Unemployment Ratio'] = df['Job Openings Total Nonfarm'] / df['Unemployment Level'] 

    return df

def transform_weekly_data(df):
    df = df.copy() ## placeholder for more data in the future

    return df

