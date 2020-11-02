from .bot import bot

bot.remove_command('help')  # Custom help command is configured in place of this.

__all__ = [
    bot,
]
