import discord
from AGNESS_BOT.settings import COMMAND_PREFIX, BOT_NAME


def get_reminder_embeds(p_user, s_user, task, time, unit, type_='individual'):
    if type_ == 'mutual':
        m_reminder_set = discord.Embed(
            title='Mutual Reminder  ⏰',
            description=f"Hey {p_user}, you've set a reminder for {s_user}."
                        f" I'll keep in mind to remind you both.",
            colour=discord.Color.blurple()
        )
        m_reminder_set.add_field(name="Reminder for :", value=task, inline=False)
        m_reminder_set.add_field(name="Reminder Type :", value='Mutual (other user included)', inline=False)
        m_reminder_set.add_field(name="Time :", value=f"{time} {unit} remaining...", inline=False)
        m_reminder_set.set_footer(text=f'powered by : {BOT_NAME}')

        m_reminder_complete = discord.Embed(
            title="It's your reminder  ⏰...",
            description=f"Hey {s_user}, {p_user} told me to remind you for your task.",
            colour=discord.Color.red()
        )
        m_reminder_complete.add_field(name="Task :", value=task, inline=False)
        m_reminder_complete.set_footer(text=f'powered by : {BOT_NAME}')
        return m_reminder_set, m_reminder_complete
    else:
        reminder_set = discord.Embed(
            title='Reminder  ⏰',
            description=f"Hey {p_user}, I'll keep ur reminder in mind. {' ' * 10}",
            colour=discord.Color.blurple()
        )
        reminder_set.add_field(name="Reminder for :", value=task, inline=False)
        reminder_set.add_field(name="Time :", value=f"{time} {unit} remaining...", inline=False)
        reminder_set.set_footer(text=f'powered by : {BOT_NAME}')

        reminder_complete = discord.Embed(
            title="It's your reminder  ⏰...",
            description=f"Hey {p_user}, Remember you told me to remind you for ur task.{' ' * 5}",
            colour=discord.Color.red()
        )
        reminder_complete.add_field(name="Task :", value=task, inline=False)
        reminder_complete.set_footer(text=f'powered by : {BOT_NAME}')

        return reminder_set, reminder_complete


def custom_help_cmd(user_type='admin', client=None):
    if user_type == 'admin':
        admin_help = discord.Embed(
            title='Admin Help Commands!',
            description='These commands are only available to admins. \n(Commands available to lower roles are also available to admins.)',
            color=discord.Color.dark_magenta()
        )
        admin_help.add_field(
            name=f'{COMMAND_PREFIX}ban @user OR id',
            value='Ban a user by mention or by id.',
            inline=False
        )
        admin_help.add_field(
            name=f'{COMMAND_PREFIX}unban',
            value='UnBan a user by id.',
            inline=False
        )
        admin_help.add_field(
            name=f'{COMMAND_PREFIX}shh <time> <unit: (s, m, h, d)>',
            value='Mute the whole channel, only admins can message. '
                  'Default is for 5 mins but you can give desired time for mute like : shhh 10 m',
            inline=False
        )
        admin_help.add_field(
            name=f'{COMMAND_PREFIX}unshh',
            value='Unmute the channel. Reverts the actions of shhh command.',
            inline=False
        )
        admin_help.add_field(
            name=f'{COMMAND_PREFIX}loadcog <name>',
            value='Loads the given COG',
            inline=False
        )
        admin_help.add_field(
            name=f'{COMMAND_PREFIX}unloadcog <name>',
            value='Unloads the given COG',
            inline=False
        )
        admin_help.add_field(
            name=f'{COMMAND_PREFIX}reloadcog',
            value='Unload and the reloads all the COGs',
            inline=False
        )

        admin_help.set_footer(text='Admin commands')

        admin_aliases = discord.Embed(
            title='Commands Aliases!',
            description='These aliases can be used to execute respective commands.',
            color=discord.Color.magenta()
        )
        admin_aliases.add_field(
            name=f'{COMMAND_PREFIX}silence <time>  <unit: (s, m, h, d)>',
            value=f'{COMMAND_PREFIX}shh <time> <unit: (s, m, h, d)>',
            inline=False
        )
        admin_aliases.add_field(
            name=f'{COMMAND_PREFIX}rm_silence',
            value=f'{COMMAND_PREFIX}unshh',
            inline=False
        )
        admin_aliases.add_field(
            name=f'{COMMAND_PREFIX}loadcog <name>',
            value=f'{COMMAND_PREFIX}lcog <name>',
            inline=False
        )
        admin_aliases.add_field(
            name=f'{COMMAND_PREFIX}unloadcog <name>',
            value=f'{COMMAND_PREFIX}ulcog <name>',
            inline=False
        )
        admin_aliases.add_field(
            name=f'{COMMAND_PREFIX}reloadcog',
            value=f'{COMMAND_PREFIX}rlcog',
            inline=False
        )

        admin_aliases.set_footer(text='Admin commands aliases')

        return admin_help, admin_aliases

    elif user_type == 'staff':

        staff_help = discord.Embed(
            title='Staff Help Commands!',
            description='These commands are only available to Staff. \n'
                        '(Commands available to lower roles are also available to Staff.)',
            color=discord.Color.dark_magenta()
        )
        staff_help.add_field(
            name=f'{COMMAND_PREFIX}mute <@user> <time>',
            value='Mute a user for given amount of time. Default is 15 mins but you can give desired time like:  '
                  'mute @user 10 m',
            inline=False
        )
        staff_help.add_field(
            name=f'{COMMAND_PREFIX}unmute <@user>',
            value='Unmute a user',
            inline=False
        )
        staff_help.add_field(
            name=f'{COMMAND_PREFIX}warn <@user> <reason=Optional>',
            value='Warns a user. Displays the reason if given.',
            inline=False
        )
        staff_help.add_field(
            name=f'{COMMAND_PREFIX}clear <amount>',
            value='Deletes the given amount of messages. Default is 5.',
            inline=False
        )
        staff_help.add_field(
            name=f'{COMMAND_PREFIX}eval <expression>',
            value='Evaluates a given expression.',
            inline=False
        )
        staff_help.set_footer(text='Staff commands')

        staff_aliases = discord.Embed(
            title='Commands Aliases!',
            description='These aliases can be used to execute respective commands.',
            color=discord.Color.magenta()
        )
        staff_aliases.add_field(
            name=f'{COMMAND_PREFIX}clear <amount>',
            value=f'{COMMAND_PREFIX}cls <amount>',
            inline=False
        )
        staff_aliases.add_field(
            name=f'{COMMAND_PREFIX}warn <@user>',
            value=f'{COMMAND_PREFIX}w <@user>',
            inline=False
        )

        staff_aliases.set_footer(text='Staff commands aliases')

        return staff_help, staff_aliases

    elif user_type == 'member':

        member_help = discord.Embed(
            title='Members Help Commands!',
            description='These commands are available to all members. (Having a role Member)',
            color=discord.Color.dark_magenta()
        )
        member_help.add_field(
            name=f'{COMMAND_PREFIX}search <Query>',
            value='Scrapes google for given query. If the query is multiple words the use "" to wrap it.',
            inline=False
        )
        member_help.add_field(
            name=f'{COMMAND_PREFIX}invite',
            value='Creates a link for invite to this server.',
            inline=False
        )
        member_help.add_field(
            name=f'{COMMAND_PREFIX}set_reminder  <task>  <time>  <unit: (s, m, h, d)>  <@other user: Optional>',
            value='Creates a reminder for the given task and given user and '
                  'will ping the user on given time. Ping both user if mutual reminder is set.',
            inline=False
        )

        member_help.set_footer(text=f'{COMMAND_PREFIX}Members commands')

        member_aliases = discord.Embed(
            title='Commands Aliases!',
            description='These aliases can be used to execute respective commands.',
            color=discord.Color.magenta()
        )
        member_aliases.add_field(
            name=f'{COMMAND_PREFIX}search <Query>',
            value=f'{COMMAND_PREFIX}find, {COMMAND_PREFIX}look4,    {COMMAND_PREFIX}lookfor',
            inline=False
        )
        member_aliases.add_field(
            name=f'{COMMAND_PREFIX}set_reminder   <task>  <time>  <unit: (s, m, h, d)>  <@other user: Optional>',
            value=f'{COMMAND_PREFIX}remind',
            inline=False
        )

        member_aliases.set_footer(text='Member commands aliases')

        return member_help, member_aliases

    elif user_type == 'global_help' and client is not None:
        gb_hlp = discord.Embed(
            title='All Commands',
            description='These are the commands implemented.'
        )
        v = ''
        for cmd in client.commands:
            v += f'{cmd}\n'

        gb_hlp.add_field(name='Commands    : ', value=v)

        return gb_hlp
