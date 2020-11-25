"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This extension module contains commands which are available to all members.
"""

from discord.ext import commands
from AGNESS_BOT import (
    configs,
    logger,
)

putlog = logger.get_custom_logger(__name__)


class OwnerCmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='shutdown')
    async def shutdown_command(self, ctx):
        try:
            await ctx.send("Going offline...")
            putlog.warning('Bot is going offline! #######')
            await self.client.close()
            putlog.info('Bot is offline! #######')
        except Exception as error:
            putlog.exception(error)


def setup(client):
    client.add_cog(OwnerCmd(client))
