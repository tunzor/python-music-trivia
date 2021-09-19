import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
import random
import argparse
import os
import csv
import sys
from pathlib import Path

from flask import Flask, redirect

app = Flask(__name__)

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

tracks = []
current_track = ""

tsv_file = open(os.environ.get("TSV_FILE"))
playlist_title = Path(os.path.basename(tsv_file.name)).stem
tsv_reader = csv.reader(tsv_file, delimiter="\t")
tsv_clues = []

for row in tsv_reader:
    tsv_clues.append(row)

unique_cats = []
for track in tsv_clues:
    if track[5] not in unique_cats:
        unique_cats.append(track[5])

# Not used by might be useful later
clues_by_cat = {} 
for clue in tsv_clues:
    if clue[5] in clues_by_cat:
        clues_by_cat[clue[5]].append(clue)
    else:
        clues_by_cat[clue[5]] = []
        clues_by_cat[clue[5]].append(clue)

max_cat_length = 0
for cat in clues_by_cat:
    if len(clues_by_cat[cat]) > max_cat_length:
        max_cat_length = len(clues_by_cat[cat])

def get_playlist_tracks(playlist_id):
    pl_id = f"spotify:playlist:{playlist_id}"
    offset = 0

    while True:
        response = sp.playlist_items(pl_id,
                                    offset=offset,
                                    fields='items.track.id,total',
                                    additional_types=['track'])
        
        if len(response['items']) == 0:
            break
        
        for t in response['items']:
            # print(t['track']['id'])
            tracks.append(t['track']['id'])

        # pprint(response['items'])
        offset = offset + len(response['items'])
        print(f"{response['total']} total tracks in the playlist")

def play_track_for_x_time(track, time, start_point=-1):
    # in seconds
    playback_length = int(time)
    start_point = int(start_point)
    info = sp.track(track)
    # TODO: Print artist
    print(f"Playing {info['name']} from {start_point} seconds for {time} seconds")
    current_track = f"Playing {info['name']}"
    track_length = info['duration_ms']
    if start_point == -1:
        start = random.randint(0, track_length-playback_length*1000)
    else:
        start = start_point

    # Shows playing devices
    res = sp.devices()

    # Change track
    
    try:
        sp.start_playback(uris=[f'spotify:track:{track}'], position_ms=start*1000)
    except:
        print("No devices found.\nMake sure to open Spotify in your browser or on your phone before starting.")
        sys.exit()
    
    sleep(playback_length)
    sp.pause_playback()

def generate_html():
    output = ""
    for cat in unique_cats:  
        it = 1
        output += "<tr>"
        output += "<td>" + cat + "</td>"
        for track in tsv_clues:
            if track[5] == cat:
                output += f"""
                    <td id="clue{it}"><a onclick="toggleView('clue{it}')" href="/shuffleplay/{it}">Clue {it}</a>
                """
            it += 1
        output += "</tr>"

    # output = ""
    # output += "<tr>"
    # for cat in unique_cats:
    #     output += "<td>" + cat + "</td>"

    # for cat in unique_cats:
    #     track_list = clues_by_cat[cat]
    #     for i in range(0,max_cat_length):
    #         pass

    return output

@app.route('/')
def webapp():
    output = ("""
    <html>
    <head>
    <title>Python Music Trivia - """ + playlist_title + """</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
    <style>
        /* Table row/col transposition
        https://siongui.github.io/2017/04/16/css-only-transpose-html-table/ */
        //tr { display: block; float: left; }
        //th, td { display: block; }
    </style>
    <script>
    function toggleView(id) {
        var x = document.getElementById(id);
        x.style.backgroundColor = "#c2ffbd";
        var anchors = document.getElementsByTagName("a");
        for (var i = 0; i < anchors.length; i++) {
            anchors[i].onclick = function() {return false;};
        }
    }
    </script>
    </head>
    <body>
    <h1>Playlist: """ + playlist_title + """</h1>
    <p>Click on any clue to start playback. Clue links are disabled until playback is finished.</p>
    <p>The currently playing clue will be highlighted in <span style="background-color: #c2ffbd;">green</span>.</p>
    <table class="table table-bordered">
    """ + generate_html() +
    """
    </table>
    </body>
    </html>    
    """)
    return output

@app.route('/shuffleplay/<int:id>')
def shuffle_play(id):
    id = id - 1
    try:
        play_track_for_x_time(tsv_clues[id][0], tsv_clues[id][4], tsv_clues[id][3])
    except:
        return """
        <p>Oops. Spotify needs to be open on a device before this will work.</p>
        <p>Click <a href='https://open.spotify.com/track/2d7139N7CJ9eJmGVE42Y44?si=94e5a32190fb45d2' target=_blank>here</a> to open Spotify in another browser tab and press the play button to activate the device for playback.<br/><b>Keep the Spotify tab open</b>.</p>
        <p>Then go back to the <a href='/'>home page</a> and try again.</p>
        """
    return redirect('/')