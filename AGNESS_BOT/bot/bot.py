from discord.ext.commands import Bot as basebot
from discord.ext import commands
import discord
from AGNESS_BOT import configs, logger

putlog = logger.get_custom_logger(__name__)

DEFAULT_ROLE = configs.DEFAULT_ROLE
COMMAND_PREFIX = configs.COMMAND_PREFIX
BOT_TOKEN = configs.BOT_TOKEN
ON_READY_DM = configs.ON_READY_DM
ON_CONNECT_DM = configs.ON_CONNECT_DM
ON_DISCONNECT_DM = configs.ON_DISCONNECT_DM
SEND_DM = configs.SEND_DM
SEND_DM_TO = configs.SEND_DM_TO
COGS = configs.COGS
OWNER_IDS = configs.OWNER_IDS


class Bot(basebot):
    def __init__(self):
        self.prefix = COMMAND_PREFIX
        self.ready = False
        self.token = BOT_TOKEN
        self.botcogs = COGS
        self.send_dm = SEND_DM
        self.on_ready_dm = ON_READY_DM
        self.on_connect_dm = ON_CONNECT_DM
        self.on_disconnect_dm = ON_DISCONNECT_DM
        self.dm_users = SEND_DM_TO
        super().__init__(command_prefix=self.prefix, owner_ids=OWNER_IDS)

    def run(self):
        super().run(self.token, reconnect=True)

    def setup(self):
        putlog.info('loading COGs -------------------------------------------+')
        for cog in self.botcogs:
            try:
                self.load_extension(f'{cog}')
                putlog.info('{: <40} Loaded.     OK!'.format(str(cog)))
            except:
                putlog.error(f'{cog}        NOT FOUND!')
        putlog.info('COGs Loaded---------------------------------------------+\n')

    async def on_connect(self):
        putlog.debug('Bot is connected.      OK!')

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.MissingRole):
            await context.send('You are not allowed to use this command  🙅‍♂️  🚫')
        elif isinstance(exception, commands.CommandNotFound):
            await context.send('Sorry! but the command is invalid.')
        elif isinstance(exception, commands.MissingRequiredArgument):
            await context.send(exception)
        else:
            # original = getattr(exception, "original", exception)
            putlog.exception(exception)
            # raise original
            # return

    async def on_error(self, event_method, *args, **kwargs):
        raise

    async def on_disconnect(self):
        putlog.error('Bot is disconnected...    DISCONNECTED!')

    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name=DEFAULT_ROLE)
        await member.add_roles(role)

    async def on_ready(self):
        await bot.change_presence(
            activity=discord.Activity(type=configs.ACTIVITY_TYPE, name=configs.ACTIVITY_NAME))

        if not self.ready:
            self.ready = True
            self.setup()
            if self.send_dm and self.on_ready_dm:
                for dmuser in self.dm_users:
                    assert isinstance(dmuser, int)
                    owner = self.get_user(dmuser)
                    await owner.send('Bot is Online...')
                putlog.debug('Bot is online...       OK!')
            else:
                putlog.debug('Bot is online...       OK!')
        else:
            putlog.warning('Bot is online...       RECONNECTING!')


bot = Bot()
