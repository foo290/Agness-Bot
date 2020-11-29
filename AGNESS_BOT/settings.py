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

BASE_DIR = os.getcwd()

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
    'BOT_NAME': "Agness",
    'COMMAND_PREFIX': ".",
    'BOT_TOKEN': os.environ.get('AGNESS_BOT_TOKEN'),
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
    'GOODBYE_CHANNEL': 773208141616906251,

    'MEMBER_JOIN_SELF_VERIFICATION': True,

    'INVITE_LINK_TTL': 86400,
    'INVITE_LINK_MAX_USES': 50,
}

#
FUNCTIONALITIES = {
    'MANAGE_NEW_JOINING': True,
    'MANAGE_MEMBER_LEFT': True,
    'SEND_DM_ON_JOIN': True
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
    'DEFAULT_ROLE': 'Member',
    'UNVERIFIED': 'Unverified',
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
    DM_CONFIGS,
    ROLE_ALIASES,
    GUILDS_CONFIG,
    FUNCTIONALITIES,
    BASE_DIR=BASE_DIR
)

# CLOUD CONFIGS:
#   BOT NAME
#   BOT TOKEN
#   CMD PREFIX
#   DM
