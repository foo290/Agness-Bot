import os

# Name of the bot that will be visible on footers of embeds
BOT_NAME = 'Agness'

HOT_WORD = 'hey agness'

# Command Prefix that will be used for invoking the commands.
COMMAND_PREFIX = '.'

# Your bot token data_type : int
BOT_TOKEN = os.environ.get('AGNESS_BOT_TOKEN')

# A dict of owner names and their IDs. Name key is just for ease of differentiate for user, bot just user value by
# list(OWNER_IDS.values()).
OWNER_IDS = {
    'Nitin': 734861106698387548,
}

# Set this var to True if you want to receive the dm by bot at all.
SEND_DM = True

# A list or tup containing IDs of the users that will be used to send DMs for bot events. Ex: bot is ready.
SEND_DM_TO = OWNER_IDS['Nitin'],

# Customize your DMs
ON_CONNECT_DM = True
ON_READY_DM = True
ON_DISCONNECT_DM = True

# Computer Operation Groups (COGs). Add your COG files here.
COGS = [
    'admin_cmds',
    'dm_cmds',
    'members_cmds',
    'staff_cmds',
    'musiccog',
]

# These names will be used to sort commands based on roles. For example if your Admin has a different name "Hokagye",
# then change ADMIN_ROLE = 'Hokagye'.
OWNER_ROLE = 'Owner'
ADMIN_ROLE = 'Admin'
STAFF_ROLE = 'Staff'
DEFAULT_ROLE = 'Member'

COMMAND_ALIASES = {
    'help': [
        'h', 'hlp', 'help'
    ],
}

# Music Player Configs : Powered by - Wavelink and Lavalink
# MUSIC_HOST = 'lava-link-server.herokuapp.com'  # '127.0.0.1'
MUSIC_HOST = '127.0.0.1'
# MUSIC_PORT = 80
MUSIC_PORT = 2333
# REST_URI = 'http://lava-link-server.herokuapp.com'
REST_URI = 'http://127.0.0.1:2333'
MUSIC_SERVER_PW = 'serverserveserverdata'
MUSIC_SERVER_REGION = 'na'

MUSIC_SEARCH_ENGINE = 'soundcloud'

# Volume range is upto 0-1000. Default volume is set for smooth hearing.
# Volume above 100 can be very noisy and creepy.
DEFAULT_VOLUME = 50
MAX_VOLUME = 100

# In Seconds : >> After given seconds the bot will leave the voice channel if no member is present.
BOT_LEAVE_CHANNEL_DELAY = 10  # Seconds

NOW_PLAYING_GIF_URL = r'https://i.pinimg.com/originals/64/53/24/645324641a0555cc55cea87787fc0bcb.gif'
INITIAL_CONNECT_GIF_URL = r'https://i.gifer.com/7d20.gif'
