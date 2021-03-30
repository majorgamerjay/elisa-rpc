# Elisa-RPC

### MajorGamerJay
#### majorgamerjay@protonmail.com

<img src="https://i.imgur.com/3YvZzRV.png" alt="screenshot" align="right" height=240px>
elisa-rpc is a program that shows your currently playing song in Elisa music
player to discord. Uses D-Bus to communicate with the Elisa music player and
then show music information to Discord.

## How to use it

To use it, copy the config file template (config_template.json)
from the root directory to the /src directory as config.json

### Get required dependencies!

1. pip install -r requirements.txt

### Create an application to represent the RPC

1. Go to: https://discord.com/developers/applications
2. Create new application

### Put required info in config file

1. Copy Client ID and put it in "id" field in config.json
2. Go to Rich Presence
3. Upload your art assets
4. In place of image_keys in config.json, place the name of your art assets
5. Add description for your art asset in config.json

### Run the script!

1. cd into the directory, `cd ./src`
2. Run the script, `python3 elisa-rpc.py`

## Other tips

### Check whether the program is working

By default, this program is daemonized (meaning this will run in background). If the program isn't working, just open your process monitor and search for `elisa-rpc.py`. If it does not exist, then the program is not working.

Paste the program's log files from `~/.local/share/elisa-rpc/` and open an issue. I will try my best to reply as soon as possible.

### States of the program

All states of the RPC is updated every 5 seconds.

- When Elisa is not playing a song (at stopped), then the program will display `Stopped: <songname>` at Discord RPC for 5 seconds and it will clear
- When it is playing, a song: it will show information about that song in RPC
- If the song is paused: It will show the song is puased within the RPC

### Want to contribute?

Just make a pull request however you want lol. But I would appreciate if your code is well commented and more understandable. :)

This program is created under MIT License.
