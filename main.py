from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

load_dotenv()

#Defined in env file
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

scope = "playlist-modify-private"
# List of tracks to be added
tracks_to_add_list = []

##################### Billboard fetch Start ##########################
date_selection = input("Enter preferred date to fetch top 100 billboards in format (yyyy-mm-dd)")
billboard_url = f"https://www.billboard.com/charts/india-songs-hotw/{date_selection}/"

data = requests.get(billboard_url)

soup = BeautifulSoup(data.text, 'html.parser')

songs_list = []

all_songs = soup.select("li ul li  h3")

for x in all_songs:
    x = x.getText().strip()
    with open("songs.txt", "a") as file:
        file.write(x + "\n")
    file.close()
print(f"Fetched top Billboard songs for the date: {date_selection}")
##################### Billboard fetch End ##########################

#Spotify's connection. pass authorizationd details
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

#Fetch current user id
results = sp.current_user()
user = results['id']

######Create Playlist###############
playlist_name = "Top 25"
playlist_desc ='Top 25 Indian Songs on Billboard'
new_playlist =  sp.user_playlist_create(user, playlist_name, public=False, description=playlist_desc)
print(f"Playlist created:{new_playlist} ")
playlist_id = new_playlist["id"] #Get newly created playlist ID

# Reading the file line by line
with open("songs.txt", "r") as file:
    for x in file:
        x = x.strip()  # strip() removes the newline character
        #######Search track from search quesry provided########
        search_query = x
        track_to_be_added = sp.search(q=search_query, limit=1, offset=0, type='track', market=None)
        track_to_be_added_uri = track_to_be_added["tracks"]["items"][0].get('uri')  # Fetch track id
        tracks_to_add_list.append(track_to_be_added_uri)



# ###### #Add songs to playlist
tracks_added = sp.playlist_add_items(playlist_id, tracks_to_add_list, None)
print(f"Tracks added: {tracks_added}")











