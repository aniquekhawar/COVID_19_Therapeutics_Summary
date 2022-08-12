import pandas as pd

# create date settings
today_timestamp = pd.Timestamp.now(tz='US/Eastern')
today_str = today_timestamp.strftime('%Y-%m-%d')

# get the beginning of the week (Sunday), which should be the cutoff for the data
period_end = (today_timestamp - pd.offsets.Week(weekday=6)).strftime('%Y-%m-%d')
last_updated = today_timestamp.strftime('%Y-%m-%d %H:%M')

url = 'https://aspr.hhs.gov/COVID-19/Therapeutics/orders/pages/default.aspx'
df = pd.read_html(url)

# separate out required tables
oav_administered = df[0]
string_filter = 'Paxlovid|Lagevrio'
oav_administered = oav_administered[oav_administered['Therapeutic'].str.contains(string_filter, regex = True)].copy()
oav_administered['Therapeutic'] = oav_administered['Therapeutic'].str.replace('\d+', '', regex = True)
oav_administered.columns = oav_administered.columns.str.replace('\d+', '', regex = True)
oav_administered['Last Updated'] = last_updated
oav_administered['Period End'] = period_end

oav_administered.to_csv(f'data/COVID_19_Therapeutics_Summary_{today_str}.csv', index = False)
oav_administered.to_csv(f'data/COVID_19_Therapeutics_Summary_latest.csv', index = False)