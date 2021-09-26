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
- Install the dependencies.
    ```
    pip install -r requirements.txt
    ```
- [Authenticate the app with your account](https://developer.spotify.com/documentation/general/guides/authorization-guide/) by launching `playlistconverter.py`.
    ```
    python playlistconverter.py
    ```

## `playlistconverter.py` usage
The converter tool will take in a Spotify playlist (full URL or ID) and create two tab-separated (`.tsv`) files: a track info file formatted for the web app and an answer file that can be loaded into a spreadsheet editor (Excel, Google Sheets, etc.) for tracking player points.
```
$ python playlistconverter.py -h
usage: playlistconverter.py [-h] [--url URL] [--id ID] [--shuffle] [--gametype {songartist,lyric,connection}]

Convert a spotify playlist into a tsv file (tab-separated) for loading into the pyspotify music trivia.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Full URL to playlist.
  --id ID               Playlist ID. Portion of the URL after the spotify.com/playlist/{COPY_THIS_PORTION}
  --shuffle             (Optional) Shuffle the order of the tracks in the output file. Add it to shuffle tracks, omit it to maintain
                        playlist track order.
  --gametype {songartist,lyric,connection}
                        (Optional) Change the game type. Modifies the generated answer file to include extra columns for different  
                        game play types: guess the song/artist, finish the lyric, or guess the connection between clues in a        
                        category. Defaults to songartist if omitted.

# With full playlist URL
python playlistconverter.py --url https://open.spotify.com/playlist/37i9dQZF1DX1MUPbVKMgJE

# With playlist ID
python playlistconverter.py --id 37i9dQZF1DX1MUPbVKMgJE

# With playlist ID, shuffle order, and change to lyric game type
python playlistconverter.py --id 37i9dQZF1DX1MUPbVKMgJE --shuffle --gametype lyric
```
The name of the file will be the playlist name in lowercase with spaces replaced by underscores.

### `<playlist_name>.tsv` format
|Track ID|Track Name|Snippet Start Point|Snippet Duration|Category|
|--|--|--|--|--|
|Pre-populated from playlist|Pre-populated from playlist|default: `0`|defaults: `3`|default: `CATEGORY`|

You only need to update the snippet start point, duration, and category for each track.

Categories are case-sensitive and the app will output each unique one on a different line with the tracks that use it.

### `<playlist_name>_answers.tsv` format
A convenience file if you want to track player's points. Import it into a spreadsheet editor, add/delete columns for players as necessary, and replace the default values below for easier answer tracking if using the `lyric` or `connection` game types.

*Default (`songartist`) game type format*
|Clue Number|Track Name|Artist|Player 1 Points|Player 2 Points|Player 3 Points|
|--|--|--|--|--|--|
|Pre-populated from playlist|Pre-populated from playlist|Pre-populated from playlist|default: empty|default: empty|default: empty|

*`lyric` game type format*
|Clue Number|Track Name|Artist|Lyric|Player 1 Points|Player 2 Points|Player 3 Points|
|--|--|--|--|--|--|--|
|Pre-populated from playlist|Pre-populated from playlist|Pre-populated from playlist|default: `REPLACE_WITH_LYRIC`|default: empty|default: empty|default: empty|

*`connection` game type format*
|Clue Number|Track Name|Artist|Connection|Player 1 Points|Player 2 Points|Player 3 Points|
|--|--|--|--|--|--|--|
|Pre-populated from playlist|Pre-populated from playlist|Pre-populated from playlist|default: `REPLACE_WITH_CLUE_CONNECTION`|default: empty|default: empty|default: empty|

## `app.py` usage
The `.tsv` file needs to be passed in as an environment variable with the `flask` command>
```
TSV_FILE=<YOUR_FILE>.tsv flask run
```
The web app can then be viewed on [`http://localhost:5000`](http://localhost:5000).

The track info `.tsv` file can be pathed to if it's not in the same directory as `app.py`.
```
TSV_FILE=examples/mix1.tsv flask run

TSV_FILE=../mix1.tsv flask run
```

## Gameplay
As the host:
- Run the webapp with the instructions above in one browser tab.
- Launch Spotify in another browser tab or device.
- Open the answers file in your spreadsheet editor to keep track of points if you want.
- Open a video call with Zoom, Google Meet, etc. and share your computer screen and audio ([Zoom instructions](https://support.zoom.us/hc/en-us/articles/201362643-Sharing-computer-sound-during-screen-sharing)).
- Host a buzzer room on [Cosmobuzz](https://www.cosmobuzz.net/#/host) and share the room code with the players.
- Play clues either randomly or by letting players choose.

As a player:
- Connect to the host's video call.
- Connect to the host's [Cosmobuzz](https://www.cosmobuzz.net/#/play) room with the room code and your name.


### Using Cosmobuzz
- Each player in the room gets a buzzer button to click and a text field to enter answers.
- As a host, remember to click the `Reset Buzzers` and `Clear text entrys` after each clue/set of clues. 
- As a host, lock the players' buzzers while the clues are playing and then unlock them when you want everyone to answer.
- As a host, enable `Only first Buzz` if you want only the fastest player to be able to answer.
- As a host, disable `Only first Buzz` to let every player answer and use the buzz order to determine who gets points for that clue/set of clues or award points to all players with the correct answer.