INDICATOR_UNITS = {
    'GDP': 'USD Billions',
    'Real GDP': 'USD Billions',
    'Real GDP Growth': 'Percent',
    'GDP Deflator': 'Index',
    'Imports': 'USD Billions',
    'Exports': 'USD Billions',
    'Net Exports': 'USD Billions',
    'Federal Debt Total Public Debt': 'USD Billions',
    'Federal Debt Held by Federal Reserve Banks': 'USD Billions',
    'Federal Debt Held by Private Investors': 'USD Billions',
    'Federal Debt Held by the Public': 'USD Billions',
    'Federal Debt Held by Foreign and International Investors': 'USD Billions',
    'Federal Debt Held by Agencies and Trusts': 'USD Billions',
    'Federal Debt: Total Public Debt as Percent of GDP': 'Percent',
    'Delinquency Rate on Business Loans, All Commercial Banks': 'Percent',
    'Delinquency Rate on Credit Card Loans, All Commercial Banks': 'Percent',
    'Delinquency Rate on Consumer Loans, All Commercial Banks':'Percent',
    'Delinquency Rate on All Loans, All Commercial Banks':'Percent',
    'Unemployment Rate': 'Percent',
    'CPI': 'Index (1982–84=100)',
    'PCE': 'Index (2012=100)',
    'CPI YoY Inflation': 'Percent',
    'PCE YoY Inflation': 'Percent',
    'Labor Force Participation Rate': 'Percent',
    'Job Openings Total Nonfarm': 'Thousands',
    'Initial Claims': 'Number of Claims',
    'Unemployment Level': 'Thousands',
    'Federal Funds Effective Rate': 'Percent',
    'M1': 'USD Billions',
    'M2': 'USD Billions',
    'Monthly Transition Rate of All U.S. Workers From Employment to Non-Employment Due to a Layoff':'Percent',
    'Monthly Transition Rate of Prime-Age U.S. Workers From Employment to Non-Employment Due to a Layoff':'Percent',
    'Monthly Transition Rate of All U.S. Workers From Employment to Non-Employment Due to a Quit':'Percent',
    'Monthly Transition Rate of Prime-Age U.S. Workers From Employment to Non-Employment Due to a Quit':'Percent',
    'Monthly Share of All U.S. Workers Who Leave the Labor Force After a Layoff':'Percent',
    'Monthly Share of Prime-Age U.S. Workers Who Leave the Labor Force After a Layoff':'Percent',
    'Monthly Share of All U.S. Workers Who Leave the Labor Force After a Quit':'Percent',
    'Monthly Share of Prime-Age U.S. Workers Who Leave the Labor Force After a Quit':'Percent',
    'University of Michigan: Consumer Sentiment':'Index (1966 Q1=100)',
    'University of Michigan: Inflation Expectation':'Percent',
    'Economic Policy Uncertainty Index for United States':'Index',
    'Continued Claims (Insured Unemployment)':'Number',
    '4-Week Moving Average of Continued Claims (Insured Unemployment)':'Number',
    '4-Week Moving Average of Initial Claims':'Number',
    'Average Hourly Earnings of All Employees, Total Private':'Dollar per Hour',
    'Average Weekly Hours of All Employees, Total Private':'Hours',
    'All Employees Total Nonfarm':'Thousands'
}

def get_yaxis_label(col_name):
    return INDICATOR_UNITS.get(col_name, "Value")