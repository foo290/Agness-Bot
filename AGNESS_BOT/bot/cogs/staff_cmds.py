from discord.ext import commands
import discord
import asyncio
from AGNESS_BOT.utils.time_utils import calculate_time
from AGNESS_BOT.settings import STAFF_ROLE, BOT_NAME


class Staff(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_role(STAFF_ROLE)
    @commands.command()
    async def mute(self, ctx, member: discord.Member, time=15, unit='min', reason=None):
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
    async def unmute(self, ctx, member: discord.Member):
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
        try:
            await ctx.channel.purge(limit=amount + 1)
        except:
            await ctx.send('You are not allowed to use this command')

    @commands.has_role(STAFF_ROLE)
    @commands.command(aliases=['eval'])
    async def evaluate(self, ctx, *, cmd):
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

    # @commands.guild_only()
    @commands.has_role(STAFF_ROLE)
    @commands.command(aliases=['warn', 'w'])
    async def warning(self, ctx, member: discord.Member, *, reason=None):
        warning_embed = discord.Embed(
            title="Warning!    ⚠",
            description=f"{member.mention} you've been warned!",
            colour=0xffed8a
        )
        if reason:
            warning_embed.add_field(name='Reason', value=reason, inline=False)
        warning_embed.set_footer(text=f'powered by : {BOT_NAME}')

        await ctx.send(embed=warning_embed)


def setup(client):
    client.add_cog(Staff(client))
