"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This extension module contains commands related to ADMIN.
"""

import discord
import asyncio
from typing import Union
from discord.ext import commands
from AGNESS_BOT import (
    custom_help_cmd,
    calculate_time,
    configs
)

ADMIN_ROLE = configs.ADMIN_ROLE
BOT_NAME = configs.BOT_NAME

CHANNEL_MUTE = False


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_role(ADMIN_ROLE)
    @commands.command()
    async def ban(self, ctx, member: Union[discord.Member, str], reason=None) -> None:
        """
        Ban can be applied either by mentioning the user or by its ID.

        :param ctx: Passed by discord.
        :param member: Passed by discord. Member who is about to be banned.
        :param reason: A reason for the ban. (Optional)
        :return: None / Sends message back with relevant message in embed.
        """

        banembed = discord.Embed(
            title='Ban User ❌ ',
            description=f"Permanent Ban Applied 👌 to {member.id}",
            colour=discord.Color.dark_red()
        )
        banembed.set_footer(text=f'powered by : {BOT_NAME}')
        await member.ban(reason=reason)
        await ctx.send(embed=banembed)

    @staticmethod
    async def send_unban(ctx, user) -> None:
        """
        This method is called after banned user found in guild.bans() and being unbanned.
        Sends an embedded message in guild for the user who just got unbanned.

        :param ctx: Passed by unban method.
        :param user: The user who just got unbanned.
        :return: None / sends message in guild.
        """
        unbanembed = discord.Embed(
            title='Unban User ✅',
            description=f"{user.mention} is unbanned and allowed to interact.",
            colour=discord.Color.green()
        )
        unbanembed.set_footer(text=f'powered by : {BOT_NAME}')
        await ctx.send(embed=unbanembed)
        return

    @commands.has_role(ADMIN_ROLE)
    @commands.command()
    async def unban(self, ctx, *, member) -> None:
        """
        Unban command. Unban user by ID.

        :param ctx: Passed by discord.
        :param member: ID of banned user passed by admin.
        :return: None
        """

        banned_users = await ctx.guild.bans()
        user_dis = int(member)

        for banned_entry in banned_users:
            user = banned_entry.user
            if user.id == user_dis:
                await ctx.guild.unban(user)
                await self.send_unban(ctx, user)
        else:
            await ctx.send(f'🤖 User not found with give id : {user_dis}')
            return

    @commands.has_role(ADMIN_ROLE)
    @commands.command(aliases=['silence'])
    async def shh(self, ctx, *, time='5', unit='min'):
        """
        This method is command which mutes the whole channel for given time. (Only Admins will be able to send message)
        When invoked, No user will be able to send message until you manually remove it or time runs out.
        Global variable "CHANNEL_MUTE" is used to keep track.

        :param ctx: Passed by discord.
        :param time: Time interval for mute. Passed by admin, default is 5 minutes.
        :param unit: unit of time (s, m, h, d)
        :return: None
        """

        global CHANNEL_MUTE

        seconds = calculate_time(int(time), unit.lower())
        muted = discord.Embed(
            title='Silence! 🤫',
            description=f"Channel is muted for {time} {unit} for everyone!",
            colour=discord.Color.orange()
        )
        muted.set_footer(text='Muted by : Administrator')

        unmuted = discord.Embed(
            description=f"Silence removed! You can send messages now. ☑",
            colour=discord.Color.green()
        )
        unmuted.set_footer(text='UnMuted by : Timer')

        await ctx.send(embed=muted)
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        CHANNEL_MUTE = True
        await asyncio.sleep(seconds)
        if CHANNEL_MUTE:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send(embed=unmuted)

    @commands.has_role(ADMIN_ROLE)
    @commands.command(aliases=['rm_silence'])
    async def unshh(self, ctx):
        """
        Opposite of "shh()" method. Removes the restriction from the channel.
        :param ctx: Passed by discord.
        :return: None
        """

        global CHANNEL_MUTE

        unmuted = discord.Embed(
            description=f"Silence removed! You can send messages now. ☑",
            colour=discord.Color.green()
        )
        unmuted.set_footer(text='UnMuted by : Administrator')

        if CHANNEL_MUTE:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            CHANNEL_MUTE = False
            await ctx.send(embed=unmuted)
        else:
            await ctx.send(embed="It's discord already in here...")

    @commands.has_role(ADMIN_ROLE)
    @commands.command(aliases=['hgb'])
    async def help_global(self, ctx):
        """
        Shows all commands regardless of roles.
        :param ctx: Passed by discord.
        :return: None
        """

        await ctx.send(embed=custom_help_cmd('global_help', client=self.client))


def setup(client):
    client.add_cog(Admin(client))
