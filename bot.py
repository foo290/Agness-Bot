import discord
from discord.ext import commands
import asyncio
import os
from web_crawlers import GoogleWebCrawler
from response import Respond

respond_to_user = Respond()

CHANNEL_MUTE = False


def write_command(ctx):
    with open('missed_commands.txt', 'a') as file:
        file.write(ctx)


def calculate_time(time_, unit):
    if unit in ['hr', 'hour', 'hours', 'h']:
        return time_ * 3600
    elif unit in ['mins', 'min', 'minute', 'minutes', 'm']:
        return time_ * 60
    elif unit in ['sec', 'seconds', 'secs', 's']:
        return time_
    elif unit in ['days', 'day', 'd']:
        return time_ * 86400
    else:
        return False


BOT_TOKEN = os.environ.get('DC_BOT_TOKEN')
bot = commands.Bot(command_prefix='.')

intro_prefixes = ['hi', 'hello', 'hey', 'wassup!', 'wassup']
intro_prefixes += [i.title() for i in intro_prefixes]
hot_word = 'hey agness'

talk_agness = False


@bot.event
async def on_ready():
    print('Bot is ready')


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")
    await member.add_roles(role)


@bot.event
async def on_member_remove(member):
    print(f'{member} has left')


@bot.listen('on_message')
async def normal_reply(message):
    global talk_agness, TALK_GPT

    print(message)

    if talk_agness:
        if message.author == bot.user:
            return
        else:
            msg = str(message.content).lower()
            if msg.lower() == 'bye agness':
                talk_agness = False
                await message.channel.send('bye...( ﾟдﾟ)つ Bye')
            f = respond_to_user.get_replies(msg)
            if f:
                await message.channel.send(f)
            else:
                content = f"Missed Command :: {msg} :: by :: {message.author}\n"
                write_command(content)
    else:
        user_msg = str(message.content).lower()

        if user_msg == hot_word:
            talk_agness = True
            await message.channel.send(f'Hellow {str(message.author).split("#")[0]}')

        if user_msg == 'cls':
            async for message in bot.get_user(734861106698387548).history(limit=10):
                if message.author.id == bot.user.id:
                    await message.delete()
        else:
            if user_msg in ['gm', 'good morning agness', 'good morning']:
                await message.channel.send('Good Morning 🥰')
            elif user_msg in ['gn', 'good night agness', 'good night']:
                await message.channel.send('Good Night 🥰')


@commands.has_role('Member')
@bot.command()
async def ping(ctx):
    await ctx.send(f'N/W Ping is : {round(bot.latency * 1000)} ms')


@commands.has_role('Member')
@bot.command(aliases=['dog'])
async def _dog(ctx, *, person):
    await ctx.send(f'Stfu you son of a bitch {person}!')


@commands.has_permissions(manage_messages=True)
@bot.command(aliases=['cls'])
async def clear(ctx, amount=4):
    try:
        await ctx.channel.purge(limit=amount + 1)
    except:
        await ctx.send('You are not allowed to use this command')


@commands.has_permissions(administrator=True)
@bot.command(aliases=['wc'])
async def welcome(ctx, *, person):
    await ctx.send(f'Welcome aboard {person.title()}, This is a special welcome from admin as well as from me 😃')


@commands.has_role('Member')
@bot.command(aliases=['agness'])
async def intro(ctx, *, person):
    await ctx.send(f'Hey {person.title()}, My name is Agness. I like peanut butter 😁😍')


@commands.has_role('Member')
@bot.command(aliases=['google', 'lookfor', 'look4', 'find'])
async def search(ctx, *, query):
    crawler = GoogleWebCrawler(query)
    results = crawler.fetch_webpage(manage_cache=True)
    print(results)
    heading = list(results[0].keys())[0]
    content = list(results[0].values())[0]
    link = list(results[1].values())[0]
    c = f"This is what i found so far...\n\n{heading}\n{content}\n\nhttps://{link}"
    await ctx.send(
        f"{c}"
    )


@commands.has_role('Member')
@bot.command()
async def say(ctx, word, person):
    await ctx.send(
        f"{word} {person}"
    )


@commands.has_role('Staff')
@bot.command(aliases=['eval'])
async def evaluate(ctx, *, cmd):
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


@bot.command()
@commands.has_role('Staff')
async def mute(ctx, member: discord.Member, time, unit='min', reason=None):
    print(ctx)
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


@commands.has_role('Staff')
@bot.command()
async def unmute(ctx, member: discord.Member):
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


@commands.has_role('Staff')
@bot.command(aliases=['silence!'])
async def shhh(ctx, *, time='5', unit='min'):
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

@commands.has_role('Staff')
@bot.command(aliases=['rm_silence!'])
async def unshhh(ctx):
    global CHANNEL_MUTE
    unmuted = discord.Embed(
        description=f"Silence removed! You can send messages now. ☑",
        colour=discord.Color.green()
    )
    unmuted.set_footer(text='UnMuted by : Administrator')

    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    CHANNEL_MUTE = False
    await ctx.send(embed=unmuted)


def get_reminder_embeds(p_user, s_user, task, time, unit):
    print()
    if s_user and str(s_user).startswith('<@!'):
        m_reminder_set = discord.Embed(
            title='Mutual Reminder',
            description=f"Hey {p_user}, you've set a reminder for {s_user}."
                        f" I'll keep in mind to remind you both.",
            colour=discord.Color.blurple()
        )
        m_reminder_set.add_field(name="Reminder for :", value=task, inline=False)
        m_reminder_set.add_field(name="Reminder Type :", value='Mutual (other user included)', inline=False)
        m_reminder_set.add_field(name="Time :", value=f"{time} {unit} remaining...", inline=False)
        m_reminder_set.set_footer(text='powered by : Agness')

        m_reminder_complete = discord.Embed(
            title="It's your reminder...",
            description=f"Hey {s_user}, {p_user} told me to remind you for your task.",
            colour=discord.Color.red()
        )
        m_reminder_complete.add_field(name="Task :", value=task, inline=False)
        m_reminder_complete.set_footer(text='powered by : Agness')
        return m_reminder_set, m_reminder_complete
    else:
        reminder_set = discord.Embed(
            title='Reminder',
            description=f"Hey {p_user}, I'll keep ur reminder in mind. {' ' * 10}",
            colour=discord.Color.blurple()
        )
        reminder_set.add_field(name="Reminder for :", value=task, inline=False)
        reminder_set.add_field(name="Time :", value=f"{time} {unit} remaining...", inline=False)
        reminder_set.set_footer(text='powered by : Agness')

        reminder_complete = discord.Embed(
            title="It's your reminder...",
            description=f"Hey {p_user}, Remember you told me to remind you for ur task.{' ' * 5}",
            colour=discord.Color.red()
        )
        reminder_complete.add_field(name="Task :", value=task, inline=False)
        reminder_complete.set_footer(text='powered by : Agness')

        return reminder_set, reminder_complete


@bot.command(aliases=['remind', 'set_reminder'])
async def remind_me(ctx, task, time, unit='min', s_user=None):
    print(ctx, task, time, unit, s_user)
    p_user = str(ctx.author).split('#')[0]
    r_set, r_complete = get_reminder_embeds(p_user, s_user, task, time, unit)
    try:
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


@commands.has_permissions(administrator=True)
@bot.command()
async def ban(ctx, member: discord.Member, reason=None):
    # try:
    banembed = discord.Embed(
        title='Ban User ❌ ',
        description=f"Permanent Ban Applied 👌 to {member.id}",
        colour=discord.Color.dark_red()
    )
    banembed.set_footer(text='powered by : Agness')
    await member.ban(reason=reason)
    await ctx.send(embed=banembed)


@commands.has_permissions(administrator=True)
@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    user_dis = member
    print('beep')

    for banned_entry in banned_users:
        user = banned_entry.user
        if user.discriminator == user_dis:
            await ctx.guild.unban(user)
            print(banned_entry)
            unbanembed = discord.Embed(
                title='Unban User ✅',
                description=f"{user.mention} is unbanned and allowed to interact.",
                colour=discord.Color.green()
            )
            unbanembed.set_footer(text='powered by : Agness')

            await ctx.send(embed=unbanembed)
            return
        else:
            print('not found')


@bot.command()
async def invite(ctx):
    link = await ctx.channel.create_invite(max_age=0)
    await ctx.send(link)



bot.run(BOT_TOKEN)
