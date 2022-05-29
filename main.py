from spotify import *

from song import *

"""Client ID and Client Secret have been stored as environment variables for security 
and privacy. They can be obtained from spotify by creating an account, heading to the 
developer console and creating a new app."""

user_input = get_user_input()
soup = get_soup()
song_details = get_top_songs(soup)
save_top_songs(song_artists = song_details[0], song_titles = song_details[1], date = user_input)
create_spotify_user()
get_song_url(date = user_input)
playlist_id = create_playlist(date = user_input)
populate_spotify_playlist(playlist_id)
