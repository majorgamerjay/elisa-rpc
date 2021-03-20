import dbus
import json

from pypresence import Presence
from time import sleep
from collections import deque
from datetime import timedelta as td

# Getting RPC configuration details:
with open('config.json') as config:
    datalist = json.load(config)
    client_id = datalist['id']
    small_image_key = datalist['small_image_key']
    large_image_key = datalist['large_image_key']
    small_image_text = datalist['small_image_text']
    large_image_text = datalist['large_image_text']
    config.close()

RPC_Client = Presence(client_id)

RPC_Client.connect()

# Connect and get information about player and music using D-Bus
# The interfaces must be reinitialized again to get the data stored into the
# variables or the old data will stay and it will give wrong output and errors
def connect_and_get_dbus_info():
    # Define global variables for use of variables outside the function
    global elisa_properties
    global metadata
    while True:
        try:
            # Proxy object for getting Elisa's Bus.
            elisa = session_bus.get_object('org.mpris.MediaPlayer2.elisa',
                '/org/mpris/MediaPlayer2')
        except dbus.exceptions.DBusException:
            print('Couldn\'t connect to Elisa\'s Bus')
            sleep(5)
        else:
            break
    # Properties interface for Elisa
    elisa_properties = dbus.Interface(elisa, dbus_interface='org.freedesktop.DBus.Properties')
    # Metadata interface
    metadata = elisa_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

# Declare session bus from D-Bus.
session_bus = dbus.SessionBus()

elisa_properties = None # Interface for connecting with properties of Elisa's interface
metadata = None # Getting metadata of currently playing song

connect_and_get_dbus_info()

# Add list of artists to one variable and declare it by popping by dequed
while True:
    connect_and_get_dbus_info()

    track_name = metadata.get('xesam:title') or meta.get('xesam:url')
    track_artists = metadata.get('xesam:artist')

    if track_artists:
        track_artists = deque(track_artists)
        track_artist = track_artists.popleft()
        while len(track_artists) > 0:
            track_artist = track_artist + ', ' + track_artists.popleft()

    playback_status = ""

    while True:
        try:
            playback_status = elisa_properties.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus")
        except dbus.exceptions.DBusException:
            print("Have you closed the program? If you did, restart the program.")
            connect_and_get_dbus_info()
            sleep(5)
        else:
            break

    RPC_STATE = '{}: "{}"'.format(
            playback_status,
            track_name)

    RPC_DETAILS = track_artist

    print(RPC_STATE + ' ' + RPC_DETAILS)

    # RPC
    RPC_Client.update(state=RPC_DETAILS,
            details=RPC_STATE,
            large_image=large_image_key,
            large_text=large_image_text,
            small_image=small_image_text,
            small_text=small_image_text)

    # Sleep to increase count
    sleep(15)
