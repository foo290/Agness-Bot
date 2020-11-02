from AGNESS_BOT.bot import bot
from AGNESS_BOT.user_interaction.response import Respond
from discord.ext import commands
from AGNESS_BOT import (
    logger,
    configs,
    custom_help_cmd,
)


channel_id = configs.MUSIC_CMD_CHANNEL
putlog = logger.get_custom_logger(__name__)

putlog.info("+-------------------------------+")
putlog.info("| Spinning Up...  STATUS : OK!  |")
putlog.info("+-------------------------------+\n")

respond_to_user = Respond()

TALK_AGNESS = False
active_chat = list()

HOT_WORD = configs.HOT_WORD
DEFAULT_ROLE = configs.DEFAULT_ROLE
ADMIN_ROLE = configs.ADMIN_ROLE
COGS = configs.COGS
COGS_DIR = configs.COGS_DIR


def check_hotword(msg, author, message):
    global TALK_AGNESS

    if msg == HOT_WORD:
        if message.author.discriminator not in active_chat:
            active_chat.append(author)
        TALK_AGNESS = True
        return True


def check_active_users(l):
    try:
        i = l[0]
        return True
    except IndexError:
        return False


@bot.listen('on_message')
async def on_message(message):
    global TALK_AGNESS, active_chat
    msg = str(message.content).lower()
    author = message.author.discriminator
    nickname = str(message.author).split("#")[0]

    if TALK_AGNESS:
        if message.author == bot.user:
            return
        if author in active_chat:  # If user has already said hot word
            if author == message.author.discriminator:
                if msg == 'bye agness':
                    active_chat.remove(author)
                    if not check_active_users(active_chat):  # if no one is talking to agness
                        TALK_AGNESS = False
                    await message.channel.send(f"Bye {nickname}")
                else:
                    response = respond_to_user.get_replies(msg)  # Get reply
                    if response:
                        await message.channel.send(response)
                    else:
                        pass  # Missed Talks
        else:
            if check_hotword(msg, author,
                             message):  # If user is not in active chat with agness but msg is hot word
                await message.channel.send(f'Hellow {nickname}')
    else:
        if check_hotword(msg, author, message):
            await message.channel.send(f'Hellow {nickname}')

        else:
            if msg in ['gm', 'good morning agness', 'good morning']:
                await message.channel.send('Good Morning 🥰')
            elif msg in ['gn', 'good night agness', 'good night']:
                await message.channel.send('Good Night 🥰')


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
async def reload_exts(ctx):
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
