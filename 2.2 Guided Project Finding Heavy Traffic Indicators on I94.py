#!/usr/bin/env python
# coding: utf-8

# # Visualizing I-94 Interstate Highway Traffic

# Below, we will use data and data visualization tools in order to determine indicators/reasons of heavy traffic on the I-94 Interstate highway. We will be looking at the westbound traffic.

# In[1]:


#Import the pandas libraries
import pandas as pd

#read in the Metro_Interstate_Traffic_Volume.csv file into pd 
traffic = pd.read_csv('Metro_Interstate_Traffic_Volume.csv', 
                      encoding = 'Latin-1')


# In[2]:


# Examine the first and the last five rows.Note 
# when you put nothing in parentheses, this implies 5.

print(traffic.head())
print("\n")
print(traffic.tail())


# For more general information, we use the followoing: 

# In[3]:


'''An important thing to note is the 
date range that this data has been recorded: 
October 2, 2012 to Sept. 30, 2018'''

traffic.info()


# All of the data we are using only involves westbound 
# traffic for the entire project.

# In[4]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# We will plot a histogram using Pandas to get the distribution of the traffic_volume: 

# In[5]:


traffic["traffic_volume"].plot.hist()
plt.title("Traffic Volume")
plt.xlabel("Number of Cars")
plt.show()


# Note the bimodial distrubtion. 

# In[6]:


#we want to find stats about the volume: 

traffic['traffic_volume'].describe()


# Over the recording's time horizon, hourly traffic volume varied from 0 to 7,280 cars. On avg, 3260 (rounded) cars would pass by the data recording station per hour.
# 
# Around 75% of the time, 4933 cars with pass by per hour on average. This is where the bulk of the traffic lies. As we can see, 25% of the time 1193 cars would pass by on average per hour. This could be during low traffic times. Most likely at night 

#  let's delve deeper by subdividing the data set into two subsets. We will divide nighttime (7pm to 7am) and daytime data (7am - 7pm). 

# In[7]:


traffic['date_time'] = pd.to_datetime(traffic['date_time'])

day = traffic.copy()[(traffic['date_time'].dt.hour >= 7) & (traffic['date_time'].dt.hour < 19)]
print(day.shape)

nighttime = traffic.copy()[(traffic['date_time'].dt.hour >= 19) | (traffic['date_time'].dt.hour < 7)]
print(nighttime.shape)


# Note: 23,877 refers to rows and 9 refers to number of columns, for example. There are more recorded rows in the daytime because, as we can see it from the data, there are missing data points for nighttime data.   

# Now we're going to compare the traffic volume at night and during day.
# 

# First, we will plot both day and night histograms side by side.

# In[8]:


plt.figure(figsize=(10,3)) #setting the size of the graph
# 10 refers to horizonatl size and 3 refers to vertical box size

#Now we tell the compiler that we have 1 of 2 graphs 
#the figure has 1 row, 2 columns, and this plot is the first plot
plt.subplot(1, 2, 1)

#plot one: 
plt.hist(day['traffic_volume'])

#we scale x and y to the same ranges 
plt.xlim(-100, 7500)
plt.ylim(0, 8000)

#title, x and y labels
plt.title('Traffic Volume: Day')
plt.ylabel('Frequency')
plt.xlabel('Traffic Volume')

#similarly for the second graph 

plt.subplot(1, 2, 2)

plt.hist(nighttime['traffic_volume'])

plt.xlim(-100, 7500)
plt.ylim(0, 8000)


plt.title('Traffic Volume: Night')
plt.ylabel('Frequency')
plt.xlabel('Traffic Volume')

plt.show()


# We will Use Series.describe() to look up a few statistics
# for traffic_volume for both day and night.

# In[9]:


day['traffic_volume'].describe() 


# In[10]:


nighttime['traffic_volume'].describe() 


# daytime notes
# - graph is left skewed
# - Dist. looks more normal
# - Traffic volumes are higher during the day since it is left skewed
# - 25% of the values are less than 4252 
# - 50% of the values are less than 4820 
# - 75% of the values are less than 5559 but more than 4252 
# (75% of values lie in the range: (4252,5559))
# 
# nighttime notes 
# - graph is right skewed 
# - most traffic frequency values are lower compared to daytime, which makes sense 
# - 75% of the time the amount of cars I would pass the station on average per hour will be less than 2819 but greater than the 25% value of 530 

# In[11]:


day['month'] = day['date_time'].dt.month
by_month = day.groupby('month').mean()
by_month['traffic_volume']


# In[12]:


plt.plot(by_month['traffic_volume'])
plt.xlabel('month')
plt.ylabel('Traffic Volume')


# Daytime traffic tends to free up during the winter months. However, during July there's a massive dip in traffic. This could be due to a lack of data recording. It doesnt make sense for there to be a drastic down-spike. Another possiblity could be that there was heavy road construction. 

# In[13]:


#Now let's look at how the traffic change on 
# average on each day of the week 

day['dayofweek'] = day['date_time'].dt.dayofweek
by_dayofweek = day.groupby('dayofweek').mean()
by_dayofweek['traffic_volume']  # 0 is Monday, 6 is Sunday


# In[14]:


plt.plot(by_dayofweek['traffic_volume'])
plt.xlabel('Day')
plt.ylabel('Traffic Volume')


#  it seems as though on the fifth and the sixth day, which is Saturday and Sunday, respectively, the traffic subsides heavily. traffic is not as busy as Tuesday through Friday. 

# We'll now generate a line plot for the time of day. The weekends, however, will drag down the average values, so we're going to look at the averages separately. To do that, we'll start by splitting the data based on the day type: business day or weekend.
# 

# In[15]:


day['hour'] = day['date_time'].dt.hour
business_days = day.copy()[day['dayofweek'] <= 4] #4 is a Friday
weekend = day.copy()[day['dayofweek'] >=5] # 5 is Saturday

by_hour_business = business_days.groupby('hour').mean()
by_hour_weekend = weekend.groupby('hour').mean()

print(by_hour_business['traffic_volume'])
print(by_hour_weekend['traffic_volume'])


# Remember we are only looking at daytime traffic. Which is why we see the seventh hour is the first option we have. And this goes up to the 18th hour of the day, which is 7 PM
#  

# In[16]:


plt.plot(by_hour_business['traffic_volume'], label = "Traffic Vol. by hour: Weekday")
plt.plot(by_hour_weekend['traffic_volume'], label = "Traffic Vol. by hour: Weekend")

plt.xlabel("Hour of Day")
plt.ylabel("Volume")

plt.legend()
plt.show()


#  on weekdays, as you can see from the blue line, rush-hour traffic happens between the hours of 7 AM and 10 AM. It dies down a little bit and then it starts ramping up from  PM till around 6 PM. 
#  
#  On weekends, we see something a little bit different. Traffic does not ramp up until around 12 PM. The traffic than continues to stay consistent until 4 PM Then it starts to die down again. 
#  
#  
#  And all, we have taken a look at traffic volume by weekday and weekend. We looked specifically at the hour of the day, the day of the week, and the month of the year. In general traffic is heavier on business days, during the warmer months, and that the 7 AM and 4 PM rush hours during those business days. 

# Looking at weather can be a useful tool to help predict traffic. The dataset provides us with columns about weather: temp, rain_1h, snow_1h, clouds_all, weather_main, weather_description.
# 
#  First we will find the correlation between volume of traffic and the above stated weather-related columns.
#  
# 

# In[17]:


day.corr()['traffic_volume']


# The strongest correlation is W/ temperature 

# In[18]:


plt.scatter( day['traffic_volume'], day['temp']) 

# You could also write the above code like:
#     day.plot.scatter('traffic_volume', 'temp') 
plt.ylim(230, 320) # two wrong 0K temperatures mess up the y-axis
plt.xlim(0, 7500)
plt.ylim(230, 320)
plt.show()


# Temp is not a reliable indicator because at a certain temperature, there are so many outcomes of traffic congestion. Use another indicator to be more helpful 

# We can expect a similar issue to happen when comparing with other columns.

# Now, we will look at the categorical weather-related columns: weather_main and weather_description and find the average traffic volume associated with each unique value in these two columns.

# In[19]:


by_weather_main = day.groupby('weather_main').mean()
by_weather_description = day.groupby('weather_description').mean()


# In[21]:


#looking at a relationship with weather main: 


plt.barh(by_weather_main.index, by_weather_main["traffic_volume"])
plt.xlabel("Traffic Volume")
plt.ylabel("Weather Main Condition")
plt.title("Weather Main vs Traffic Volume")
plt.show()


# In[ ]:





#  no relation of traffic volume and weatherman has you'll do it traffic congestion greater than 5000. Using main weather categorization may not be the most efficient way to understand traffic congestion reasons. 
#  
#  
#  Let's try using weather description and seeing if there is a significant relationship with that:

# In[23]:


#looking at a relationship with weathe Description: 

plt.figure(figsize=(10,12))
plt.barh(by_weather_description.index, by_weather_description["traffic_volume"])
plt.xlabel("Traffic Volume")
plt.ylabel("Weather Description")
plt.title("Weather Description vs Traffic Volume")
plt.show()


#  here we see that light rain and snow and showers of snow yield the biggest traffic congestion over 5000 cars per hour. Also the proximity of thunderstorms What's a drizzle can lead to more congestion. Of course, the closer you are, the more Congested the road becomes 

#  in this project, the main indicators we focused on wartime indicators and weather indicators. There are certain time zone congestion is high. Likewise, there are certain weather patterns that are correlated with high traffic congestion. This tells us there's not only one answer that we can find which explains the reason for traffic congestion. Traffic congestion, so it seems, is spurred about due to a combination of factors.
