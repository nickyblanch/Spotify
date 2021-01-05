import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from graphics import graphics
#from mytest import mytest



def setup():
    # Login to Spotify
    scope = 'user-read-currently-playing, user-modify-playback-state, playlist-read-private'
    cid = '2d9136999f6046ad81e9fcf4fb15ca04'
    secret = '6ad44cf128154a0cb6ec8f244de084b7'
    username = 'nickyblanch-us'
    my_url = 'http://nickyblanch.xyz'

    # Generate token (currently unused)
    token = util.prompt_for_user_token(username, scope, cid, secret, my_url)

    # Get spotify object
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=my_url, scope=scope))

    # Great graohic canvas object
    gui = graphics(940, 1020, 'spotify_player')

    return sp, gui



def get_current_track_info(sp):
    track = sp.current_user_playing_track()

    # Get current track name
    try:
        current_track_name = track['item']['name']
    except:
        #print("Failed to get current track name.")
        current_track_name = "UNKNOWN"
    # Get current track artist
    try:
        current_track_artist = track['item']['artists'][0]['name']
    except:
        #print("Failed to get current track artist.")
        current_track_artist = "UNKNOWN"
    # Get current track album
    try:
        current_track_album = track['item']['album']['name']
    except:
        #print("Failed to get current track album.")
        current_track_album = "UNKNOWN"
    try:
        current_track_id = track['item']['id']
    except:
        #print("Failed to get current track id.")
        current_track_id = "UNKNOWN"

    # Return current track ID
    return [current_track_id, current_track_name, current_track_artist, current_track_album]



def update_gui(gui, sp):
    gui.rectangle(0, 0, 940, 1020, 'green')
    info = get_current_track_info(sp)
    gui.text(50, 200, info[1], "white")
    gui.text(50, 250, info[2], "white")
    gui.text(50, 300, info[3], "white")
    gui.text(50, 400, ("ID: " + info[0]), "white", "10")



def main():
    sp, gui = setup()
    while(1):
        gui.clear()
        update_gui(gui, sp)
        gui.update_frame(10)



main()