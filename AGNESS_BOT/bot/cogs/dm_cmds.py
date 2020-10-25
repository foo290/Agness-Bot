from discord.ext import commands


class DM(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.dm_only()
    @commands.command(aliases=['clsdm'])
    async def clear_dm(self, ctx, limit=5):
        async for message in self.client.get_user(ctx.message.author.id).history(limit=limit + 1):
            if message.author.id == self.client.user.id:
                await message.delete()


def setup(client):
    client.add_cog(DM(client))
