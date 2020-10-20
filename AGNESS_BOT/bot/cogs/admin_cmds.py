from discord.ext import commands
import discord
from AGNESS_BOT.utils.time_utils import calculate_time
import asyncio
from AGNESS_BOT.global_configs import ADMIN_ROLE

CHANNEL_MUTE = False


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print('cogs')

    @commands.has_role(ADMIN_ROLE)
    @commands.command()
    async def ban(self,ctx, member: discord.Member, reason=None):

        banembed = discord.Embed(
            title='Ban User ❌ ',
            description=f"Permanent Ban Applied 👌 to {member.id}",
            colour=discord.Color.dark_red()
        )
        banembed.set_footer(text='powered by : Agness')
        await member.ban(reason=reason)
        await ctx.send(embed=banembed)

    async def send_unban(self,ctx, user):
        unbanembed = discord.Embed(
            title='Unban User ✅',
            description=f"{user.mention} is unbanned and allowed to interact.",
            colour=discord.Color.green()
        )
        unbanembed.set_footer(text='powered by : Agness')
        await ctx.send(embed=unbanembed)
        return

    @commands.has_role(ADMIN_ROLE)
    @commands.command()
    async def unban(self,ctx, *, member):
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
    @commands.command(aliases=['silence!'])
    async def shhh(self, ctx, *, time='5', unit='min'):
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
    @commands.command(aliases=['rm_silence!'])
    async def unshhh(self, ctx):
        global CHANNEL_MUTE
        unmuted = discord.Embed(
            description=f"Silence removed! You can send messages now. ☑",
            colour=discord.Color.green()
        )
        unmuted.set_footer(text='UnMuted by : Administrator')

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        CHANNEL_MUTE = False
        await ctx.send(embed=unmuted)

    @commands.has_role(ADMIN_ROLE)
    @commands.command(aliases=['loadcog'])
    async def load_exts(self, ctx, extension):
        print('loading ext...')
        self.client.load_extension(f"cogs.{extension}")
        print('ext loaded.')

    @commands.has_role(ADMIN_ROLE)
    @commands.command(aliases=['unloadcog'])
    async def unload_exts(self, ctx, extension):
        print('loading ext...')
        self.client.unload_extension(f"cogs.{extension}")
        print('ext loaded.')

    @commands.has_role(ADMIN_ROLE)
    @commands.command(aliases=['reloadcog'])
    async def reload_exts(self, ctx):
        await ctx.send('Reloading cogs...')
        for cog in self.client.botcogs:
            try:
                self.client.unload_extension(f"cogs.{cog}")
            except:
                print(f'{cog} does not exist')
                pass

        for cogs in self.client.botcogs:
            self.client.load_extension(f"cogs.{cogs}")

        await ctx.send('COGs Loaded!')





def setup(client):
    client.add_cog(Admin(client))