import sys
import discord
from discord.ext import commands
from AGNESS_BOT.settings import configs
from discord.ext.commands import context
import asyncio
import functools


def export(fn):
    """
    A decorator function, used to export selected components from a module.
    Put this deco on any component you want to export and it will add component's name in the module __all__ list.
    :param fn:
    :return:
    """
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
    """
    A predicate for music channel to ensure the commands are being restricted to music channel.
    :param ctx:
    :return:
    """
    if configs.RESTRICT_CMDS_TO_MUSIC_CHANNEL:
        return ctx.channel.id == configs.MUSIC_CMD_CHANNEL
    return True


# A decorator to check Music commands are being called in music channel only.
check_valid_channel = commands.check(predicate)


def show_typing(interval=configs.TYPING_INTERVAL):
    """
    A decorator which can be used on functions/methods on which you want to show bot's typing status.
    :param interval: A typing interval for how long you want to show bot typing... , default is set in settings.py
    :return: un_executed function.
    """
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


def member_join_self_verification(**kw):
    """
    **********************  MEMBER SELF VERIFICATION SYSTEM  ********************************************

    This deco is a part of additional user SELF VERIFICATION SYSTEM in which newly joined user have to type,
     "i agree ####" in welcome channel where #### is the discriminator.

    This deco is also depends on your server configuration of roles. Here is how this is configured in my server :

        -> Make a role name "Unverified" and restrict the permissions according to your needs.
            --> In my case, The unverified user is only allow to see welcome and rules channel.

        -> When a member joins, The bot will assign this role to member.
        -> Member have to type "i agree ####" where #### is the discriminator of member.
        -> After this process, if successful, the member will be assigned "DEFAULT_ROLE" which is defined in settings.py

        All these tasks of assigning and removing roles are been taken care of by this decorator.

        **** IF YOU DONT WANT THIS BEHAVIOUR, SET "MEMBER_JOIN_SELF_VERIFICATION" TO False IN Settings.py ****

    :param kw:
            self_verification: bool = if true, will setup the step verification for newly joined user.
            verification_venue_channel: int = The channel where you want the user to send verification text, ex: welcome
            bot: The instance of bot.
            logger: custom logger, "putlog"

    :return: un executed on_message function.
    """

    self_verification = kw.get('self_verification')
    verification_venue_channel = kw['verification_venue_channel']
    bot = kw['bot']
    putlog = kw['logger']

    def wrapper_1(fun):
        @functools.wraps(fun)
        async def wrapper_2(*args, **kwargs):
            if self_verification:
                message = args[0]
                if isinstance(message, discord.Message):
                    channel = message.channel.id
                    msg_content = str(message.content).lower()
                    author = message.author
                    author_discriminator = message.author.discriminator

                    if (
                            channel == verification_venue_channel and
                            configs.UNVERIFIED in [role.name for role in author.roles] and
                            message.author != bot.user

                    ):
                        if author_discriminator == msg_content.strip().split(' ')[-1]:

                            putlog.info(
                                f'user : {message.author.display_name} verification complete.'
                                f' Assigning default role now...'
                            )

                            role_to_remove = discord.utils.get(message.author.guild.roles, name=configs.UNVERIFIED)
                            role_to_assign = discord.utils.get(message.author.guild.roles,
                                                               name=configs.DEFAULT_ROLE)

                            putlog.debug(f'Removing {role_to_remove} from {author}')
                            await author.remove_roles(role_to_remove)
                            putlog.debug(f'Role {role_to_remove} removed from {author}')

                            putlog.debug(f'Assigning {role_to_assign} to user {author}')
                            await author.add_roles(role_to_assign)
                            putlog.info(f"{message.author} has assigned with {role_to_assign} role.")

                            return await fun(*args, verification_complete=True, **kwargs)
                        else:
                            return await fun(*args, verification_complete=False, **kwargs)

            return await fun(*args, **kwargs)

        return wrapper_2

    return wrapper_1


__all__ = [
    "check_valid_channel",
    "export", "show_typing", "member_join_self_verification"
]
