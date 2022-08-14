import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# separate out required tables
def update_table(curr_data, t):
    df = pd.read_html(t)
    oav_administered = df[0]
    string_filter = 'Paxlovid|Lagevrio'
    oav_administered = oav_administered[oav_administered['Therapeutic'].str.contains(string_filter, regex = True)].copy()
    oav_administered['Therapeutic'] = oav_administered['Therapeutic'].str.replace('\d+', '', regex = True)
    oav_administered.columns = oav_administered.columns.str.replace('\d+', '', regex = True)
    oav_administered['Last Updated'] = last_updated
    oav_administered['Period End'] = period_end
    combined_data = pd.concat([curr_data, oav_administered])
    return oav_administered, combined_data

# create date settings
today_timestamp = pd.Timestamp.now(tz='US/Eastern')
today_str = today_timestamp.strftime('%Y-%m-%d')
last_updated = today_timestamp.strftime('%Y-%m-%d %H:%M')

# get the latest date that the table was updated
url = 'https://aspr.hhs.gov/COVID-19/Therapeutics/orders/pages/default.aspx'
response = requests.get(url)
t = response.text
soup = BeautifulSoup(t, features = "html.parser")
pattern = re.compile(r'December 17, 2021')
period_end = soup.find(text = pattern).split('–')[-1].strip()
period_end = pd.to_datetime(period_end)

# import currently existing data
curr_data = pd.read_csv('data/COVID_19_Therapeutics_Summary_latest.csv', parse_dates = ['Period End'])

# check if the underlying table on the webpage has been updated
if period_end > curr_data['Period End'].max():
    oav_administered, combined_data = update_table(curr_data, t)
    print('Exporting Tables to CSV.')
    oav_administered.to_csv(f'data/COVID_19_Therapeutics_Summary_{today_str}.csv', index = False)
    combined_data.to_csv(f'data/COVID_19_Therapeutics_Summary_latest.csv', index = False)