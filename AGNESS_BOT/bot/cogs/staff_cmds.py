"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This extension module contains the commands used by staff role.
"""

from discord.ext import commands
import discord
import asyncio
from AGNESS_BOT import configs, calculate_time, logger
from typing import Union

STAFF_ROLE = configs.STAFF_ROLE
BOT_NAME = configs.BOT_NAME

putlog = logger.get_custom_logger(__name__)


class Staff(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_role(STAFF_ROLE)
    @commands.command()
    async def mute(self, ctx, member: Union[discord.Member, str], time=15, unit='min', reason=None):
        """
        Mute a user either by mentioning it or by ID of user.
        After a user is muted, he won't be able to see even the messages in channel.
        A "Muted" role is assigned to that user which has no permission.

        :param ctx: Passed by discord.
        :param member: The member who is about to be muted.
        :param time: Time interval for mute.
        :param unit: Unit of time (s, m, h, d)
        :param reason: Reason for mute (Optional)
        :return: None
        """

        muted = discord.Embed(
            title='🤐  Mute User',
            description=f"Mute Applied to {member.mention} for {time} {unit}",
            colour=discord.Color.light_grey()
        )
        muted.set_footer(text=f'powered by : {BOT_NAME}')

        try:
            seconds = int(calculate_time(int(time), str(unit).lower()))
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

            await member.add_roles(muted_role, reason=reason)
            await ctx.send(embed=muted)
            await asyncio.sleep(seconds)
            await member.remove_roles(muted_role, reason="Muted Time Up!")
        except Exception as e:
            print(e)
            await ctx.send(
                "something went wrong with the command"
            )

    @commands.has_role(STAFF_ROLE)
    @commands.command()
    async def unmute(self, ctx, member: Union[discord.Member, str]):
        """
        Pretty understood.
        :param ctx: Passed by DC
        :param member: Member to unmute.
        :return: None
        """

        unmuted = discord.Embed(
            title="Unmute 😀",
            description=f"Mute removed! {member.mention} is now free to message.",
            colour=discord.Color.green()
        )
        unmuted.set_footer(text=f'powered by : {BOT_NAME}')
        try:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.remove_roles(muted_role, reason="Admin removed the mute")
            await ctx.send(embed=unmuted)
        except Exception as e:
            print(e)
            await ctx.send(
                "something went wrong with the command"
            )

    @commands.has_role(STAFF_ROLE)
    @commands.command(aliases=['cls'])
    async def clear(self, ctx, amount=4):
        """
        Clears the given amount of message from the channel.
        :param ctx: Passed by DC
        :param amount: Amount of messages to be deleted, default is 4.
        :return: None.
        """

        try:
            await ctx.channel.purge(limit=amount + 1)
        except:
            await ctx.send('You are not allowed to use this command')

    @commands.has_role(STAFF_ROLE)
    @commands.command(aliases=['eval'])
    async def evaluate(self, ctx, *, cmd):
        """
        Just for fun. Evaluates python expressions.
        :param ctx: Passed by DC.
        :param cmd: Python expression.
        :return: None / Sends the result of the given expression.
        """
        try:
            r = True, eval(f"{cmd}")
        except Exception as error:
            r = False, error

        if r[0]:
            await ctx.send(
                f"Your eval job is completed...\n"
                f"```{cmd}  =  {r[1]}```"
            )
        else:
            await ctx.send(
                f'Can not evaluate this command. This is the reason :\n'
                f'```Exception : {r[1]}```'
            )

    @commands.has_role(STAFF_ROLE)
    @commands.command(aliases=['warn', 'w'])
    async def warning(self, ctx, member: Union[discord.Member, str], *, reason=None):
        """
        Warn a user for something quirky.
        :param ctx: I am not writing this every time....
        :param member: Member to warn.
        :param reason: A reason of warning (Optional)
        :return: None.
        """

        warning_embed = discord.Embed(
            title="Warning!    ⚠",
            description=f"{member.mention} you've been warned!",
            colour=0xffed8a
        )
        if reason:
            warning_embed.add_field(name='Reason', value=reason, inline=False)
        warning_embed.set_footer(text=f'powered by : {BOT_NAME}')

        await ctx.send(embed=warning_embed)

    @commands.has_role(STAFF_ROLE)
    @commands.command(aliases=['kik'])
    async def _kick(self, ctx, member: Union[discord.Member, str], *, reason=None):
        """
        No docs needed!
        :param ctx: ...
        :param member: ...
        :param reason: ...
        :return: None
        """
        await member.kick(reason=reason)
        await ctx.send(f'Member {member.mention} is kicked out of the server.')


def setup(client):
    client.add_cog(Staff(client))
