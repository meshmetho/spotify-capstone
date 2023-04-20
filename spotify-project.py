import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import csv
# Set up the client ID, client secret, and redirect URI for your application
client_id = ("2162fe68e1034b90aa1be9b6411188d9")
client_secret = ("56c67aa6c8e34cffb2b1d57ad7477277")
redirect_uri = 'http://localhost:8080'
# Authenticate the user's Spotify account credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='playlist-modify-private'))
# Get the user's Spotify username
user = sp.current_user()['id']
# Prompt the user to enter a name for the new playlist
playlist_name = input("Enter a name for the new playlist: ")
# Create the new playlist
playlist = sp.user_playlist_create(user, playlist_name, public=False)
# Prompt the user to enter their preferred genre, artist, or mood
genre = input("Enter your preferred genre: ")
artist = input("Enter your preffered artsist: ")
mood = input("Enter your mood: ")
user_input = genre + artist + mood
# Search for tracks based on the user's input
results = sp.search(q=user_input, type='track', limit=50)
# Add the top 10 tracks to the new playlist
tracks = results['tracks']['items'][:10]
for track in tracks:
    artist_name = track['artists'][0]['name']
    track_name = track['name']
    print(f"{artist_name} - {track_name}")

track_uris = [track['uri'] for track in tracks]
sp.user_playlist_add_tracks(user, playlist['id'], track_uris)
# Confirm that the tracks were added to the playlist
playlist_tracks = sp.playlist_tracks(playlist['id'])
print(f"{len(playlist_tracks['items'])} tracks added to the new playlist!")
#print(playlist_tracks) 


with open("example.csv", mode = "w", encoding = "utf-8", newline ="") as file:
    writer = csv.writer(file)
    writer.writerow(["artist", "track name"])
    for track in tracks:
        artist_name = track['artists'][0]['name']
        track_name = track['name']
        writer.writerow([artist_name, track_name])