import os

# Name of the bot that will be visible on footers of embeds
BOT_NAME = 'Agness'

# Command Prefix that will be used for invoking the commands.
COMMAND_PREFIX = '!'

# Your bot token data_type : int
BOT_TOKEN = os.environ.get('AGNESS_BOT_TOKEN')

# A dict of owner names and their IDs. Name key is just for ease of differentiate for user, bot just user value by
# list(OWNER_IDS.values()).
OWNER_IDS = {
    'Nitin': 734861106698387548,
}

# Set this var to True if you want to receive the dm by bot at all.
SEND_DM = False

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
]

# These names will be used to sort commands based on roles. For example if your Admin has a different name "Hokagye",
# then change ADMIN_ROLE = 'Hokagye'.
OWNER_ROLE = 'Owner'
ADMIN_ROLE = 'Admin'
STAFF_ROLE = 'Staff'
DEFAULT_ROLE = 'Member'

HOT_WORD = 'hey agness'

