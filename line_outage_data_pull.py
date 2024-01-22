"""
@author: ArturoGalofre
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#Perform an APIN call to ISO New England online service to obtain the data needed for the analysis
def get_outage_data(api_endpoint, day, outageType, station):
    api_complete_key = f"{api_endpoint}/outages/day/{day}/outageType/{outageType}/station/{station}"
    
    # Make a GET request to the API endpoint
    response = requests.get(api_complete_key, auth=(username, password), headers={'Accept': 'application/json'})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.json()
    else:
        # Print an error message if the request was unsuccessful
        print(f"Failed to fetch data. Status code: {response.status_code}")



api_endpoint = 'https://webservices.iso-ne.com/api/v1.1'
outageType = 'short-term' #[x]xxxx-xxxx
station = 'BRAYTNPT' #XXXXXXXX

username = 'your_username'
password = 'your_username'

# Start date (10 years ago from '2023-11-30')
end_date = datetime.strptime('2023-11-30', '%Y-%m-%d') - timedelta(days=10*365)

# End date (today)
start_date = datetime.now()


columns = ['BeginDate', 'AppNumber', 'Company1', 'ToStation', 'FromStation',
       'EquipType', 'EquipDesc', 'Volt', 'PlnStart', 'PlnEnd', 'Status',
       'ReqType', 'EcoFlag', 'MtoFlag', 'OvrFlag', 'NonLineStation',
       'ActStart']

api_data = pd.DataFrame(columns = columns)
timer = 0


# while loop to obtain all the data for the preiod we're interested in:
while start_date > end_date:
    # Format the date in YYYYMMDD
    date_str = start_date.strftime('%Y%m%d')
    api_response_data = get_outage_data(api_endpoint, date_str, outageType, station)

    try:
        api_response_df = pd.DataFrame(api_response_data['Outages'][0]['Outage'])
        api_data = pd.concat([api_data, api_response_df])

    except:
        pass
    
    # Move to the previous date
    start_date += timedelta(days=-1)

    timer += 1
    
    # Show how many years worth of data have been obtained
    if timer%365 == 0:
        print(f'Process update (Year = {timer/365})')
    
# Save data to a CSV file in order to analyse it
api_data.to_csv('api_data.csv', index=False, mode = 'w')
