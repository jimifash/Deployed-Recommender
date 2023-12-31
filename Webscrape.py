from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import re

data = pd.read_csv("Boomplay Scraped songs.csv")
def scrape_boomplay(url):
    # Send an HTTP request to the provided URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Dictionaries for storing data
        song_name = {'song_name': []}
        artist = {'artist_name': []}
        artist_age = {'a_age': []}
        time = {'time': []}

        # Extract song names
        song_data = soup.findAll('div', {'class': 'songNameWrap'})
        index = 1
        while index < 31:
            name = song_data[index].text.replace('\n', '').split('ft.')
            if len(name) >= 2:
                name = name[0]
            else:
                name = name[0]
            song_name['song_name'].append(name)
            index += 1

        # Extract artist names
        artist_data = soup.findAll('a', {'class': 'artistName'})
        i = 0
        while i < 30:
            artist_name = artist_data[i].text
            artist['artist_name'].append(artist_name)
            i += 1

        # Build URLs for artist age search
        age_url = ["https://en.wikipedia.org/wiki/" + i for i in artist['artist_name']]

        # Get and store artist age
        pattern = "[0-9]{4}|[0-9]{2}|[0-9]{2}"
        for j in age_url:
            response1 = requests.get(j)
            try:
                soup1 = BeautifulSoup(response1.content, 'html.parser')
                age_data = soup1.select_one('span span', {'class': 'bday'})
                age = age_data.text if age_data else 'NA'
                if re.search(pattern, age):
                    artist_age['a_age'].append(age)
                else:
                    artist_age['a_age'].append('NA')
            except AttributeError:
                artist_age['a_age'].append('NA')

        # Extract run_time
        time_data = soup.findAll('li', {'class': 'clearfix play_one'})
        for t in range(30):
            time['time'].append(time_data[t].time.text)

        # Create DataFrames
        df = pd.DataFrame({'song_name': song_name['song_name'], 'artist_name': artist['artist_name'],
                           'a_age': artist_age['a_age'], 'time': time['time']})

        # Clean data
        df['a_age'] = pd.to_datetime(df['a_age'], errors='coerce', format='%Y-%m-%d')
        df['age'] = datetime.today().year - df['a_age'].dt.year
        df.rename(columns={'a_age': 'dob'}, inplace=True)
        df2 = data.append(df)
        df2.to_csv("Top_Naija_Music_Trends_Boom_play.csv") #saving the dataframe
        return df2

    else:
        print(f"Error: Unable to retrieve data from {url}")
        return None
     




