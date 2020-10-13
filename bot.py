import discord
from discord.ext import commands
import random
import asyncio
import os
import datetime
from web_crawlers import GoogleWebCrawler
from response import Respond
import sys

respond_to_user = Respond()


def write_command(ctx):
    with open('missed_commands.txt', 'a') as file:
        file.write(ctx)


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
async def on_join(member):
    print(f'Welcome {member}, glad to see you popped up here :D')


@bot.event
async def on_left(member):
    print(f'{member} has left')


@bot.command()
async def send_msg(ctx, msg):
    await ctx.author.send('This is msg')

b = '760068374268346390'

@bot.listen('on_message')
async def normal_reply(message):
    global talk_agness, TALK_GPT
    # print(message.guild)
    # print(message.author.dmChannel)
    print(message)


    # print(message)
    # if  message.guild is None and message.author != bot.user:
    #
    #     print(message.channel)
    #     await message.author.send('This is msg')

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

    user_msg = str(message.content).lower()

    if user_msg == hot_word:
        talk_agness = True
        await message.channel.send(f'Hellow {str(message.author).split("#")[0]}')

    if user_msg == 'cls':
        async for message in bot.get_user(734861106698387548).history(limit=20):
            if message.author.id == bot.user.id:
                await message.delete()
                # await asyncio.sleep(0.5)
        # await message.channel.purge(check=lambda m: m.author == bot.user)

    else:
        if message.content in ['gm', 'good morning agness', 'good morning']:
            await message.channel.send('Good Morning 🥰')

# async for msg in channel.history():
#     if msg.author == client.user:
#         await msg.delete()


@bot.command()
async def ping(ctx):
    await ctx.send(f'N/W Ping is : {round(bot.latency * 1000)} ms')


@bot.command(aliases=['dog'])
async def _dog(ctx, *, person):
    await ctx.send(f'Stfu you son of a bitch {person}!')


@bot.command(aliases=['cls'])
async def clear(ctx, amount=4):
    await ctx.channel.purge(limit=amount + 1)



@bot.command(aliases=['wc'])
async def welcome(ctx, *, person):
    await ctx.send(f'Welcome aboard {person.title()}, This is a special welcome from admin as well as from me 😃')


@bot.command(aliases=['agness'])
async def intro(ctx, *, person):
    await ctx.send(f'Hey {person.title()}, My name is Agness. I like peanut butter 😁😍')


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


@bot.command()
async def say(ctx, word, person):
    await ctx.send(
        f"{word} {person}"
    )


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


#
# def convert_timefmt(time, _12hours=True):
#     # try:
#         if not _12hours:
#             fmt = datetime.datetime.strptime(time, "%I:%M %p")
#             _24hourtimefmt = datetime.datetime.strftime(fmt, "%H:%M")
#             return _24hourtimefmt
#
#         d = datetime.datetime.strptime(time, "%H:%M")
#         _12hourtimefmt = d.strftime("%I:%M %p")
#         return _12hourtimefmt
# except:
#     return False

# def valid_timeformat(time,)

def calculate_time(time_, unit):
    if unit in ['hr', 'hour', 'hours']:
        return time_ * 3600
    elif unit in ['mins', 'min', 'minute', 'minutes', 'm']:
        return time_ * 60
    elif unit in ['sec', 'seconds', 'secs', 's']:
        return time_
    else:
        return False
    # elif unit in ['am', 'pm']:
    #     _24hourtimefmt = ':'.join(str(datetime.datetime.today().time()).split(':')[:-1])
    #     _12hourtimefmt = convert_timefmt(_24hourtimefmt)
    #     if not _12hourtimefmt:
    #         return False
    #     current_noon = _12hourtimefmt.split(' ')[-1]
    #
    #     if unit.upper() != current_noon:
    #         current_hour, current_minute = _24hourtimefmt.split(':')
    #
    #         given_12to24 = convert_timefmt(f'{time_} {unit}', _12hours=False)
    #         if not given_12to24:
    #             return False
    #         reminder_hour, reminder_minute = given_12to24.split(':')
    #
    #         time_difference_hours = abs(int(reminder_hour)-int(current_hour))
    #         # time_difference_minutes = abs(int(reminder_minute)+int(current_minute))
    #         # print(time_difference_hours, time_difference_minutes)
    #         finnal_time = time_difference_hours*3600 + reminder_minute*60
    #         return finnal_time
    #
    #
    #     else:
    #         current_hour, current_minutes = int(datetime.datetime.today().now().hour), int(datetime.datetime.today().now().minute)
    #         given_time = convert_timefmt(f"{time_} {unit}", _12hours=False).split(':')
    #         # print(fii, '-------------------------------------')
    #
    #         # given_time = time_.split(':')
    #         # print(given_time)
    #
    #         # if len(given_time)==1:
    #         #     print('boop')
    #         #     reminder_hour, reminder_minute = given_time[0], 0
    #         # elif len(given_time)==2:
    #
    #         reminder_hour, reminder_minute = given_time
    #         reminder_hour = int(reminder_hour)
    #         reminder_minute = int(reminder_minute)
    #         if reminder_minute == 0:
    #             reminder_minute = current_minutes
    #         # print(reminder_hour-current_hour)
    #         print(reminder_minute)
    #
    #         set_reminder_hour = current_hour + abs(reminder_hour-current_hour)
    #         # set_reminder_minute = current_minutes + abs(reminder_minute-current_minutes)
    #         reminder_set_at = convert_timefmt(f"{set_reminder_hour}:{reminder_minute}")
    #         # print(reminder_hour, current_hour,)
    #
    #
    #         time_diffrence_hours = abs(int(reminder_hour - current_hour))
    #         time_diffrence_minutes = abs(int(reminder_minute - current_minutes))
    #         print(time_diffrence_minutes)
    #
    #         final_time = (time_diffrence_hours*3600) + (time_diffrence_minutes*60)
    #         return final_time


# def check_time(time_):
#     time_split = time_.split(':')
#     hour = int(time_split[0])
#     minute = int(time_split[1])
#     if hour > 12 or hour <= 0:
#         return False
#     if minute > 60 or minute < 0:
#         return False
#     return True
#
# def valid_timefmt(time):
#     if len(time) == 1:
#         return f'0{time}:00'
#     elif len(time) == 2:
#         return f'{time}:00'
#     else:
#         return time


@bot.command(aliases=['remind', 'set_reminder'])
async def remind_me(ctx, task, time, unit='min', *meta):
    try:
        seconds = int(calculate_time(int(time), str(unit).lower()))
        print(seconds)
        await ctx.send(f"Reminder Set for    ---->     {task}. \n\nI'll remind you after {time} {unit}.")

        await asyncio.sleep(seconds)

        await ctx.send(
            f"\nREMINDER ALERT ! Hey <@{str(ctx.author.id)}> ```\n\nYou told me {time} {unit}"
            f" ago to remind you for   ---->    '{task}'\n\n```")
    except:
        await ctx.send(f'Something is not as what i expected...🤔... Unable to set reminder.'
                       f'\nTry again with right command format  : \n'
                       f'```.remind<space>"Your_Task_Name_Here"<space>TIME<space>Unit(mins or secs or hours)```')


bot.run(BOT_TOKEN)



# f = valid_timefmt('4:61pm','')
# if f:
#     if check_time(f):
#         print(f)
#     else:
#         print('pissed')
