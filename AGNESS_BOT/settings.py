import os
from discord import ActivityType as act
from AGNESS_BOT.utils.configMapper import Config

COGS = [
    'AGNESS_BOT.bot.cogs.admin_cmds',
    'AGNESS_BOT.bot.cogs.dm_cmds',
    'AGNESS_BOT.bot.cogs.members_cmds',
    'AGNESS_BOT.bot.cogs.staff_cmds',
    'AGNESS_BOT.bot.cogs.musiccog',
]

OWNER_IDS = {
    'Nitin': 734861106698387548,
}

BOT_CONFIGS = {
    'BOT_NAME': "Agness",
    'COMMAND_PREFIX': ".",
    'BOT_TOKEN': os.environ.get('AGNESS_BOT_TOKEN'),
    'OWNER_IDS': list(OWNER_IDS.values()),
    'COGS': COGS,
    'ACTIVITY_TYPE': act.listening,
    'ACTIVITY_NAME': 'to your commands.'


}

CHAT_CONFIGS = {
    'HOT_WORD': "hey agness"
}

DM_CONFIGS = {
    'DM_RECEPTIONIST': OWNER_IDS['Nitin'],
    'SEND_DM': True,
    "ON_CONNECT": True
}

ROLE_ALIASES = {
    'OWNER_ROLE': 'Owner',
    'ADMIN_ROLE': 'Admin',
    'STAFF_ROLE': 'Staff',
    'DEFAULT_ROLE': 'Member'

}

COMMAND_ALIASES = {
    'help': [
        'h', 'hlp', 'help'
    ],
}

MUSIC_SERVER_CONFIGS = {
    'MUSIC_HOST': "lava-link-server.herokuapp.com",

    'MUSIC_PORT': 80,
    'REST_URI': "http://lava-link-server.herokuapp.com",
    'MUSIC_SERVER_PW': "serverserveserverdata",
    'MUSIC_SERVER_REGION': "na",
    'MUSIC_SEARCH_ENGINE': "soundcloud",
}

MUSIC_PLAYER_CONFIGS = {
    'DEFAULT_VOLUME': 50,
    'MAX_VOLUME': 100
}

MUSIC_CHANNEL_CONFIGS = {
    'BOT_LEAVE_DELAY': 10,
    'NOW_PLAYING_GIF_URL': r"https://i.pinimg.com/originals/64/53/24/645324641a0555cc55cea87787fc0bcb.gif",
    'INITIAL_CONNECT_GIF_URL': r"https://i.gifer.com/7d20.gif",
}

LOGGING = {
    'LOG_FILE': 'logs/agness.log',
}

configs = Config(
    LOGGING,
    BOT_CONFIGS,
    CHAT_CONFIGS,
    DM_CONFIGS,
    ROLE_ALIASES,
    MUSIC_SERVER_CONFIGS,
    MUSIC_PLAYER_CONFIGS,
    MUSIC_CHANNEL_CONFIGS
)
