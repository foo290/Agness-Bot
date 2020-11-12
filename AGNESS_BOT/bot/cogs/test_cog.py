"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This extension module contains commands which are available to all members.
"""

from discord.ext import commands
from AGNESS_BOT import (
    configs,

    SillyCommands
)
from typing import Union
import discord

DEFAULT_ROLE = configs.DEFAULT_ROLE


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='slap')
    async def slap_command(self, ctx, member: Union[discord.Member, str]):
        await ctx.send(
            embed=SillyCommands().slap_member(
                ctx.author,
                member, ctx.author.color
            )
        )


def setup(client):
    client.add_cog(Test(client))
