# Discord Music Player Bot

A discord bot used to play music over a discord voice channel (The bot may currently have some bugs).

## Usage

Download the source code and run the following in the terminal:
```
pip install -r requirements.txt
```
Inside the `config.py` file, make sure you change the toekn into your own discord bot token. This can be done through this [guide](https://www.writebots.com/discord-bot-token/).

```python
token = "Your discord bot token"
```

Then run to start the bot:
```
python -m bot
```

Invite the bot to your server and enjoy!

## Commands
### Prefix
The prefix for all commands is `$`

### join
The bot joins the voice channel the user is currently in

### leave
The bot leaves the voice channel it is currently in

### play
Syntax: 
```
$play input
```
The bot adds to the queue the requested song. The input can be either a string that the bot searches for through YouTube or a YouTube URL.

Examples:
```
$play Minecraft OST
```
```
$play https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### pause
Pauses the currently playing song

### resume
Resumes the currently playing song

### stop
Stops playing the current song and clears the queue

### skip
Skips the currently playing song and plays the next song in queue

### queue
Lists the songs available in the queue
