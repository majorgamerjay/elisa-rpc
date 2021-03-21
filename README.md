# Elisa-RPC

### MajorGamerJay
#### majorgamerjay@protonmail.com

<img src="https://i.imgur.com/3YvZzRV.png" alt="screenshot" align="right" height=240px>
elisa-rpc is a program that shows your currently playing song in Elisa music
player to discord. Uses D-Bus to communicate with the Elisa music player and
then show music information to Discord.

## How to use it

To use it, copy the config file template (config_template.json)
from the root directory to the /src directory.

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
1. Run the script, `python3 main.py`

This program is created under MIT License.
