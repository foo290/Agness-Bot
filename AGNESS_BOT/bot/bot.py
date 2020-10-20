from discord.ext.commands import Bot as basebot
import os
import discord
from glob import glob
from AGNESS_BOT.global_configs import DEFAULT_ROLE

PREFIX = '.'
OWNER_IDS = [734861106698387548]
BOT_TOKEN = os.environ.get('AGNESS_BOT_TOKEN')
COGS = [cog.split('\\')[-1][:-3] for cog in glob('./bot/cogs/*.py')]



class Bot(basebot):
    def __init__(self):
        self.prefix = PREFIX
        self.ready = False
        self.token = BOT_TOKEN
        self.botcogs = COGS
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def run(self):
        self.setup()
        super().run(self.token, reconnect=True)

    def setup(self):
        for cog in self.botcogs:
            print(f'{cog}----------------------')
            self.load_extension(f"AGNESS_BOT.bot.cogs.{cog}")

    async def on_connect(self):
        print('Bot is connected...')

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
            print('Bot is online...')
        else:
            print('reconnecting')





bot = Bot()
