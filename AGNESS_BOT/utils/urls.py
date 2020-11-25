"""
This module does not abide charecter length rule of 79 charecter of PEP 8 because of long raw url links.

"""

from .decorators import export
import random


@export
class GetUrl:
    def __init__(self):
        self.static_urls = {
            # Events gifs
            'wc_gif': "https://firebasestorage.googleapis.com/v0/b/discord-bot-294607.appspot.com/o/bot%2Fgifs%2Fother_gifs%2Fwelcome%20gifs%2Fanime_cheer.gif?alt=media&token=f5618220-d975-4a3e-9f3e-6df4134986b3",
            'bye_gif': '',
            'wc02_gif': 'https://firebasestorage.googleapis.com/v0/b/discord-bot-294607.appspot.com/o/bot%2Fgifs%2Fother_gifs%2Fwelcome%20gifs%2Fwelcome.gif?alt=media&token=2f02e96f-1d8b-4dbf-8773-fd79cd23606c',


            # Embed gifs
            'rainbow_divider': 'https://firebasestorage.googleapis.com/v0/b/discord-bot-294607.appspot.com/o/bot%2Fgifs%2Fother_gifs%2FAS_divider.gif?alt=media&token=9d5aa995-7a36-4cc5-b92e-a19bd5c03143',
        }

        self.dynamic_urls = {
            'slap': [
                'https://firebasestorage.googleapis.com/v0/b/myportfolio-366ad.appspot.com/o/discord-dependencies%2Foneslap-man.gif?alt=media&token=08be9a03-fb61-47bb-b5aa-f782b3269158',
            ],
            'pet': [
                'https://firebasestorage.googleapis.com/v0/b/myportfolio-366ad.appspot.com/o/discord-dependencies%2Fpat_008.gif?alt=media&token=04783e71-75af-4a52-8009-2b26c9c5ab8c'
            ]
        }

    def __getattr__(self, item, dynamic=False):
        if not dynamic:
            return self.static_urls[item]
        return random.choice(self.dynamic_urls[item])

    @classmethod
    def get(cls, key, dynamic=False):
        return cls().__getattr__(key, dynamic)


if __name__ == '__main__':
    print(GetUrl.get('slap', dynamic=True))
