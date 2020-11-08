"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This module is the heart of the Bot. Every settings defined or set here is been used throughout the bot.

Abbreviation:
    --> settings groups : A dict is referred as settings group coz every dict contains settings related to
                          some specific task.

Every group of settings are dicts and joined in a single dict later in utils.configMapper.

These settings are accessed by "." (dot) operator with exact names like :
        config.BOT_NAME  ----> Gives bot name

Once you define a new setting group as dict, add that in the Config class at bottom.
Remember these are dicts, Keys are unique in all settings groups as they are joined as one later.
Two settings groups cannot have same keys, even if they are different dicts here. For ex :
    > If "ACTIVITY_TYPE" is already used in "BOT_CONFIGS" settings group, it cannot be used in any other settings group.

"""

import os
from discord import ActivityType as act
from AGNESS_BOT.utils.configMapper import Config

COGS_DIR = 'AGNESS_BOT.bot.cogs.'  # This is the directory that contains all the cogs

"""
Computer Operation Groups : Add your cog here.
COG_DIR and COGS make the complete import later in core code. Ex :
    --> Every COG is imported as COGS_DIR + cog_name_defined_in_COGS
"""
COGS = [
    'admin_cmds',
    'dm_cmds',
    'members_cmds',
    'staff_cmds',
    'musiccog',
]

OWNER_IDS = {
    'Nitin': 734861106698387548,
}

#
BOT_CONFIGS = {
    'BOT_NAME': "Agness",
    'COMMAND_PREFIX': ".",
    'BOT_TOKEN': os.environ.get('AGNESS_BOT_TOKEN'),
    'OWNER_IDS': list(OWNER_IDS.values()),
    'COGS_DIR': COGS_DIR,
    'COGS': COGS,
    'ACTIVITY_TYPE': act.watching,
    'ACTIVITY_NAME': 'the world collapse!'
}

CHAT_CONFIGS = {
    'HOT_WORD': "hey agness"
}

#
FUNCTIONALITIES = {
    'MANAGE_BOOT_DM': True,
    'MANAGE_NEW_JOINING': True,
    'MANAGE_MEMBER_LEFT': True,
    'MANAGE_MUSIC': True,
    'MANAGE_MODERATION': True
}

# This is currently configured to get a dm by bot when bot is online.
DM_CONFIGS = {
    'DM_RECIPIENT': [OWNER_IDS['Nitin']],
    'SEND_DM': True,
    "ON_CONNECT": True
}

ROLE_ALIASES = {
    'OWNER_ROLE': 'Owner',
    'ADMIN_ROLE': 'Admin',
    'STAFF_ROLE': 'Staff',
    'DEFAULT_ROLE': 'Member'
}

# Currently not in use X_X
COMMAND_ALIASES = {
    'help': [
        'h', 'hlp', 'help'
    ],
}

MUSIC_PLAYER_CONFIGS = {
    'DEFAULT_VOLUME': 50,
    'MAX_VOLUME': 100
}

MUSIC_SERVER_CONFIGS = {
    'MUSIC_HOST': "lava-link-server.herokuapp.com",
    'MUSIC_PORT': 80,
    'REST_URI': "http://lava-link-server.herokuapp.com",
    'MUSIC_SERVER_PW': "serverserveserverdata",
    'MUSIC_SERVER_REGION': "na",
    'MUSIC_SEARCH_ENGINE': "soundcloud",
}

MUSIC_CHANNEL_CONFIGS = {
    'RESTRICT_CMDS_TO_MUSIC_CHANNEL': True,
    'MUSIC_CMD_CHANNEL': 769254977863417887,
    'BOT_LEAVE_DELAY': 10,
    'NOW_PLAYING_GIF_URL': r"https://i.pinimg.com/originals/64/53/24/645324641a0555cc55cea87787fc0bcb.gif",
    'INITIAL_CONNECT_GIF_URL': r"https://i.gifer.com/7d20.gif",
}

PLAYER_UTILITIES_CONFIGS = {
    'PAGINATION_LIMIT': 10,
}

LOGGING = {
    'LOG_FILE': 'logs/agness.log',
}

# Every settings group should be included here in order to be accessed internally.
configs = Config(
    LOGGING,
    BOT_CONFIGS,
    CHAT_CONFIGS,
    DM_CONFIGS,
    ROLE_ALIASES,
    MUSIC_SERVER_CONFIGS,
    MUSIC_PLAYER_CONFIGS,
    MUSIC_CHANNEL_CONFIGS,
    PLAYER_UTILITIES_CONFIGS
)
