import dbus
import json
import daemon
import logging

from os import getenv
from pathlib import Path
from pypresence import Presence
from pypresence import exceptions as pyexep
from time import sleep
from collections import deque
from datetime import timedelta as td

# Setting up logger
logpath = ""+getenv('HOME')+'.local/share/elisa-rpc'
Path(logpath).mkdir(parents=True, exist_ok=True)
logpath = logpath+'/elisa-rpc.log'

# Declaring file handler
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(logpath, mode='w')
fh.setFormatter(log_formatter)
fh.setLevel(logging.DEBUG)

# Creating new logger with file handler
logger = logging.getLogger('Elisa-RPC')
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

# Getting RPC configuration details:
with open('config.json') as config:
    datalist = json.load(config)
    client_id = datalist['id']
    small_image_key = datalist['small_image_key']
    large_image_key = datalist['large_image_key']
    small_image_text = datalist['small_image_text']
    large_image_text = datalist['large_image_text']
    config.close()
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
        except dbus.exceptions.DBusException as de:
            logger.error(de)
            logger.error('Could not connect to Elisa\'s Bus')
            sleep(5)
        else:
            break
    # Properties interface for Elisa
    elisa_properties = dbus.Interface(elisa, dbus_interface='org.freedesktop.DBus.Properties')
    # Metadata interface
    metadata = elisa_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')


elisa_properties = None # Interface for connecting with properties of Elisa's interface
metadata = None # Getting metadata of currently playing song

# Make daemon context:

with daemon.DaemonContext(files_preserve = [ fh.stream ]):
    RPC_Client = Presence(client_id)

    # Error handling in case Discord is closed when connecting to RPC
    while True:
        try:
            RPC_Client.connect()
        except (FileNotFoundError, ConnectionRefusedError):
            logger.error("Could not connect to RPC. Do you have discord running?")
            sleep(5)
        else:
            break

    session_bus = dbus.SessionBus()
    already_stopped = 0 # Magic variable for controlling the stoppah!

    while True:
        # Declare session bus from D-Bus.
        connect_and_get_dbus_info()

        track_name = metadata.get('xesam:title') or metadata.get('xesam:url')
        track_artists = metadata.get('xesam:artist')

        # Add list of artists to one variable and declare it by popping by dequed
        track_artist = None
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
                logger.error("Could not get PlaybackStatus")
                connect_and_get_dbus_info()
                sleep(5)
            else:
                break

        RPC_STATE = '{}: "{}"'.format(
                playback_status,
                track_name)

        # Check if track_artist is None, if it is, then change RPC_DETAILS to
        # "None" instead of putting it to None, which will occur concatenation
        # error later
        if track_artist != None:
            RPC_DETAILS = track_artist
        else:
            RPC_DETAILS = "None"

        logger.info(RPC_STATE + ' ' + RPC_DETAILS)

        # RPC and conditional statements to make sure to not update when
        # track_artist is None and playback_status is "Stopped"
        # also make sure if it is Stopped but there is track_artist (or a
        # song that got played before), make sure to sleep for a little bit
        # and then clear the client so other people may see the user stopped
        # listening to the song.
        if track_artist != None and playback_status != "Stopped":
            already_stopped = 0
            RPC_Client.update(state=RPC_DETAILS,
                    details=RPC_STATE,
                    large_image=large_image_key,
                    large_text=large_image_text,
                    small_image=small_image_text,
                    small_text=small_image_text)
            sleep(5)
        elif playback_status == "Stopped":
            if already_stopped == 0:
                RPC_Client.update(state=RPC_DETAILS,
                        details=RPC_STATE,
                        large_image=large_image_key,
                        large_text=large_image_text,
                        small_image=small_image_text,
                        small_text=small_image_text)
                already_stopped = 1
            sleep(5)
            # This handles if discord closes or turns on
            while True:
                try:
                    RPC_Client.clear()
                except (ConnectionRefusedError, pyexep.InvalidID):
                    logger.error('Connection reset, retrying connection')
                    while True:
                        try:
                            RPC_Client.connect()
                        except (FileNotFoundError, ConnectionRefusedError):
                            logger.error("Could not connect to RPC. Do you have discord running?")
                            sleep(5)
                        else:
                            break
                    sleep(5)
                else:
                    break

        else:
            while True:
                try:
                    RPC_Client.clear()
                except (ConnectionRefusedError, pyexep.InvalidID):
                    logger.error('Connection reset, retrying connection')
                    # This handles error just in case Discord still hasn't turned on
                    while True:
                        try:
                            RPC_Client.connect()
                        except (FileNotFoundError, ConnectionRefusedError):
                            logger.error("Could not connect to RPC. Do you have discord running?")
                            sleep(5)
                        else:
                            break
                    sleep(5)
                else:
                    break
            sleep(5)
