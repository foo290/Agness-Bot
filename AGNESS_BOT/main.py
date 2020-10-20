from AGNESS_BOT.bot import bot
from AGNESS_BOT.global_configs import HOT_WORD
from AGNESS_BOT.user_interaction.response import Respond

respond_to_user = Respond()

TALK_AGNESS = False
active_chat = list()


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
    print(active_chat)
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


bot.run()
