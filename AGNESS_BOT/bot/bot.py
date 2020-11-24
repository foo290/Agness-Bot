"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This module is main Bot module.
DemonBot class in inherited from Bot class and necessary methods are overridden.

Configs (imported) is a dict containing every config defined in resonate_settings.py and accessible by "." (dot) operator.
"""

from discord.ext.commands import Bot
from discord.ext import commands
import discord
from AGNESS_BOT import configs, logger, EventEmbeds

putlog = logger.get_custom_logger(__name__)

# Configurations from resonate_settings.py

DEFAULT_ROLE = configs.DEFAULT_ROLE
COMMAND_PREFIX = configs.COMMAND_PREFIX
BOT_TOKEN = configs.BOT_TOKEN
BOT_NAME = configs.BOT_NAME
COGS_DIR = configs.COGS_DIR
COGS = configs.COGS
OWNER_IDS = configs.OWNER_IDS

DM_RECIPIENT = configs.DM_RECIPIENT
SEND_DM = configs.SEND_DM
ON_CONNECT = configs.ON_CONNECT


class DemonBot(Bot):
    """
    Main Bot class inherited from discord.ext.commands "Bot".
    Intents related stuff happens here.
    """

    def __init__(self):
        self.prefix = COMMAND_PREFIX
        self.ready = False
        self.bot_name = BOT_NAME
        self.token = BOT_TOKEN
        self.botcogs = COGS
        self.log_configs()
        self.dm_recipient = DM_RECIPIENT
        self.send_dm_authorization = SEND_DM
        self.on_connect_dm = ON_CONNECT
        super().__init__(command_prefix=self.prefix, owner_ids=OWNER_IDS)

    @staticmethod
    def log_configs() -> None:
        """
        This function just logs the current Configs bot is starting with.
        :return: None
        """

        putlog.info("Bot will start with the following Configs...")
        putlog.info(f"Default Role : {DEFAULT_ROLE}")
        putlog.info(f"Owner IDs : {OWNER_IDS}")
        putlog.info(f"Command Prefix : {COMMAND_PREFIX}")

    async def on_member_join(self, member) -> None:
        """
        Assign a role of "DEFAULT_ROLE" to every user who join the server.
        DEFAULT_ROLE: This is defined in resonate_settings.py
        :param member: Passed by discord, the user who joined the server.
        :return: None
        """
        channel = self.get_channel(configs.FIRST_REDIRECT_CHANNEL)
        rules_channel = self.get_channel(configs.RULES_CHANNEL)

        putlog.info(f'{member} has joined!')
        role = discord.utils.get(member.guild.roles, name=configs.NEW_ROLE)
        await member.add_roles(role)
        putlog.info(f"{member} has assigned with {role} role.")

        await member.send(f'**Welcome to {member.guild.name}! 😃**\n'
                          f'Hello {member.display_name}, I am {bot.user.display_name}!\n'
                          f'You have to write **i agree ####** in {channel.mention} where **####** '
                          f'is the four digits after your username in  discord. \n\n'
                          f'for example if i have username **example#1234**, then I would type i agree 1234".\n\n'
                          f'**But first, read the {rules_channel.mention}**\n\n'
                          f'Welcome again and have fun 🎉 🥳')

        if not member.bot:
            await channel.send(f'{member.mention} just arrived! ♥ Welcome to {member.guild.name} 😀 \n'
                               f'Lets make you familiar with rules : '
                               f'{rules_channel.mention}')
            await channel.send(embed=EventEmbeds().member_join(member, rules_channel))

    async def on_member_remove(self, member) -> None:
        """
        Events that should take place when a user is either kicked, or left the server.
        :param member: Passed by discord, the member related to the event.
        :return: None
        """
        channel = self.get_channel(773208141616906251)
        if not member.bot:
            await channel.send(embed=EventEmbeds().member_left(member))

        putlog.info(f"{member} has left the server")

    def run(self):
        super().run(self.token, reconnect=True)

    def setup(self) -> None:
        """
        This function loads the COGS defined in resonate_settings.py
        :return: None
        """

        putlog.info('loading COGs -------------------------------------------+')
        for cog in self.botcogs:
            try:
                self.load_extension(f'{COGS_DIR + cog}')
                putlog.info('{: <40} Loaded.     OK!'.format(str(COGS_DIR + cog)))
            except:
                putlog.error(f'{COGS_DIR + cog}        NOT FOUND!')
        putlog.info('COGs Loaded---------------------------------------------+\n')

    async def on_connect(self) -> None:
        """
        On connect event stuffs here...
        :return: None
        """
        putlog.debug('DemonBot is connected.      OK!')

    async def on_command_error(self, context, exception):
        """
        Overridden Function !
        Global Exception Handling here...
        Exceptions are handled locally in COGS too but common ones are handled here.
        :param context: Passed by discord
        :param exception: Passed by discord
        :return: None / raises exception or sends the relevant message.
        """

        if isinstance(exception, commands.MissingRole):
            await context.send('You are not allowed to use this command  🙅‍♂️  🚫')
        elif isinstance(exception, commands.CommandNotFound):
            await context.send('Sorry! but the command is invalid.')
        elif isinstance(exception, commands.MissingRequiredArgument):
            await context.send(exception)
        else:
            original = getattr(exception, "original", exception)
            raise original

    async def on_error(self, event_method, *args, **kwargs):
        raise

    async def on_disconnect(self) -> None:
        putlog.error('DemonBot is disconnected...    DISCONNECTED!')

    async def on_ready(self) -> None:
        """
        Sets the bot's status and logs the status of bot if it is online or not.
        Sends message to "DM_RECIPIENT" when bot is online if DM_CONFIGS are configured in resonate_settings.py.
        :return: None
        """
        await bot.change_presence(
            activity=discord.Activity(type=configs.ACTIVITY_TYPE, name=configs.ACTIVITY_NAME))
        if not self.ready:
            self.ready = True
            self.setup()
            if self.send_dm_authorization and self.on_connect_dm:
                for user_id in self.dm_recipient:
                    if isinstance(user_id, int):
                        dm_user = bot.get_user(user_id)
                        await dm_user.send(f'{self.bot_name} is online now...')

            putlog.debug('DemonBot is online...       OK!')

        else:
            putlog.warning('DemonBot is online...       RECONNECTING!')


bot = DemonBot()
