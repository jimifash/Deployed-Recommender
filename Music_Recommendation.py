#!/usr/bin/env python
# coding: utf-8

# # Music Recommendation

# In[2]:


#import libraries

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from Webscrape import scrape_boomplay
#from sqlalchemy import create_engine
#import mysql.connector
#import os
#from dotenv import load_dotenv
#load_dotenv()
#key = os.getenv('PASSWORD')
#host = os.getenv('HOST')
#user = os.getenv('USER')
#db = os.getenv('DB')



#db_config = {
#    'host': host,
 #   'user': user,
  #  'password': key,
   # 'database': db,
#}

# In[3]:
#conn = mysql.connector.connect(**db_config)

#load the scraped and cleaned data
df = scrape_boomplay('https://www.boomplay.com/playlists/26356675?from=home')
#engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")


# Use the connection to execute the query
#query = 'SELECT DISTINCT(song_name),artist_name,a_age,time FROM music.scraped_data'
#df = pd.read_sql_query(query, con=conn)
#df
#df = pd.read_csv("Boomplay Scraped songs.csv")
df = df.drop_duplicates(subset=['song_name'])

# In[4]:


#Copy dataset to avoid tampering with the original
df_new = df.copy()


#convert timestamp to string
df_new['time']=df_new['time'].astype('str')
df_new['a_age']=df_new['a_age'].astype('str')


# In[5]:


#check
df_new.info()


# In[6]:


#Create tags
df_new['tags'] = df_new['song_name']+df_new['artist_name']+df_new['a_age']+df_new['time']
df_new['song_name'] = df_new['song_name'].apply(lambda x:x.strip())
df_new


# In[7]:


#vectorize the tags
cv = CountVectorizer(max_features=5000, stop_words='english')


# In[8]:


#Reducing or stemming words to it's roots
ps = nltk.stem.PorterStemmer()


def stem(obj):
    y = []
    for i in obj.split():
        y.append(ps.stem(i))
    return " ".join(y)


# In[9]:


df_new['tags'] = df_new['tags'].apply(stem)


# In[10]:


vector = cv.fit_transform(df_new['tags']).toarray()
vector


# In[11]:


#finding the cosine similarities in the vector using cosine siimilarities

similarity = cosine_similarity(vector)


# In[25]:


similarity.shape


# In[14]:


#reduce all the song title to lower case
df_new['song_name'] = df_new['song_name'].apply(lambda x:x.lower())


# In[49]:

def recommend(key):
    key = key.lower()
    matching_rows = df_new[df_new['song_name'] == key]
    
    if not matching_rows.empty:
        index = matching_rows.index[0]
        print("Index:", index)
        
        if 0 <= index < min(similarity.shape):
            sim_row = similarity[index]
            print("Similarity Row:", sim_row)

            song_ls = sorted(list(enumerate(sim_row)), reverse=True, key=lambda x: x[1])[1:15]

            recommended_songs = [df_new.iloc[i[0]].song_name for i in song_ls]
            return recommended_songs
        else:
            print("Index out of bounds:", index)
            return ["Song not found"] 
    else:
        return ["Song not found"]

