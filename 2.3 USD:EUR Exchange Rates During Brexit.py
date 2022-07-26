#!/usr/bin/env python
# coding: utf-8

# # Storytelling Exchange Rate Data With Visualizations

# We will create visualizations with a dataset that describes Euro daily exchange rates between 1999 and 2021.

# In[1]:


#Import the pandas libraries
import pandas as pd

#read in the euro-daily-hist_1999_2020.csv file into pd 
exchange_rates = pd.read_csv('euro-daily-hist_1999_2020.csv', 
                      encoding = 'Latin-1')
#Inspect the first and the last five rows to understand the structure of the dataset.

exchange_rates.head()


# In[2]:


exchange_rates.tail()


# In[3]:


exchange_rates.info()


# Note we have 40 columns (1 date column and 39 different currency columns). We have no null values and the data type of each column is either object or float. 
# 
# Before we start working further, let's clean the data. 

# In[4]:


exchange_rates.rename(columns={'[US dollar ]': 'US_dollar','Period\\Unit:': 'Time'},
                      inplace=True)
exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])
exchange_rates.sort_values('Time', inplace=True)
exchange_rates.reset_index(drop=True, inplace=True)


# We will isolate Time and US_dollar columns:

# In[5]:


euro_to_dollar = exchange_rates[['Time', 'US_dollar']].copy()
euro_to_dollar['US_dollar'].value_counts()


# Note that there are 62 - characters. This could indicated missing data. Let's delete these rows with this blank data 

# In[6]:


# Here we are selecting rows that don't include - as their value
euro_to_dollar = euro_to_dollar[euro_to_dollar['US_dollar'] != '-']

# Use following syntax to convert US_dollar column to 
# data type float: df['Fee'] = df['Fee'].astype(float)

euro_to_dollar['US_dollar'] = euro_to_dollar['US_dollar'].astype(float)
euro_to_dollar.info()



# Now we have cleaner data. Lets see a graph that relates the eruo and USD:

# In[7]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# Enables Jupyter to display graphs

plt.plot(euro_to_dollar['Time'],
         euro_to_dollar['US_dollar'])
plt.show()


# To make the graph smmoother, we will take a rolling average of exchange rates based on 30 day increments. 
# 

# In[8]:


euro_to_dollar['rolling_mean'] = euro_to_dollar['US_dollar'].rolling(30).mean()
euro_to_dollar


# Let's see the smoother graph now: 
# 

# In[9]:


plt.plot(euro_to_dollar['Time'],
         euro_to_dollar['rolling_mean'])
plt.show()


# Now it's time for us to generate ideas for a storytelling visualization with this data. One idea I had is that you can take a look at exchange rate fluctuations during the significant moments leading up to the Brexit decision. 
# 
# https://en.wikipedia.org/wiki/Timeline_of_Brexit
# 
# Another idea is to look at the effects of the exchange rate during COVID or the '08 financial crisis.
# 
# Let us dive into the Brexit events and tell a data story with it: 

# We will take a look at each year starting the year before (2015) the idea of Brexit
# was introduced through the year after its enactment(2021). 
# 
# Note, even before Brexit was introduced, the UK used the British Pound. They don't use the Euro. However, it would be intersting to see if there is any correlation between this political event and the USD/EUR (EUR being the base currency) exchange rates. 
# 
# Summary of graphs: 
# - 7 graphs 
# - each title will be the year and the subtitle will have a pivotal moment that took place in that year. Of course, the first year and the last year ('15 & '21) won't have any moments that are crucially related. 
# 

# In[10]:


brexit = euro_to_dollar.copy(
                   )[(euro_to_dollar['Time'].dt.year >= 2015) & (euro_to_dollar['Time'].dt.year <= 2021)]
yr_one = brexit.copy(
       )[brexit['Time'].dt.year < 2016]

yr_two = brexit.copy(
       )[(brexit['Time'].dt.year >= 2016) & ((brexit['Time'].dt.year < 2017))]

yr_three = brexit.copy(
       )[(brexit['Time'].dt.year >= 2017) & ((brexit['Time'].dt.year < 2018))]

yr_four = brexit.copy(
       )[(brexit['Time'].dt.year >= 2018) & ((brexit['Time'].dt.year < 2019))]

yr_five = brexit.copy(
       )[(brexit['Time'].dt.year >= 2019) & ((brexit['Time'].dt.year < 2020))]

yr_six = brexit.copy(
       )[(brexit['Time'].dt.year >= 2020) & ((brexit['Time'].dt.year < 2021))]

yr_seven = brexit.copy(
       )[(brexit['Time'].dt.year >= 2021) & ((brexit['Time'].dt.year < 2022))]

years = [yr_one, yr_two, yr_three, yr_four, yr_five, yr_six, yr_seven]


# In[27]:


### Adding the FiveThirtyEight style
import matplotlib.style as style
style.use('fivethirtyeight')

### Adding the subplots
plt.figure(figsize=(24, 17))
ax1 = plt.subplot(4,2,1)
ax2 = plt.subplot(4,2,2)
ax3 = plt.subplot(4,2,3)
ax4 = plt.subplot(4,2,4)
ax5 = plt.subplot(4,2,5)
ax6 = plt.subplot(4,2,6)
ax7 = plt.subplot(4,2,7)


axes = [ax1,ax2,ax3,ax4,ax5,ax6,ax7]
all_years = ['2015: Year Before Brexit Introduced','2016: Brexit Idea Introduced',
             '2017: Article 50 is Invoked',
             '2018: Brexit Withdrawal Agreement Published',
             '2019: Brexit Controversy Battle',
             '2020: Brexit Agreement Passes',
             '2021: Year After UK Withdrawal']
### Changes to all the subplots

for ax in axes: 
    ax.set_ylim(0.8, 1.7)
    ax.set_yticks([1.0, 1.2, 1.4, 1.6])
    ax.set_yticklabels(['1.0', '1.2','1.4', '1.6'], alpha=0.3)
    ax.grid(alpha=0.5)


### Ax: All years
for ax, year, yr in zip(axes, years, all_years):
    ax.plot(year['Time'], year['rolling_mean'],color='#BF5FFF')
    ax.set_xticklabels(['Jan-Mar', '', 'Apr-Jun','', 'Jul-Sept','','Oct-Dec'],alpha=0.3)
    ax.title.set_text(yr)


plt.show()


# Bc this is USD/EUR, any uptrend means the EUR is getting weaker. We can see that during the year Brexit passed, then the EUR got weaker by around 9%. I got 9% by taking the final spot rate from December 31, 2020 and subtracting the initial spot rate from Jan. 1, 2020. The values can be found here: https://www.exchangerates.org.uk/EUR-USD-spot-exchange-rates-history-2020.html
# 

# In[ ]:




