import sys, os

sys.path.append(os.path.expanduser('~/bot_project/'))  # This is for my linux server O_o

from AGNESS_BOT.bot import bot
from discord.ext import commands
from AGNESS_BOT import (
    logger,
    configs,
    custom_help_cmd,
    EventEmbeds,
    member_join_self_verification
)

embed_msgs = EventEmbeds()

putlog = logger.get_custom_logger(__name__)

putlog.info("+-------------------------------+")
putlog.info("| Spinning Up...  STATUS : OK!  |")
putlog.info("+-------------------------------+\n")

TALK_AGNESS = False
active_chat = list()

DEFAULT_ROLE = configs.DEFAULT_ROLE
ADMIN_ROLE = configs.ADMIN_ROLE
COGS = configs.COGS
COGS_DIR = configs.COGS_DIR


@bot.listen('on_message')
@member_join_self_verification(
    bot=bot, logger=putlog,
    self_verification=configs.MEMBER_JOIN_SELF_VERIFICATION,
    verification_venue_channel=configs.FIRST_REDIRECT_CHANNEL
)
async def on_message(message, verification_complete=None):
    msg = str(message.content).lower()
    author_discriminator = message.author.discriminator
    channel = message.channel.id

    if message.author == bot.user:
        return

    if verification_complete is not None:
        if verification_complete:
            await message.author.send(embed=embed_msgs.member_verification_complete())
            return
        else:
            await message.channel.send(f'Ohow... Your 4-digit no. does not match your user discriminator.\n'
                                       f'Your discriminator is **{author_discriminator}**')
            return


@commands.has_role(DEFAULT_ROLE)
@bot.command(aliases=['h', 'hlp'])
async def help(ctx):
    author = ctx.message.author
    author_roles = [role.name for role in author.roles]
    if 'Admin' in author_roles:
        cmds, aliases = custom_help_cmd('admin')
        await ctx.send(embed=cmds)
        await ctx.send(embed=aliases)
    elif 'Staff' in author_roles:
        cmds, aliases = custom_help_cmd('staff')
        await ctx.send(embed=cmds)
        await ctx.send(embed=aliases)
    elif 'Member' in author_roles:
        cmds, aliases = custom_help_cmd('member')
        await ctx.send(embed=cmds)
        await ctx.send(embed=aliases)
    else:
        pass


@commands.has_role(ADMIN_ROLE)
@bot.command(aliases=['lcog'])
async def load_exts(ctx, *, extension):
    putlog.info(f'Cog : {extension}    Loading...')
    await ctx.send(f'Cog : {extension}    Loading...')
    try:
        bot.load_extension(f'{COGS_DIR + extension}')
        await ctx.send(f'Cog : {extension}    Loaded Successfully!')
        putlog.info(f'Cog : {COGS_DIR + extension}    OK!')
    except Exception as e:
        putlog.exception(e)
        await ctx.send(f'Cog : {extension}    Load Failed! ❌')
        putlog.error(f'Cog : {COGS_DIR + extension}    LOAD FAILED!')


@commands.has_role(ADMIN_ROLE)
@bot.command(aliases=['ulcog'])
async def unload_exts(ctx, *, extension):
    putlog.info(f'Cog : {extension}    UnLoading...')
    await ctx.send(f'Cog : {extension}    UnLoading...')
    try:
        bot.unload_extension(f'{COGS_DIR + extension}')
        await ctx.send(f'Cog : {extension}    UnLoaded Successfully!')
        putlog.info(f'Cog : {COGS_DIR + extension} Unloaded    OK!')
    except:
        await ctx.send(f'Cog : {extension}    UnLoad Failed! ❌')
        putlog.error(f'Cog : {COGS_DIR + extension}    UNLOAD FAILED!')


@commands.has_role(ADMIN_ROLE)
@bot.command(aliases=['ulacog'])
async def unload_all_ext(ctx):
    putlog.warning(f'UnLoading All Extensions...')
    await ctx.send(f'UnLoading All Extensions...')

    for extension in COGS:
        try:
            bot.unload_extension(f'{COGS_DIR + extension}')
            await ctx.send(f'Cog : {extension}    UnLoaded Successfully!      OK!')
            putlog.info(f'Cog : {COGS_DIR + extension} Unloaded    OK!')
        except:
            await ctx.send(f'Cog : {extension}    UnLoad Failed! ❌')
            putlog.error(f'Cog : {COGS_DIR + extension}    UNLOAD FAILED!')
    await ctx.send('Done')


@commands.has_role(ADMIN_ROLE)
@bot.command(aliases=['lacog'])
async def load_all_ext(ctx):
    putlog.warning(f'Loading All Extensions...')
    await ctx.send(f'Loading All Extensions...')
    for extension in COGS:
        try:
            bot.load_extension(f'{COGS_DIR + extension}')
            await ctx.send(f'Cog : {extension}    Loaded Successfully!       OK!')
            putlog.info(f'Cog : {COGS_DIR + extension} loaded    OK!')
        except:
            await ctx.send(f'Cog : {extension}    Load Failed! ❌')
            putlog.error(f'Cog : {COGS_DIR + extension}    LOAD FAILED!')
    await ctx.send('Done')


@commands.has_role(ADMIN_ROLE)
@bot.command(aliases=['rlcog'])
async def reload_ext(ctx, *, ext):
    putlog.warning(f'Reloading command for {ext} received.')
    try:
        putlog.info(f'Reloading {ext}...')
        bot.reload_extension(f'{COGS_DIR + ext}')
        putlog.info(f'{ext} Loaded!')
        await ctx.send(f'{ext} ReLoaded! ✅')
    except Exception as e:
        putlog.exception(e)
        await ctx.send(f'Reloading of {ext} Failed! ❌')


@commands.has_role(ADMIN_ROLE)
@bot.command(aliases=['rlallcog'])
async def reload_all_exts(ctx):
    putlog.info('Reloading cogs...')
    await ctx.send('Reloading cogs...')
    putlog.warning('Unloading COGS...')
    for cog in COGS:
        try:
            bot.unload_extension(COGS_DIR + cog)
            putlog.info(f'{COGS_DIR + cog} Unloaded successfully...      OK!')
        except:
            putlog.error(f'{COGS_DIR + cog} FAILED to unload...')

    putlog.warning('Loading COGS...')
    for lcog in COGS:
        try:
            bot.load_extension(COGS_DIR + lcog)
            putlog.info(f'{COGS_DIR + lcog} Loaded Successfully...      OK!')
        except:
            putlog.error(f'{COGS_DIR + lcog} FAILED to load...      FAILED!')
    await ctx.send('COGs Loaded!')
    putlog.info('-' * 40)


bot.run()
