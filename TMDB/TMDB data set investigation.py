
# coding: utf-8

# 
# #  'tmdb-movies' data set investigation
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction

# In[62]:


# import statements for all of the packages planned to be used.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# ### General Properties

# In[63]:


# Load data and print out a few lines. Perform operations to 
#inspect data types and look for instances of missing or possibly errant data.
df = pd.read_csv("E:/Udacity/project 3/tmdb-movies.csv")
                 
#Data representation
df.head()


# In[64]:


#View the dimensions of data frame to know the size
df.shape


# In[65]:


#Investigate the data types of columns
df.dtypes


# In[66]:


#Summary of data frame including an initial investigation for the NAN values
df.info()


# In[67]:


#show the exact number of NAN values
df.isnull().sum()


# In[68]:


#show the duplicated rows
df.duplicated().sum()


# In[69]:


#show some statistical analysis
df.describe()


# <a id='ask_result'></a>
# By this time i know the questions to ask.
# ### 1- Ask questions:
# >1- Which genres are most popular from year to year? 
# >
# >2- Which are the production companies with most productions?
# >
# >3- Are movies with high budget successful?
# 
# **Bad Columns with lots of NANs:** homepage, tagline, keywords

# ### Gather Data

# In[70]:


#Selected columns are :[id, popularity, budget, original_title, cast, director,
# runtime, genres, production_companies, vote_count, vote_average, release_year]
# There are two ways to do this either drop columns or choose columns ----> I chose to drop columns and add it to clean_df
clean_df = df.drop(['imdb_id', 'homepage','tagline','keywords','overview','release_date','budget_adj','revenue_adj'], axis=1)
clean_df


# ### Clean Data
# ### The important question to answer is: Is the NAN values the only missing data ?

# In[71]:


clean_df.hist(figsize=(15,15));


# In[72]:


clean_df[clean_df.production_companies.isnull()].hist(figsize=(15,15));


# In[73]:


# Check for the NAN count before cleaning
clean_df.isnull().sum()


# In[74]:


#Inspect the dataframe with '0'
#clean_df[clean_df.revenue==0]


# In[75]:


#this will clear rows with '0'
#clean_df = clean_df[clean_df.budget != 0]
#clean_df = clean_df[clean_df.revenue != 0]


# In[76]:


(clean_df.revenue==0).sum(),(clean_df.budget==0).sum()


# ### Dealing with missing values:
# production_companies column alone has 1030 missing values but since its a string we can't fill it with a mean value.
# 
# Best way to deal with this is to eliminate the rows with missing values, since the dataset is big this will applicable.
# 
# Similar to columns: cast, director, genres they have less missing values with respect to production_companies
# 
# We need to make assumption:
# 
#             budget revenue -> result
#              0       0     -> movie not out yet
#              0       value -> missing value 
#              value   0     -> maybe movie not out yet ? missing data?
# Is the best practice to drop all the '0's value ? with consideration that if you drop it will drop 6000 row !
#              

# In[77]:


# Drop NAN rows
clean_df.dropna(inplace= True)


# In[78]:


# Check for the NAN count after cleaning
clean_df.isnull().sum()


# In[79]:


# Check for duplicates
clean_df.duplicated().sum()


# In[80]:


# Drop 1 duplicated row
clean_df.drop_duplicates(inplace= True)


# ### Assess Data

# In[81]:


# Check if there is any column needs to change its data type
clean_df.dtypes


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# ### Research Question 1: Which genres are most popular from year to year?

# In[82]:


#Get the unique years
unique_years = clean_df['release_year'].value_counts().index.values
unique_years


# #### Get the most popular genres based on released year ( Column genres depending on released year)

# In[83]:


# Take a subset from the whole data
small_df = clean_df[['release_year','genres']]

# Group by 'release_year' column -> aggregate the output (genres) with index [0] of value_counts() function
# which returns the most frequent (genres) based on this year grouped by it
year_genres_df = small_df.groupby(['release_year']).agg(lambda x:x.value_counts().index[0])

# Add column with the count of repeatition of the most frequent genre per year
year_genres_df['count'] = small_df.groupby(['release_year']).agg(lambda x:x.value_counts()[0])

# Display the result
year_genres_df


# Now we have the answer for the first question move on to the second question

# ### Research Question 2: Which are the production companies with most productions?

# In[84]:


# Get the count of unique values in production_companies column.
unique_production_companies=(clean_df['production_companies'].value_counts())

# Filter only those company with more than 10 productions
unique_production_companies=unique_production_companies[unique_production_companies>=10]

# Show result
unique_production_companies


# <a id='conclusions'></a>
# ## Conclusions
# 

# ### First question findings more clear through this visualization

# In[85]:


y = year_genres_df['count'].tail(15)
names_genres = year_genres_df['genres'].tail(15)
N = len(y)
x = range(N)
width = 0.7
plt.bar(x, y, width, color="blue",align='edge')
plt.xticks(x,names_genres,rotation='vertical')
plt.subplots_adjust(bottom=0.15)
plt.xlabel('top genres from 2001:2015')
plt.ylabel('Repetition count');


# We can see that Drama genre is most frequent obviously in the last years from 2001:2015 with large amount of movies in 2014.

# ### Second question findings more clear through this visualization

# In[86]:


y = unique_production_companies.head(15)
names_production = (clean_df["production_companies"].value_counts()>10).index.values
N = len(y)
x = range(N)
width = 0.7
plt.bar(x, y, width, color="blue",align='edge')
plt.xticks(x,names_production,rotation='vertical')
plt.subplots_adjust(bottom=0.15)
plt.xlabel('Production Companies')
plt.ylabel('Number Of Movies');


# ### The third question
# #### Are movies with high budget successful?
# 
# Check for there any correlation between budget & revenue to continue with the analysis (if they aren't correlated we can't answer this question).

# In[87]:


# Correlation function
corr = clean_df.corr()


# In[88]:


# Beautiful seaborn heat map
sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns);


# ### What is most important is to get insights from this graph is that we can see:
# 
# budget -> revenue (correlated)
# 
# So that we can in the future improve this analysis to answer more questions about this.
# 

# ### Set the small_df we work on to compare budget - revenue

# In[89]:


small_df = clean_df[['budget','revenue']]

#Sort based on revenue
small_df.sort_values('revenue')

#Set the index as movie name
small_df.index=clean_df['original_title']
small_df


# ### We will be working on top 10 movies both in successful & failed

# In[90]:


#Successful movies are those whose revenue >= budget
success_movies = small_df[small_df.revenue>=small_df.budget].head(10)

#Failed movies are those whose revenue < budget
#Since the question for '0' values is ambigous lets just neglect columns with '0' values
fail_movies = small_df[small_df.revenue<small_df.budget]
fail_movies = fail_movies[fail_movies.revenue != 0]
fail_movies = fail_movies.head(10)

#Make sure that the sum of both of them equals total count
success_movies.count() + fail_movies.count() == small_df.count()
success_movies


# In[91]:


fail_movies


# In[92]:


success_movies.plot.bar(rot='vertical')
plt.subplots_adjust(bottom=0.15)
plt.xlabel('Movies')
plt.ylabel('Budget/Revenue');


# In[93]:


ax = fail_movies.plot.bar(rot='vertical')
plt.subplots_adjust(bottom=0.15)
plt.xlabel('Movies')
plt.ylabel('Budget/Revenue');


# ### The result of this analysis is sufficient to say that when the budget is high the movie will succeed ?
# 
# The answer is no because there is a movie with high budget but it failed in the end so the budget alone can not determine if the movie will succeed or not. 
