import os

import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

"""Client ID and Client Secret have been stored as environment variables for security 
and privacy. They can be obtained from spotify by creating an account, heading to the 
developer console and creating a new app."""

user_input = input("Which year do you want to travel to? Enter the year in this format YYYY-MM-DD:\n")
year = user_input.split("-")[0]
spotify_base_url = "https://api.spotify.com/v1"
redirect_url = "http://example.com"
print(user_input)
url = f"https://www.billboard.com/charts/hot-100/{user_input}/"

response = requests.get(url = url).text
soup = BeautifulSoup(response, "html.parser")

# Using bs4 to scrap the top 100 songs data from the billboard site

artists = soup.find_all(name = "span",
                        class_ = "c-label a-no-trucate a-font-primary-s lrv-u-font-size"
                                 "-14@mobile-max u-line-height-normal@mobile-max u-letter"
                                 "-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line"
                                 " u-max-width-330 u-max-width-230@tablet-only")
song_artists = [name.get_text().split("\n\t\n\t")[1].split("\n")[0] for name in artists if name is not None]
titles = soup.find_all(name = "h3",
                       class_ = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing"
                                "-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height"
                                "-125 u-line-height-normal@mobile-max a-truncate-ellipsis "
                                "u-max-width-330 u-max-width-230@tablet-only")
song_titles = [title.get_text().split("\t")[9] for title in titles if title is not None]
# print(len(song_titles))
# print(len(song_artists))

# Saving the gotten songs to a local text file

with open(file = "top_songs.txt", mode = "w", encoding = "utf-8") as file:
    try:
        for idx in range(0, 99):
            file.write(f"{song_titles[idx]} by {song_artists[idx]}\n")
    except IndexError:
        print("There was an Index Error out of range")

# --------------------------------SPOTIPY--------------------------------------

OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
scope = "playlist-modify-private"

# Creating spotipy auth user object

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        scope = "playlist-modify-private",
        redirect_uri = redirect_url,
        client_id = os.environ.get("SPOTIFY_CLIENT_ID"),
        client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET"),
        show_dialog = True,
        cache_path = "token.txt"
    )
)

# Get user ID

user_id = sp.current_user()["id"]
print(user_id)
song_urls = []

# Get song url by parsing song details in our text file to the search function
# of the spotipy library

with open(file = "top_songs.txt", mode = "r") as file:
    all_songs = file.readlines()

for song in all_songs:
    music_title = song.split(" by ")[0]
    music_artiste = song.split(" by ")[1]

    result = sp.search(q = f"track:{music_title} artist:{music_artiste}", type = "track", limit = 1)
    try:
        url = result["tracks"]['items'][0]['external_urls']['spotify']
        song_urls.append(url)
        print(f"{music_title} by {music_artiste} will be added to your playlist")
    except IndexError:
        print(f"{music_title} by {music_artiste} does not exist in spotify. Skipped")
        continue

# Create Playlist

playlist = sp.user_playlist_create(
    user = user_id,
    name = f"{user_input} Billboard Hot 100",
    public = False,
    collaborative = False,
    description = "Playlist created through python code",
)
playlist_id = playlist['id']

# Add all songs to the created playlist using all their song urls

sp.playlist_add_items(
    playlist_id = playlist_id,
    items = song_urls
)
