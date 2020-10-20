from discord.ext import commands
import discord
import asyncio
from AGNESS_BOT.utils.time_utils import calculate_time
from AGNESS_BOT.global_configs import STAFF_ROLE

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
        muted.set_footer(text='powered by : Agness')

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
        unmuted.set_footer(text='powered by : Agness')
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


def setup(client):
    client.add_cog(Staff(client))