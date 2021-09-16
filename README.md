# Python Music Trivia
Play snippets of songs on Spotify for friends and see who can identify the most!

Generate a file from a Spotify playlist, enter the start point and duration of each song snippet as well as the category, and the app will display them in a grid for easy playback.

## Setup
- [Set up an app](https://developer.spotify.com/dashboard/applications) by logging in to Spotify for developers. Make sure to add `http://localhost` as a Redirect URI in the app settings.
- Export your app's Client ID and Client Secret values and the redirect URI as environment variables.
    ```bash
    export SPOTIPY_CLIENT_ID=<SPOTIFY_CLIENT_ID>
    export SPOTIPY_CLIENT_SECRET=<SPOTIFY_CLIENT_SECRET>
    export SPOTIPY_REDIRECT_URI=http://localhost
    ```
- Install the dependencies with
    ```
    pip install -r requirements.txt
    ```
- [Authenticate the app with your account](https://developer.spotify.com/documentation/general/guides/authorization-guide/) by launching `playlistconverter.py`.
    ```
    python playlistconverter.py
    ```

## `playlistconverter.py` usage
The converter tool will take in a Spotify playlist and create a tab-separated file (`.tsv`) in the format required by the app.
```
$ python playlistconverter.py -h
usage: playlistconverter.py [-h] [--url URL] [--id ID]

Convert a spotify playlist into a csv file for loading into the pyspotify music trivia.

optional arguments:
  -h, --help  show this help message and exit
  --url URL   Full URL to playlist.
  --id ID     Playlist ID. Portion of the URL after the spotify.com/playlist/{COPY_THIS_PORTION}

# With full playlist URL
python playlistconverter.py --url https://open.spotify.com/playlist/37i9dQZF1DX1MUPbVKMgJE

# With playlist ID
python playlistconverter.py --id 37i9dQZF1DX1MUPbVKMgJE
```
The name of the file will be the playlist name in lowercase with spaces replaced by underscores.

### `.tsv` format
|Track ID|Track Name|Snippet Start Point|Snippet Duration|Category|
|--|--|--|--|--|
|Pre-populated from playlist|Pre-populated from playlist|default: `0`|defaults: `3`|defaults to `CATEGORY`|

You only need to update the snippet start point, duration, and category for each track.

Categories are case-sensitive and the app will output each unique one on a different line with the tracks that use it.

## `app.py` usage
The `.tsv` file needs to be in the same directory as `app.py` and passed in as an environment variable with the `flask` command:
```
TSV_FILE=<YOUR_FILE>.tsv flask run
```
The app can then be viewed on `http://localhost:5000`.