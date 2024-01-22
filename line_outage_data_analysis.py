"""
@author: ArturoGalofre
"""

# Import the necesary libraries for the project
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Previously collected data from line_outage_data_pull.py
data_df = pd.read_csv("api_data.csv")

# Filter by the Outages that occur on lines and evaluate only the ones that have been implemented
line_data_df = data_df[(data_df['EquipType'] == 'Line') & (data_df['Status'] == 'Implemented')]

# Filter only for the lines we're interested in (315 and 317)
line_data_df = line_data_df[line_data_df['EquipDesc'].str.contains('315|327')]

# Remove duplicates from the EquipDesc, PlnStart, PlnEnd
line_data_df = line_data_df.drop_duplicates(subset=['AppNumber'])

# Convert 'BeginDate' column to datetime format, create column containing the duration of the outage in datetime and in minutes
line_data_df['Date'] = pd.to_datetime(line_data_df['BeginDate'], utc=True)
line_data_df['Duration'] = pd.to_datetime(line_data_df['PlnEnd'], utc=True) - pd.to_datetime(line_data_df['PlnStart'], utc=True)
line_data_df['TotalHours'] = line_data_df['Duration'].dt.days*24 + line_data_df['Duration'].dt.components['hours'] + line_data_df['Duration'].dt.components['minutes'] /60 + line_data_df['Duration'].dt.components['seconds'] /3600

# Counting occurrences of each 'EquipDesc'
equip_counts = line_data_df['TotalHours'].sum()

# Grouping by year ('Date') and 'EquipDesc', calculating the sum of 'TotalMinutes'
yearly_data = line_data_df.groupby([line_data_df['Date'].dt.year, 'EquipDesc'])['TotalHours'].sum().unstack()

# Set new names for columns
yearly_data.columns = ['315', '327']

# Convert the index (PeriodIndex) to string for merging
yearly_data.index = yearly_data.index.astype(str)

# Merge to fill missing months with a value of 0
date_list = ['2017', '2018', '2019', '2020', '2021', '2022', '2023']
date_df = pd.DataFrame(date_list, columns=['Date'])
merged_df = date_df.merge(yearly_data, how='left', left_on='Date', right_index=True).fillna(0)

# Plotting line diagram
merged_df.set_index('Date').plot(kind='line', marker='o')
plt.xlabel('Year')
plt.ylabel('Total Hours')
plt.title('Yearly Graph for Line Outages in 315 and 327')
plt.legend(title='EquipDesc')
plt.grid(True)
plt.savefig('OccurencesTimeSeries.png')

# Plotting pie Plot
line315_total = merged_df['315'].sum()
line327_total = merged_df['327'].sum()
sizes = [line315_total/(line315_total + line327_total), line327_total/(line315_total + line327_total)]
labels = ['315', '327']
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('Distribution of line outage time')
plt.savefig('PieDistribution.png')

# Changing the name of the column to have the same format in both
line_data_df['EquipDesc'] = line_data_df['EquipDesc'].replace('315: W_FARNUM', '315')
line_data_df.to_csv('line_data_df.csv', index=False, mode = 'w')

# Generate a range of dates for the year 2022
dates_2022 = pd.date_range(start='2022-01-01', end='2022-12-31', freq='H')

# Create a DataFrame with columns for year, month, day, and hour
date_df = pd.DataFrame({
    'Year': dates_2022.year,
    'Month': dates_2022.month,
    'Day': dates_2022.day,
    'Hour': dates_2022.hour,
    'Date': pd.to_datetime(dates_2022).tz_localize(tz = 'UTC')
})

# Set values for the columns 'PlnStart' and 'PlnEnd'
line_data_df['PlnStart'] = pd.to_datetime(line_data_df['PlnStart'], utc=True)
line_data_df['PlnEnd'] = pd.to_datetime(line_data_df['PlnEnd'], utc=True)

# Add two columns ('Value315' and 'Value327') to the 'date_df' DataFrame based on date ranges
# and equipment descriptions specified in the 'line_data_df' DataFrame. If the 'Date' in 'date_df' falls within the
# specified date range for a given equipment description ('EquipDesc') matching '315' or '327', the corresponding column
# is set to 1; otherwise, it is set to 0.
date_df['Value315'] = date_df.apply(lambda row: 1 if any((row['Date'] >= start) and (row['Date'] <= end) for start, end, equip in zip(line_data_df['PlnStart'], line_data_df['PlnEnd'], line_data_df['EquipDesc']) if equip == '315') else 0, axis=1)
date_df['Value327'] = date_df.apply(lambda row: 1 if any((row['Date'] >= start) and (row['Date'] <= end) for start, end, equip in zip(line_data_df['PlnStart'], line_data_df['PlnEnd'], line_data_df['EquipDesc']) if equip == '327') else 0, axis=1)

# Generate a line plot to visualize outage trends for equipment descriptions '315' and '327'
# based on the 'Value315' and 'Value327' columns in the 'date_df' DataFrame.
plt.figure(figsize=(25, 6))
date_df.set_index('Date')[['Value315', 'Value327']].plot(kind='line', marker='')
plt.xlabel('Date')
plt.ylabel('Outage')
plt.title('Outage Trends for EquipDesc 315 and 327')
plt.legend(title='EquipDesc')
plt.grid(True)
plt.savefig('OutageOnOff.png')

# Create a new DataFrame 'save_df' containing columns 'Date', 'Value315', and 'Value327'
# from the 'date_df' DataFrame. Then saves this DataFrame to a CSV file.
save_df = date_df[['Date', 'Value315', 'Value327']]
save_df.to_csv('save_df.csv', index = False, mode = 'w')
