import os

# If find a token from .env file then use it, otherwise use the token from the this config file.
TOKEN = os.environ.get('TOKEN') or "YOUR_BOT_TOKEN"  # If you need to get a token, go to https://discordapp.com/developers/applications/me

# If not choise a default enabled guilds, the bot will work on all server join but need to many time to make a slash command.
DEFAULT_GUILDS_ENABELS = []  # If you want to enable guilds, add their ids here.


MONGO_DB_URI = os.environ.get('MONGO_DB_URI') or "YOUR_MONGO_DB_URI"
