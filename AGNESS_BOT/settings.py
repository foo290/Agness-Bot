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
    'moderation_cmds',
    'musiccog',
    'owner_cmds',
    'test_cog'
]

OWNER_IDS = {
    'Nitin': 734861106698387548,
}

BOT_CONFIGS = {
    'BOT_NAME': "Amadeus",
    'COMMAND_PREFIX': "!",
    'BOT_TOKEN': os.environ.get('AMADEUS_BOT_TOKEN'),
    'OWNER_IDS': list(OWNER_IDS.values()),
    'COGS_DIR': COGS_DIR,
    'COGS': COGS,
    'ACTIVITY_TYPE': act.watching,
    'ACTIVITY_NAME': 'the world collapse!',
    'SHOW_TYPING': False,
    'TYPING_INTERVAL': 0.5
}

GUILDS_CONFIG = {
    'FIRST_REDIRECT_CHANNEL': 773203865151602729,  # Welcome Channel!
    'RULES_CHANNEL': 773219713026621490,

    'INVITE_LINK_TTL': 86400,
    'INVITE_LINK_MAX_USES': 50,
}

CHAT_CONFIGS = {
    'HOT_WORD': "hey amadeus"
}

#
FUNCTIONALITIES = {
    'MANAGE_BOOT_DM': True,
    'MANAGE_NEW_JOINING': True,
    'MANAGE_MEMBER_LEFT': True,
    'MANAGE_MUSIC': True,
    'MANAGE_MODERATION': True,
    'MANAGE_MESSAGES': True
}

# This is currently configured to get a dm by bot when bot is online.
DM_CONFIGS = {
    'DM_RECIPIENT': [OWNER_IDS['Nitin']],
    'SEND_DM': False,
    "ON_CONNECT": True
}


ROLE_ALIASES = {
    'OWNER_ROLE': 'Owner',
    'ADMIN_ROLE': 'Admin',
    'STAFF_ROLE': 'Staff',
    'DEFAULT_ROLE': 'Member',
    'NEW_ROLE': 'new'

}

# Currently not in use X_X
COMMAND_ALIASES = {
    'help': [
        'h', 'hlp', 'help'
    ],
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
    GUILDS_CONFIG,
)

# CLOUD CONFIGS:
#   BOT NAME
#   BOT TOKEN
#   CMD PREFIX
