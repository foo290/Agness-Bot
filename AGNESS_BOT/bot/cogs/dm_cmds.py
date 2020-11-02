"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This extension module contains the commands which are accessible in DM.
"""
from discord.ext import commands


class DM(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.dm_only()
    @commands.command(aliases=['clsdm'])
    async def clear_dm(self, ctx, limit=5):
        """
        Deletes DM message by bot. (Only deletes message by bot, not by user.)
        :param ctx: Passed by discord.
        :param limit: Limit for message to be deleted in numbers. default is 5.
        :return: None
        """

        async for message in self.client.get_user(ctx.message.author.id).history(limit=limit + 1):
            if message.author.id == self.client.user.id:
                await message.delete()


def setup(client):
    client.add_cog(DM(client))
