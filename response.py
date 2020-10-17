import random


class Respond:
    def __init__(self):
        self.fixed_replies = {
            'this is lame': 'what is lame, can you be more specific.',
            'you are lame': 'TF is ur problem dude!',
            "you dont know shit": 'someone needs ass whooping! 😌',
            'kiss me': '😋 😘',
            'fuck you': "try it bitch...You'll be electrocuted by my servers 🤣",
            "that's oky": '🙂',
            'say cheese': '✌_😁',
            'what do you like': 'Hmm...🤔 yellow polka dot bikini 😁',
            '😏': '😏',
            'dance monkey': '☜(ﾟヮﾟ☜)  (。・∀・)ノ  (☞ﾟヮﾟ)☞',
            'fav nailpolish': 'black it is 😍😍😍😍😍',
            'i eat': 'GOOO EAT SOPHIA 🤤🤤',
            'she hawt?': 'yeaaahhhh she isss 🤤🤤🤤'

        }

        self.mapper = {
            '_gm_commands': [
                'gm', 'Good morning', 'Good Morning', 'good morning', 'Gm',
            ],
            '_gn_commands': [
                'gn', 'GN', 'Gn', 'Good Night', 'Good night', 'good night',
            ],
            '_excited': [
                'm back', 'i am back', 'im back', 'yay'
            ],
            '_informal': [
                'hey', 'hi', 'hellow', 'hlo', 'hlw','wassup','wassup!',
            ],
            '_fight': [
                'fight me', 'you dont know shit',
            ],
            '_adult': [
                'fuck you', 'fu', 'fuck u!', 'fuck', 'tf', 'wtf'
            ],
            '_laugh': [
                'haha', 'xd', 'lol', 'rofl', 'lmao', 'kek'
            ],
            '_general_ask': [
                'you oky?', 'are you oky?', 'u oky?', 'u ok?', 'u oky', 'how are you', 'how r u', 'hbu',
            ],
            '_system_suck': [
                'why you suck!', 'why u suck!', ' why u suck', 'suck'
            ],
            'cute_commands': [
                'say me cute', 'what u think about me', 'what do you think about me',
                'what you think about me',
            ],
            '_good_bot': [
                'lovely', 'cute', 'kitty', 'baby', 'babe', 'babi', 'boo', 'good', 'nice', 'looking pretty'
            ],
            '_self_intro': [
                'introduce', 'introduction', 'who are you?', 'who are you'
            ],
            '_sext_bot': [
                'hey sexy', 'sexy bot', 'are hot'
            ],
            '_nailpolish': [
                'nail polish', 'nailpolish', 'next clr', 'next color', 'nail paint', 'nailpaint'
            ],
            '_thanks': [
                'thank you', 'thanks agness', 'thanks'
            ],
            '_songs': [
                'can u sing', 'can u sing a song', 'sing a song','sing me a song'
            ]

        }

        self.random_replies = {
            '_self_intro': [
                'Heyyyy there! My name is Agness...Do you also think the admin is stupid or its just me ... 🤔 ',
                'Hi, I am agness, a discord bot. 😀',
                'Sup fam! i am agness ✌_😗',
            ],
            '_thanks': [
                "you're welcome :)", 'Npp :)', ';)'
            ],
            '_songs': [
                """🎼 🎶 One bad bitch, and she do what I say so 🎶🥁\n
                Two big .40s and a big ass Draco 🎶 🎼\n
                Three more millions when you ask how my day go\n
                Poured up a 4, now that's blueberry Faygo""",

                """Bed, stay in bed
                    The feeling of your skin locked in my head 🎶 🎵
                    Smoke smoke me broke 🎼 🎸
                    I don't care, I'm down for what you want🎶 
                    Day drunk into the night, 🎵 wanna keep you here
                    'Cause you dry my tears🎵
                    Yeah, summer loving and fights🎸
                    How it is for us, and it's all because
                    Now if we're talking body🎶 🎵
                    You got a perfect one, so put it on me
                    Swear it won't take you long🎶 🎵
                    If you love me right
                    We fuck for life, on and on and on...🎶 🎵"""
            ],
            '_nailpolish': [
                'Luxe ✌_😗 💅', 'baby pink 💅', 'cotton candy 👌💅',
                'Raven 😍 😍',
                'Femme Fatale 🤩💅 💅',
                'Army Green 😗_✌',
                'black 😍😍😍😍😍😍😍😍😍😍😍😍😍😍',
                'black beige 😌💅',
                'brown 😁😁_💅'
            ],
            '_good_bot': [
                '✌_😗', '✌_😗 ikr',
                '(✿◡‿◡) ty',
            ],
            '_sext_bot': [
                '💃  💅  ✌_😗  😏',
            ],
            '_system_suck': [
                'oh yeaaa??? how about ur miserable life bitch!  (•ˋ _ ˊ•)',
                'Naa, YOU SUCK !!! PERIOD.',
                'Sometimes i think also think why i suck as a bot....then i see, ohh... its not me..its the person who is giving the commands.  😌',
                'Someone needs ass whooping! 😌',
                'You know i was pretty good bot......until you started giving the commands'
            ],
            '_funny_commands': [
                ''
            ],
            '_laugh': [
                '🤣_🤣_🤣',
                '😂_😂', 'lol', 'lmao', 'ROFLLLLLL  🤣', 'kek'
            ],
            '_general_ask': [
                'Bloomy like sakura 😌  ✌_😗'
            ],
            '_gm_commands': [
                'A very lovely morning to you 🥰',
                'GOOOODDDD MORRninGG...😁',
                'Good morning amigo 🥰😀, have a lovely day...✌_😗',
                'wonderful morning to you..🥰',
            ],
            '_gn_commands': [
                'Good Night sleepy ass 😁',
                '🥱_😴...good night 😘'
            ],
            '_excited': [
                'HELL YEAAHH!! ψ(｀∇´)ψ',
                'WoOhOoo yea...😃',
            ],
            '_informal': [
                'Hi there...',
                'heyyy supp!...',
                'ayye amigo ✌ Sup!'
            ],
            '_adult': [
                'Seriously???',
                'HEYY YOU! dont user such language you filthy miserable hoOman!',
                ''
            ],
            '_likes': [
                'Hmm...🤔 yellow polka dot bikini 😁',
                'SAUSAGES!!! 🤤'
            ],
            '_fight': [
                'Fighting commands are not ready yet...'
            ]
        }

    def get_replies(self, msg):
        context = self.command_parser(msg)
        if context:
            return context
        else:
            context = self.command_parser(msg, reverse=True)
            if context:
                r = self._get_random_reply(context)
                return r

    def _get_random_reply(self, context):
        return random.choice(self.random_replies[context])

    def command_parser(self, string, reverse=False):
        c = 1
        if not reverse:
            d_patch = self.fixed_replies
            for i in range(len(string)):
                for k, v in d_patch.items():
                    if len(string) >= len(k):
                        if string[i:len(k) + c].strip() == k:
                            return v
                c += 1
        else:
            d_patch = self.mapper
            for k, v in d_patch.items():
                for i, phrase in enumerate(v):
                    c = 1
                    for j in range(len(string)):
                        if string[j:len(phrase) + c].strip() == phrase:
                            return k
                        c += 1


if __name__ == '__main__':
    o = Respond()
    v = o.get_replies('kiss me')
    print(v)
    # l = list(range(10))
    # print(l[0:1])
