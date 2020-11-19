import sys
from discord.ext import commands
from AGNESS_BOT.settings import configs
from discord.ext.commands import context
import asyncio
import functools


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


def show_typing(interval=configs.TYPING_INTERVAL):
    assert any([isinstance(interval, int), isinstance(interval, float)])

    def top_wrapper(fun):
        @functools.wraps(fun)
        async def wrapper(*args, **kwargs):
            if configs.SHOW_TYPING:
                for ctx in args:
                    if isinstance(ctx, context.Context):
                        async with ctx.typing():
                            await asyncio.sleep(interval)
            return await fun(*args, **kwargs)

        return wrapper

    return top_wrapper


__all__ = [
    "check_valid_channel",
    "export", "show_typing"
]
