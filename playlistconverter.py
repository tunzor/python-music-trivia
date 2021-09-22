import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
import random
import argparse
from urllib.parse import urlparse
import sys
import json

try:
    scope = "user-read-playback-state,user-modify-playback-state"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
except:
    print("Did you set up your Spotify credentials as environment variables?\nhttps://developer.spotify.com/documentation/general/guides/app-settings/")
    sys.exit()

parser = argparse.ArgumentParser(description='Convert a spotify playlist into a tsv file (tab-separated) for loading into the pyspotify music trivia.')
parser.add_argument('--url', help="Full URL to playlist.", type=str)
parser.add_argument('--id', help="Playlist ID. Portion of the URL after the spotify.com/playlist/{COPY_THIS_PORTION}", type=str)
parser.add_argument('--shuffle', help="(Optional) Shuffle the order of the tracks in the output file. Add it to shuffle tracks, omit it to maintain playlist track order.", required=False, action="store_true")
parser.add_argument('--gametype', help="(Optional) Change the game type. Modifies the generated answer file to include extra columns for different game play types: guess the song/artist, finish the lyric, or guess the connection between clues in a category. Defaults to songartist if omitted.", required=False, type=str, choices=['songartist','lyric','connection'], default='songartist')
args = parser.parse_args()

spotify_url_prefix = "https://open.spotify.com/playlist"
playlist_id = ""

if args.url == None and args.id == None:
    print("No playlist ID or URL provided.\nPlease pass either the full playlist URL with [--url PLAYLIST_URL] or the ID with [--id PLAYLIST_ID].")
    sys.exit()

if args.url != None:
    if spotify_url_prefix not in args.url:
        print(f"That URL doesn't look right.\nMake sure you provide the full URL, it should start with {spotify_url_prefix}")
        sys.exit()
    path = urlparse(args.url).path
    playlist_id = path.split("playlist/")[1]
elif args.id != None:
    playlist_id = args.id

print(f"Playlist ID: {playlist_id}\n")

try:
    playlist_info = sp.playlist(playlist_id)
except:
    print("Something went wrong when trying to retrieve that playlist.\nDouble check the provided URL or ID.")
    sys.exit()

print(f"Playlist name: {playlist_info['name']}")
print(f"{playlist_info['tracks']['total']} total track(s):")
tracks = []
for track in playlist_info['tracks']['items']:
    name = track['track']['name']
    artist = track['track']['artists'][0]['name']
    id = track['track']['id']
    print(f"{name} by {artist} (id: {id})")
    tracks.append([id, name, artist])

playlist_renamed = playlist_info['name'].lower().replace(" ", "_")
playlist_answers = playlist_info['name'].lower().replace(" ", "_") + "_answers"

if args.shuffle:
    random.shuffle(tracks)

with open(f"{playlist_renamed}.tsv", 'w', encoding='utf-8') as f:
    for t in tracks:
        f.write(f"{t[0]}\t{t[1]}\t{t[2]}\t0\t3\tCATEGORY")
        f.write("\n")

print(f"\nSuccessfully wrote track info file to [{playlist_renamed}.tsv] with default start point of 0 seconds and default duration of 3 seconds.\n\nReplace each 0 with the point where you'd like the snippet to start playing (start point) and the each 3 with how long you'd like the snippet to play for from that start point (duration).")

with open(f"{playlist_answers}.tsv", 'w', encoding='utf-8') as f:
    if args.gametype == "songartist":
        f.write("Clue\tName\tArtist\tPlayer 1 Points\tPlayer 2 Points\tPlayer 3 Points")
        f.write("\n")
        for idx, t in enumerate(tracks):
            # Index, song name, artist name
            f.write(f"{idx + 1}\t{t[1]}\t{t[2]}")
            f.write("\n")
    elif args.gametype == "lyric":
        f.write("Clue\tName\tArtist\tLyric\tPlayer 1 Points\tPlayer 2 Points\tPlayer 3 Points")
        f.write("\n")
        for idx, t in enumerate(tracks):
            # Index, song name, artist name
            f.write(f"{idx + 1}\t{t[1]}\t{t[2]}\tREPLACE_WITH_LYRIC")
            f.write("\n")
    elif args.gametype == "connection":
        f.write("Clue\tName\tArtist\tConnection\tPlayer 1 Points\tPlayer 2 Points\tPlayer 3 Points")
        f.write("\n")
        for idx, t in enumerate(tracks):
            # Index, song name, artist name
            f.write(f"{idx + 1}\t{t[1]}\t{t[2]}\tREPLACE_WITH_CLUE_CONNECTION")
            f.write("\n")

print(f"\n\nSuccessfully wrote answer file to [{playlist_answers}.tsv].\n\nOpen it in a spreadsheet editor to keep track of how many points each player gets for each clue. Add more player columns as necessary.")
if args.gametype == 'lyric' or args.gametype == 'connection':
    print(f"Be sure to replace the default REPLACE_WITH_LYRIC or REPLACE_WITH_CLUE_CONNECTION values with the correct answers for easier answer tracking.")