import sys
from discord.ext import commands
from AGNESS_BOT.settings import configs


def export(fn):
    mod = sys.modules[fn.__module__]
    if hasattr(mod, '__all__'):
        name = fn.__name__
        all_ = mod.__all__
        if name not in all_:
            all_.append(name)
    else:
        mod.__all__ = [fn.__name__]
    return fn


async def predicate(ctx):
    if configs.RESTRICT_CMDS_TO_MUSIC_CHANNEL:
        return ctx.channel.id == configs.MUSIC_CMD_CHANNEL
    return True


# A decorator to check Music commands are being called in music channel only.
check_valid_channel = commands.check(predicate)

__all__ = [
    "check_valid_channel",
    "export"
]
