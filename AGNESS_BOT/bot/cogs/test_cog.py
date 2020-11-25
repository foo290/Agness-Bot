"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This extension module contains commands which are available to all members.
"""

from discord.ext import commands
from AGNESS_BOT import (
    configs,
    EventEmbeds,
    GetUrl
)

import discord

DEFAULT_ROLE = configs.DEFAULT_ROLE


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cheer(self, ctx):
        await ctx.send(embed=discord.Embed().set_image(
            url=GetUrl.get('cheer')))

    @commands.command()
    async def lol(self, ctx):
        await ctx.send(embed=discord.Embed().set_image(
            url='https://media.tenor.com/images/4f404ce06825f7d2b6ab44a3ac2acd41/tenor.gif'))

    @commands.command()
    async def sendm(self, ctx):
        await ctx.send(embed=EventEmbeds().member_verification_complete())


def setup(client):
    client.add_cog(Test(client))
