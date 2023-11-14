# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 09:47:55 2021

@author: u6026797
"""
#%% libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#%% data
pd.set_option('display.max_columns', None)
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
covid_df = pd.read_csv(url, index_col=0)
#print(covid_df.head())
#print(covid_df['Admin2']) #County
#%% Instructions
'''
Overall instructions:
As described in the homework description, each graphic you make must:
   1. Have a thoughtful title
   2. Have clearly labelled axes 
   3. Be legible
   4. Not be a pie chart
I should be able to run your .py file and recreate the graphics without error.
As per usual, any helper variables or columns you create should be thoughtfully
named.
'''

#%% viz 1
'''
Create a visualization that shows all of the counties in Utah as a time series,
similar to the one shown in slide 22 during the lecture. The graphic should
-Show cases over time
-Have all counties plotted in a background color (something like grey)
-Have a single county plotted in a contrasting color (something not grey)
-Have well formatted dates as the X axis
'''

v1 = covid_df[covid_df['Province_State'] == 'Utah']

date_columns = v1.columns[11:]
# Group data by month for each county in Utah
utah_county_totals = v1.groupby(['Admin2']).sum()
print(utah_county_totals)
# Plotting
plt.figure(figsize=(12, 6))

# Plot each county
for county in utah_county_totals.index:
    county_data = utah_county_totals.loc[county, date_columns]

    # Set color for Davis County to gold, and other counties to grey
    color = 'gold' if county == 'Davis' else 'grey'

    plt.plot(county_data.index, county_data.values, label=county, color=color)

# Format x-axis as months
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

# Rotate x-axis labels for better readability
plt.gcf().autofmt_xdate()

# Add labels and legend
plt.title('COVID-19 Cases by County in Utah')
plt.xlabel('Date')
plt.ylabel('Number of Cases')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Show the plot
plt.show()

#%% viz 2
'''
Create a visualization that shows the contrast between the county in Utah with
the most cases to date to a county in Florida with the most cases to date.
The graphic should:
-Have only two counties plotted
-Highlight the difference between the two comparison counties
You may use any style of graphic you like as long as it is effective (dense)
and readable
'''

# Filter rows for Utah and Florida
utah_data = covid_df[covid_df['Province_State'] == 'Utah']
florida_data = covid_df[covid_df['Province_State'] == 'Florida']

# Group data by county and sum the cases
utah_county_totals = utah_data.groupby('Admin2').sum().iloc[:, -1]
florida_county_totals = florida_data.groupby('Admin2').sum().iloc[:, -1]

# Find the county in Utah with the most cases
utah_max_county = utah_county_totals.idxmax()
utah_max_cases = utah_county_totals.max()

# Find the county in Florida with the most cases
florida_max_county = florida_county_totals.idxmax()
florida_max_cases = florida_county_totals.max()

# Plotting
plt.figure(figsize=(10, 6))

# Bar chart for Utah county
plt.bar(utah_max_county, utah_max_cases, color='blue', label='Utah', alpha=0.7)

# Bar chart for Florida county
plt.bar(florida_max_county, florida_max_cases, color='red', label='Florida', alpha=0.7)

# Highlight the difference between the two counties
plt.annotate(f'Difference: {florida_max_cases - utah_max_cases}',
             xy=(0.5, 0), xytext=(0, 50),
             xycoords=('axes fraction', 'figure fraction'),
             textcoords='offset points',
             ha='center', va='bottom', fontsize=12, color='black')

# Add labels and legend
plt.title('COVID-19 Cases in Utah vs Florida (Most Cases to Date)')
plt.xlabel('County')
plt.ylabel('Number of Cases (in 100k)')
plt.legend()

# Show the plot
plt.show()


#%% viz 3
'''
Create a visualization that shows BOTH the running total of cases for a single
county AND the daily new cases. The graphic should:
-Use two y-axes (https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html)
-Use color to contrast the two series being plotted
-Have well formatted dates as the X axis
'''
# Filter rows for Salt Lake County, Utah, and Orange County, California
# Function to plot running total and daily new cases for a given county
# Function to plot running total and daily new cases for a given county
# Filter rows for Salt Lake County, Utah
# Filter rows for Salt Lake County, Utah
# Filter rows for Salt Lake County, Utah
#
# Filter rows for Salt Lake County, Utah
salt_lake_county_data = covid_df[(covid_df['Province_State'] == 'Utah') & (covid_df['Admin2'] == 'Salt Lake')]

# Extract date columns
date_columns = salt_lake_county_data.columns[11:]

# Melt the dataframe to have individual rows for each date
melted_data = salt_lake_county_data.melt(id_vars=['Province_State', 'Admin2'], value_vars=date_columns, var_name='Date', value_name='Cases')

# Convert the 'Date' column to datetime
melted_data['Date'] = pd.to_datetime(melted_data['Date'])

# Calculate running total of cases
melted_data['Running Total'] = melted_data.groupby('Admin2')['Cases'].cumsum()

# Calculate daily new cases
melted_data['Daily New Cases'] = melted_data.groupby('Admin2')['Cases'].diff().fillna(0)

# Plotting
plt.figure(figsize=(12, 6))

# Plot running total on the left y-axis
plt.plot(melted_data['Date'], melted_data['Running Total'], label='Running Total Cases', color='blue')
plt.xlabel('Date')
plt.ylabel('Running Total Cases', color='blue')
plt.tick_params('y', colors='blue')

# Set x-axis locator to show dates at a monthly cadence
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# Rotate x-axis tick labels vertically
plt.xticks(rotation=90)

# Create a second y-axis for daily new cases on the right side
plt.twinx().plot(melted_data['Date'], melted_data['Daily New Cases'], label='Daily New Cases', color='orange')
plt.ylabel('Daily New Cases', color='orange')

# Add a title and legend
plt.title('Running Total and Daily New Cases for Salt Lake County, Utah')
plt.legend()
plt.show()
#%% viz 4
'''
Create a visualization that shows a stacked bar chart of county contributions
to a given state's total cases. You may choose any state (or states).
(https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_stacked.html#sphx-glr-gallery-lines-bars-and-markers-bar-stacked-py)
The graphic should:
-Have a single column delineate a state
-Have each 'slice' or column compontent represent a county
'''
# URL for the COVID-19 time series dataset for confirmed cases in the United States
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
covid_df = pd.read_csv(url, index_col=0)

# Choose the state of interest
selected_state = 'Utah'
state_data = covid_df[covid_df['Province_State'] == selected_state]

# Group data by county in the selected state and calculate total cases for each county
state_county_totals = state_data.groupby('Admin2').sum().reset_index()

# Plotting
plt.figure(figsize=(12, 6))

# Use a vertical stacked bar chart to show county contributions to the total cases in the state
plt.bar('Total Cases', state_county_totals.iloc[:, 11:].sum().sum(), color='white')  # White bar as the background

# Plot each county's contribution stacked on top
bottom = 0
for county in state_county_totals['Admin2']:
    plt.bar('Total Cases', state_county_totals[state_county_totals['Admin2'] == county].iloc[:, 11:].sum().sum(),
            bottom=bottom, label=county)
    bottom += state_county_totals[state_county_totals['Admin2'] == county].iloc[:, 11:].sum().sum()

# Add labels and title
plt.ylabel('Total Cases')
plt.xlabel('County')
plt.title(f'Total COVID-19 Cases by County in {selected_state}')

# Add legend
plt.legend(title='County', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot
plt.show()
#%% extra credit (5 points)
'''
Use Seaborn to create a grouped box plot of all reported states. Each boxplot
should be a distinct state. Have the states ordered from most cases (FL) to fewest 
cases. (https://seaborn.pydata.org/examples/grouped_boxplot.html)
'''
