#import os
import pandas as pd
from Music_Recommendation import preprocess_and_compute_similarity, recommend
from youtubesearchpython import VideosSearch
import streamlit as st


# Load environment variables
#

df_new, sim = preprocess_and_compute_similarity()
data = df_new
df = pd.DataFrame(data)

# Set your YouTube API key
#key = os.getenv('api_key')

# Set the YouTube API key globally
#VideosSearch(key)

def play_youtube_video(video_id):
    st.video(f"https://www.youtube.com/watch?v={video_id}")

def main():
    st.title("Nigerian Songs Recommendation System")

    # Use st.selectbox for song selection
    st.markdown("### Select a song:")
    selected_song = st.selectbox("", df['song_name'])

    st.subheader("Selected Song Details:")
    selected_song_details = df[df['song_name'] == selected_song]
    st.write(selected_song_details)

    recommendations = recommend(selected_song, df, sim)

    st.subheader("Recommended Songs:")
    if "Song not found" in recommendations:
        st.error("Song not found. Please try another.")
    else:
        # Display recommended songs with a styled layout
        for recommended_song in recommendations:
            st.markdown(f"### {recommended_song}")
            artist = df[df['song_name'] == recommended_song]["artist_name"].iloc[0]

            # Use YouTube API to get video information
            videos_search = VideosSearch(recommended_song + " by " + artist, limit=1)
            results = videos_search.result()
            if results:
                video_id = results['result'][0]['id']
                st.markdown(f"**[Play on YouTube](https://www.youtube.com/watch?v={video_id})**")
                play_youtube_video(video_id)

if __name__ == "__main__":
    main()
