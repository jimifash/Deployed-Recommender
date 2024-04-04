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
def preprocess_and_compute_similarity(playlist_url='https://www.boomplay.com/playlists/26356675?from=home'):
    # Scrape Boomplay playlist data
    df = scrape_boomplay(playlist_url)
    
    # Drop duplicate song entries
    df = df.drop_duplicates(subset=['song_name'])
    df.reset_index(drop=True, inplace=True)
    
    # Copy dataset to avoid tampering with the original
    df_new = df.copy()
    
    # Convert timestamp and artist age to string
    df_new['time'] = df_new['time'].astype(str)
    df_new['a_age'] = df_new['a_age'].astype(str)
    
    # Create tags
    df_new['tags'] = df_new['song_name'] + df_new['artist_name'] + df_new['a_age'] + df_new['time']
    df_new['song_name'] = df_new['song_name'].apply(lambda x: x.strip())
    
    # Vectorize the tags
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(df_new['tags']).toarray()
    
    # Reduce words to their roots
    ps = nltk.stem.PorterStemmer()

    def stem(obj):
        y = []
        for i in obj.split():
            y.append(ps.stem(i))
        return " ".join(y)

    df_new['tags'] = df_new['tags'].apply(stem)
    
    # Compute cosine similarities
    similarity = cosine_similarity(vector)
    
    # Convert song names to lowercase
    df_new['song_name'] = df_new['song_name'].apply(lambda x: x.lower())
    
    return df_new, similarity

def recommend(key, df):
    key_lower = key.lower()
    matching_rows = df[df['song_name'].str.lower() == key_lower]
    
    if not matching_rows.empty:
        index = matching_rows.index[0]
        print("Index:", index)
            
        if 0 <= index < similarity.shape[0]:
            sim_row = similarity[index]
            print("Similarity Row:", sim_row)

            song_ls = sorted(list(enumerate(sim_row)), reverse=True, key=lambda x: x[1])[0:15]
            recommended_songs = [df.iloc[i[0]].song_name for i in song_ls]
            return recommended_songs
        else:
            print("Index out of bounds:", index)
            return ["Song not found"]
    else:
        return ["Song not found"]


