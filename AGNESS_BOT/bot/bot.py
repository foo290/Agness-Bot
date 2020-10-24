from discord.ext.commands import Bot as basebot
from discord.ext import commands
import discord
from AGNESS_BOT.settings import (
    DEFAULT_ROLE,
    COMMAND_PREFIX,
    BOT_TOKEN,
    ON_READY_DM,
    ON_CONNECT_DM,
    ON_DISCONNECT_DM,
    SEND_DM,
    SEND_DM_TO,
    COGS,
    OWNER_IDS
)

OWNER_IDS = list(OWNER_IDS.values())


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
        print('loading COGs-----------------------------------------')
        for cog in self.botcogs:
            try:
                self.load_extension(f'AGNESS_BOT.bot.cogs.{cog}')
                print(f'OK!    AGNESS_BOT.bot.cogs.{cog} Loaded.')
            except:
                print(f'NOT FOUND!    AGNESS_BOT.bot.cogs.{cog}')
        print('COGs Loaded------------------------------------------\n')

    async def on_connect(self):
        print('Connecting...')
        print('OK!    Bot is connected')

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.MissingRole):
            await context.send('You are not allowed to use this command  🙅‍♂️  🚫')
        elif isinstance(exception, commands.CommandNotFound):
            await context.send('umm...🤔   This command is not valid. Atleast not for me. 😐')
        elif isinstance(exception, commands.MissingRequiredArgument):
            await context.send(exception)
        else:
            raise getattr(exception, "original", exception)

    async def on_error(self, event_method, *args, **kwargs):
        raise

    async def on_disconnect(self):

        print('bot is disconnected...')

    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name=DEFAULT_ROLE)
        await member.add_roles(role)

    async def on_ready(self):
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="the world collapse"))

        if not self.ready:
            self.ready = True
            self.setup()
            if self.send_dm and self.on_ready_dm:
                for dmuser in self.dm_users:
                    assert isinstance(dmuser, int)
                    owner = self.get_user(dmuser)
                    await owner.send('Bot is Online...')
                print('Bot is online...')
            else:
                print('Bot is online...')
        else:
            print('reconnecting')


bot = Bot()
