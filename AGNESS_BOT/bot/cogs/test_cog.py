"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This extension module contains commands which are available to all members.
"""

from discord.ext import commands
from AGNESS_BOT import (
    configs,
    SillyCommands,
    EventEmbeds,
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

    @commands.command()
    async def role(self, ctx):
        # await user.add_roles(role, reason=reason)
        print(ctx.user)
        print(self.client.user)
        # await ctx.send(f"Role {role.mention} has been assigned to {user.display_name}")

    @commands.command()
    async def create_r(self, ctx):
        guild = ctx.guild
        await guild.create_role()

    @commands.command(name='happydiwali')
    async def diwali_wish(self, ctx):
        await ctx.send(EventEmbeds().diwali())

    @commands.command()
    async def eq(self, ctx):
        await ctx.send(embed=discord.Embed().set_image(
            url='https://i.pinimg.com/originals/cb/17/b8/cb17b80a942d7c317a35ff1324fae12f.gif'))

    @commands.command()
    async def cheer(self, ctx):
        await ctx.send(embed=discord.Embed().set_image(
            url='https://firebasestorage.googleapis.com/v0/b/discord-bot-294607.appspot.com/o/bot%2Fgifs%2Fother_gifs%2Fwelcome%20gifs%2Fanime_cheer.gif?alt=media&token=f5618220-d975-4a3e-9f3e-6df4134986b3'))

    @commands.command()
    async def loader1(self, ctx):
        await ctx.send(embed=discord.Embed().set_image(
            url='https://cutewallpaper.org/21/equalizer-gif/Equalizer-GIFs-Get-the-best-gif-on-GIFER.gif'))

    @commands.command()
    async def lol(self, ctx):
        await ctx.send(embed=discord.Embed().set_image(
            url='https://media.tenor.com/images/4f404ce06825f7d2b6ab44a3ac2acd41/tenor.gif'))


def setup(client):
    client.add_cog(Test(client))
