
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from graphics import graphics
#from mytest import mytest



def setup():
    # Login to Spotify
    scope = 'user-read-currently-playing, user-modify-playback-state, playlist-read-private'
    cid = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    username = 'xxxxxxxxxxxxxx'
    my_url = 'any url'

    # Generate token (currently unused)
    token = util.prompt_for_user_token(username, scope, cid, secret, my_url)

    # Get spotify object
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=my_url, scope=scope))

    # Great graohic canvas object
    #gui = graphics(1000, 1000, 'spotify_player')

    return sp



def print_divider():
    print("\n___________________________________\n")



def print_new_screen():
    for i in range(50):
        print('')


def print_current_track_info(sp):
    track = sp.current_user_playing_track()

    # Get current track name
    try:
        current_track_name = track['item']['name']
    except:
        print("Failed to get current track name.")
        current_track_name = "UNKNOWN"
    # Get current track artist
    try:
        current_track_artist = track['item']['artists'][0]['name']
    except:
        print("Failed to get current track artist.")
        current_track_artist = "UNKNOWN"
    # Get current track album
    try:
        current_track_album = track['item']['album']['name']
    except:
        print("Failed to get current track album.")
        current_track_album = "UNKNOWN"
    
    # Print current track info
    print_divider()
    print("Current track:", current_track_name)
    print("Artist:", current_track_artist)
    print("Album:", current_track_album)
    print_divider()



def get_current_track_info(sp):
    track = sp.current_user_playing_track()

    # Get current track name
    try:
        current_track_name = track['item']['name']
    except:
        print("Failed to get current track name.")
        current_track_name = "UNKNOWN"
    # Get current track artist
    try:
        current_track_artist = track['item']['artists'][0]['name']
    except:
        print("Failed to get current track artist.")
        current_track_artist = "UNKNOWN"
    # Get current track album
    try:
        current_track_album = track['item']['album']['name']
    except:
        print("Failed to get current track album.")
        current_track_album = "UNKNOWN"
    try:
        current_track_id = track['item']['id']
    except:
        print("Failed to get current track id.")
        current_track_id = "UNKNOWN"

    # Return current track ID
    return [current_track_id, current_track_name, current_track_artist, current_track_album]



def add_track(sp):
    # Add a song to up next
    song_name = input("Track name: ")

    # Find first 10 search results
    results = sp.search(song_name, limit=10, offset=0, type='track', market=None)
    
    # Ask the user if they want to add each search result, until the correct song is found
    # Figuring out exactly how to retrieve the track name, artist name, and track ID from the dictionary that
    # is returned by the search function was tremendously difficult. Lots and lots of trial and error.
    # Who would've thought it would require accessing so many consecutive dictionaries and lists??
    for i in range(len(results['tracks']['items'])):
        user_input = input("Add " + results['tracks']['items'][i]['artists'][0]['name'] + "-" + results['tracks']['items'][i]['name'] + "? (y/n): ")
        if user_input == 'y':
            try:
                sp.add_to_queue(results['tracks']['items'][i]['id'])
            except:
                print_divider()
                print("Error adding track. Possible cause: Premium required.")   
                print_divider()
            else:
                print_divider()
                print("Success! Track added to queue.")   
                print_divider()
            return



def playlist(sp):
    results = sp.current_user_playlists(limit=50, offset=0)
    #print(results)
    for i in range(len(results['items'])):
        name = results['items'][i]['name']
        user_preference = input("Add " + name + " ? (y/n): ")
        if user_preference == 'y':
            playlist_contents = sp.playlist(results['items'][i]['id'], fields='tracks,next')
            tracks = playlist_contents['tracks']
            #print(tracks['items'][0]['id']) # DEBUG
            print(tracks) # DEBUG
            for j in range(len(tracks['items'])):
                try:
                    #print(tracks['items'][j]['id'])
                    sp.add_to_queue(tracks['items'][j]['track']['id'])
                except:
                    print_divider()
                    print("Error adding track. Possible cause: Premium required.")   
                    print_divider()
                else:
                    print_divider()
                    print("Song added to up next!")   
                    print_divider()

            # Done!
            print_divider()
            print("Playlist successfully added!")   
            print_divider()
            return



def add_album(sp):
    # Add an album to up next
    album_name = input("Album name: ")

    # Find first 10 search results
    results = sp.search(album_name, limit=10, offset=0, type='album', market=None)
    #print(results)
    for i in range(len(results['albums']['items'])):
        user_input = input("Add " + results['albums']['items'][i]['artists'][0]['name'] + "-" + results['albums']['items'][i]['name'] + "? (y/n): ")
        if user_input == 'y':
            album_contents = sp.album_tracks(results['albums']['items'][i]['id'])
            print(album_contents) # DEBUG
            print("adding tracks now") # DEBUG
            for j in range(len(album_contents['items'])):
                try:
                    #print(tracks['items'][j]['id'])
                    sp.add_to_queue(album_contents['items'][j]['id'])
                except:
                    print_divider()
                    print("Error adding track. Possible cause: Premium required.")   
                    print_divider()
                else:
                    print_divider()
                    print("Song added to up next!")   
                    print_divider()
            # Done!
            print_divider()
            print("Album successfully added!")   
            print_divider()
            return



def repeat(sp, state):
    sp.repeat(state=state, device_id=None)
    return



def clear_queue(sp):
    # Ensure repeat is not on so that we do not get an infinite loop
    repeat(sp, 'off')

    # Add song at end to mark we have reached the end
    sp.add_to_queue('spotify:track:3gHoqx8j6Fwc5nucTkEJ0A')
    while get_current_track_info(sp)[0] != '3gHoqx8j6Fwc5nucTkEJ0A':
        next(sp)
    next(sp)

    # Done!
    print_divider()
    print("Queue cleared!")   
    print_divider()
    return



def print_playback():
    pass



def pause(sp):
    try:
        sp.pause_playback()
    except:
        print_divider()
        print("Error pausing. Possible cause: Premium required.")   
        print_divider()
    else:
        print_divider()
        print("Paused successfully!")   
        print_divider()



def show_help():
    print_divider()
    print("'clear' : clears console output.")
    print("'add track' : add a track to playback.")
    print("'add album' : add an album to queue.")
    print("'add playlist' : add (your) playlist to queue.")
    print("'pause' : pause playback.")
    print("'resume': resume playback.")
    print("'next' : skip to next song in queue.")
    print("'previous' : return to previous song.")
    print("'clear queue' : clear the queue of all tracks (disables repeat).")
    print("'repeat track' : enable repeat for the current track.")
    print("'repeat context' : enable repeat for the current context.")
    print("'repeat off' : disable repeat.")
    print_divider()
    #unused = input("Press any key to continue.")



def update(sp):
    print_new_screen()
    print_divider()
    print("Updating...")
    # Print the current track info
    print_current_track_info(sp)
    print_divider()



def next(sp):
    try:
        sp.next_track()
    except:
        print_divider()
        print("Error skipping. Possible cause: Premium required.")   
        print_divider()
    else:
        print_divider()
        print("Skipped to next song successfully!")   
        print_divider()



def previous(sp):
    try:
        sp.previous_track()
    except:
        print_divider()
        print("Error returning. Possible cause: Premium required.")   
        print_divider()
    else:
        print_divider()
        print("Returned to previous song successfully!")   
        print_divider()



def resume(sp):
    try:
        sp.start_playback()
    except:
        print_divider()
        print("Error starting playback. Possible cause: Premium required.")
        print_divider()
    else:
        print_divider()
        print("Playback resumed successfully!")   
        print_divider()



def update_gui(gui, sp):
    gui.rectangle(0, 0, 1000, 1000, 'green')
    info = get_current_track_info(sp)
    gui.text(450, 200, info[1], "white")
    gui.text(450, 250, info[2], "white")
    gui.text(450, 300, info[3], "white")
    gui.text(450, 300, str(info[0]), "white")



def main():
    # Run setup function and get the spotify object
    sp = setup()

    # Print the current track info
    #print_current_track_info(sp)

    user_input = 'null'
    while not user_input == "exit":

        # Get user input
        user_input = input("\n\nInstruction (type 'help' for help): ")

        if user_input == 'help':
            show_help()
        elif user_input == 'clear':
            print_new_screen()
        elif user_input == 'add track':
            add_track(sp)
        elif user_input == 'add playlist':
            playlist(sp)
        elif user_input == 'pause':
            pause(sp)
        elif user_input == 'next':
             next(sp)
        elif user_input == 'previous':
            previous(sp)
        elif user_input == 'resume':
            resume(sp)
        elif user_input == 'clear queue':
            clear_queue(sp)
            #print("This command is temporarily unavilable due to limitations with Spotify's web API. To be finished later.")
        elif user_input == 'repeat track':
            repeat(sp, 'track')
        elif user_input == 'repeat context':
            repeat(sp, 'context')
        elif user_input == 'repeat off':
            repeat(sp, 'off')
        elif user_input == 'add album':
            add_album(sp)

        # Clear screen
        #print_new_screen()

    # If user types 'exit':
    print("Exiting.")       



main()
                                                                                             
