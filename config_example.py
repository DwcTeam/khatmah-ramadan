import os

# If find a token from .env file then use it, otherwise use the token from the this config file.
TOKEN = os.environ.get('TOKEN') or "YOUR_BOT_TOKEN"  # If you need to get a token, go to https://discordapp.com/developers/applications/me

# If not choise a default enabled guilds, the bot will work on all server join but need to many time to make a slash command.
DEFAULT_GUILDS_ENABELS = []  # If you want to enable guilds, add their ids here.


# MongoDB is a online database, you can use it to store data.
MONGO_DB_URI = os.environ.get('MONGO_DB_URI') or "YOUR_MONGO_DB_URI"  # if you need to get a mongoDB URI, go to https://cloud.mongodb.com/


QURAN_EMOJI = "YOUR_QURAN_EMOJI"  # Like this <:quran:959703248720252948> or 🕋