from AGNESS_BOT.utils.custom_exceptions import *
from functools import wraps
from discord.ext import commands
from AGNESS_BOT.settings import configs

channel_id = configs.MUSIC_CMD_CHANNEL
RESTRICTION = configs.RESTRICT_CMDS_TO_MUSIC_CHANNEL


def check_empty_queue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self, *_ = args
        if self._Queue__queue:
            return func(*args, **kwargs)
        raise QueueIsEmpty

    return wrapper


def check_connected_to_channel(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self, *_ = args
        if not self.is_connected:
            return func(*args, **kwargs)
        raise AlreadyConnectedToChannel

    return wrapper


async def predicate(ctx):
    if RESTRICTION:
        return ctx.channel.id == channel_id
    return True

# A decorator to check Music commands are being called in music channel only.
check_valid_channel = commands.check(predicate)
