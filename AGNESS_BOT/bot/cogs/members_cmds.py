"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This extension module contains commands which are available to all members.
"""

from discord.ext import commands
import asyncio
from AGNESS_BOT import (
    configs,
    get_reminder_embeds,
    calculate_time,
    GoogleWebCrawler,
    InsigniaEmbeds
)

DEFAULT_ROLE = configs.DEFAULT_ROLE


class Members(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_role(DEFAULT_ROLE)
    @commands.command()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=0)
        await ctx.send(link)

    @commands.command(aliases=['remind', 'set_reminder'])
    async def remind_me(self, ctx, task, time, unit='min', s_user=None):
        """
        Set a reminder for either yourself or mutual reminder by pinging other user and the bot will remind you for
        your task.
        :param ctx: Passed by discord.
        :param task: Task to be reminded. Passed by user
        :param time: Time interval for reminder.
        :param unit: Unit of time (s, m, h, d)
        :param s_user: Second user (Optional) which will be pinged by bot for reminder (Mutual reminder.)
        :return: None
        """

        p_user = ctx.author.display_name
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
        """
        Silly command. Will be removed soon.

        :param ctx: X_X
        :param word: X_X
        :param person: X_X
        :return: X_X
        """

        await ctx.send(
            f"{word} {person}"
        )

    @commands.command(aliases=['agness'])
    async def intro(self, ctx, *, person):
        """
        Silly command. Will be removed soon.

        :param ctx: X_X
        :param person: X_X
        :return: X_X
        """

        await ctx.send(f'Hey {person.title()}, My name is Agness. I like peanut butter 😁😍')

    @commands.command()
    async def ping(self, ctx):
        """
        Shows network pings.
        :param ctx: Passed by discord.
        :return: None
        """

        await ctx.send(f'N/W Ping is : {round(self.client.latency * 1000)} ms')

    @commands.command(aliases=['google', 'lookfor', 'look4', 'find'])
    async def search(self, ctx, *, query):
        """
        This command is used to search content on Google. Pass a query along with this command and the bot will scrape
        Google's organic search results ad will return first result. (by default only one result is returned)

        :param ctx: Passed by discord.
        :param query: Query to be searched on Google.
        :return: None / Sends results found on google in respective channel.
        """

        crawler = GoogleWebCrawler(query)
        results = crawler.fetch_webpage(manage_cache=False)
        heading = list(results[0].keys())[0]
        content = list(results[0].values())[0]
        link = list(results[1].values())[0]

        c = f"This is what i found so far...\n\n{heading}\n{content}\n\nhttps://{link}"
        await ctx.send(
            f"{c}"
        )

    @commands.command(name='myinsignia')
    async def show_insignia(self, ctx):
        """
        This method is to show user's information thru embeds
        :param ctx: Passed by discord.
        :return: None.
        """

        author = ctx.author
        author_name = author.display_name
        author_avatar = author.avatar_url
        author_color = author.color
        author_level = 10

        embed = InsigniaEmbeds().get_my_insignia(
            author_name, author_avatar, author_color, author_level
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Members(client))
