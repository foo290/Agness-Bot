from discord.ext import commands
import asyncio
from AGNESS_BOT.utils.embeds_utils import get_reminder_embeds
from AGNESS_BOT.utils.time_utils import calculate_time
from AGNESS_BOT.utils.web_crawlers import GoogleWebCrawler
from AGNESS_BOT.settings import DEFAULT_ROLE
import discord

class Members(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_role(DEFAULT_ROLE)
    @commands.command()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=0)
        await ctx.send(link)

    @commands.has_role(DEFAULT_ROLE)
    @commands.command(aliases=['remind', 'set_reminder'])
    async def remind_me(self, ctx, task, time, unit='min', s_user=None):
        p_user = str(ctx.author).split('#')[0]
        try:
            int(time)
        except:
            ctx.send('Time should be integer number')

        if s_user and str(s_user).startswith('<'):

            r_set, r_complete = get_reminder_embeds(p_user, s_user, task, time, unit, type_='mutual')
        else:
            r_set, r_complete = get_reminder_embeds(p_user, s_user, task, time, unit)
        try:
            assert len(unit.split()) == 1

            seconds = int(calculate_time(int(time), str(unit).lower()))
            await ctx.send(ctx.author.mention, embed=r_set)

            await asyncio.sleep(seconds)
            if s_user:
                await ctx.send(f"{s_user}, {ctx.author.mention}", embed=r_complete)
            else:
                await ctx.send(f"{ctx.author.mention}", embed=r_complete)

        except:
            await ctx.send(f'Something is not as what i expected...🤔... Unable to set reminder.'
                           f'\nTry again with right command format  : \n'
                           f'```.remind<space>"Your_Task_Name_Here"<space>TIME<space>Unit(mins or secs or hours)```')

    @commands.has_role(DEFAULT_ROLE)
    @commands.command()
    async def say(self, ctx, word, person):
        await ctx.send(
            f"{word} {person}"
        )

    @commands.has_role(DEFAULT_ROLE)
    @commands.command(aliases=['agness'])
    async def intro(self, ctx, *, person):
        await ctx.send(f'Hey {person.title()}, My name is Agness. I like peanut butter 😁😍')

    @commands.has_role(DEFAULT_ROLE)
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'N/W Ping is : {round(self.client.latency * 1000)} ms')

    @commands.has_role(DEFAULT_ROLE)
    @commands.command(aliases=['google', 'lookfor', 'look4', 'find'])
    async def search(self, ctx, *, query):
        crawler = GoogleWebCrawler(query)
        results = crawler.fetch_webpage(manage_cache=False)
        heading = list(results[0].keys())[0]
        content = list(results[0].values())[0]
        link = list(results[1].values())[0]
        c = f"This is what i found so far...\n\n{heading}\n{content}\n\nhttps://{link}"
        await ctx.send(
            f"{c}"
        )

    @commands.command()
    async def test_embedd(self, ctx):
        e = discord.Embed(description='Song name goes here')

        e.set_image(url="https://i.pinimg.com/originals/64/53/24/645324641a0555cc55cea87787fc0bcb.gif")
        # e.add_field(name='Now Playing...', value='Some thing a bit long string here so i can see it correctly', inline=False)
        e.set_footer(text='some footer text')
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Members(client))
