import discord


def get_reminder_embeds(p_user, s_user, task, time, unit, type_='individual'):
    if type_ == 'mutual':
        m_reminder_set = discord.Embed(
            title='Mutual Reminder',
            description=f"Hey {p_user}, you've set a reminder for {s_user}."
                        f" I'll keep in mind to remind you both.",
            colour=discord.Color.blurple()
        )
        m_reminder_set.add_field(name="Reminder for :", value=task, inline=False)
        m_reminder_set.add_field(name="Reminder Type :", value='Mutual (other user included)', inline=False)
        m_reminder_set.add_field(name="Time :", value=f"{time} {unit} remaining...", inline=False)
        m_reminder_set.set_footer(text='powered by : Agness')

        m_reminder_complete = discord.Embed(
            title="It's your reminder...",
            description=f"Hey {s_user}, {p_user} told me to remind you for your task.",
            colour=discord.Color.red()
        )
        m_reminder_complete.add_field(name="Task :", value=task, inline=False)
        m_reminder_complete.set_footer(text='powered by : Agness')
        return m_reminder_set, m_reminder_complete
    else:
        reminder_set = discord.Embed(
            title='Reminder',
            description=f"Hey {p_user}, I'll keep ur reminder in mind. {' ' * 10}",
            colour=discord.Color.blurple()
        )
        reminder_set.add_field(name="Reminder for :", value=task, inline=False)
        reminder_set.add_field(name="Time :", value=f"{time} {unit} remaining...", inline=False)
        reminder_set.set_footer(text='powered by : Agness')

        reminder_complete = discord.Embed(
            title="It's your reminder...",
            description=f"Hey {p_user}, Remember you told me to remind you for ur task.{' ' * 5}",
            colour=discord.Color.red()
        )
        reminder_complete.add_field(name="Task :", value=task, inline=False)
        reminder_complete.set_footer(text='powered by : Agness')

        return reminder_set, reminder_complete
