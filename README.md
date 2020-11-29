
<h1 align='center'>Agness-Bot</h1>

A discord bot for moderation and fun activity and music streaming and many more and... O_o <br>

The bot is self hosted that means you have the code which is ready to go on server, **Your server.** 


## Music powered by :

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='https://github.com/foo290/resonate-beats'><img src='https://github.com/foo290/resonate-beats/blob/main/readme_imgs/resonate-beats-logo.png' width=50px, alt='an image was supposed to be here'></a> <br />
<a href='https://github.com/foo290/resonate-beats'>resonate-beats</a>


## Setup :

There are some minor setting that you'd ahve to do before get going. There is a <a href='https://github.com/foo290/Agness-Bot/blob/master/AGNESS_BOT/settings.py'>settings.py</a> file in there which contains all the configurations that you need to customize the bot for your need.

<p id='Guild-settings'>
<h2 align='center'>
    Guild Settings
</h2>

There are some configurations which are server dependent, in this section, those configs are explained ...

#### 1. Roles :

A dict defining aliases for the roles you may create and for the roles the bot will use for command checks are defined in <a href='https://github.com/foo290/Agness-Bot/blob/a4066dd35ec1fbf6b018e32ebe3eadc7b5b86722/AGNESS_BOT/settings.py#L86'>ROLE_ALIASES</a> in <a href='https://github.com/foo290/Agness-Bot/blob/master/AGNESS_BOT/Settings.py'>settings.py</a>.

You have to give exact name of your roles for this to work.

```
ROLE_ALIASES = {
    'OWNER_ROLE': 'Owner',
    'ADMIN_ROLE': 'Admin',
    'STAFF_ROLE': 'Staff',
    'DEFAULT_ROLE': 'Member',
    'UNVERIFIED': 'Unverified',
    ...
}
```


* ```OWNER_ROLE :``` The name or the role for owner could be diffrent for diffrent servers, so for commands which are ```Owner``` Specific uses this role.
* ```DEFAULT_ROLE :``` The default role for user, like normal role which has minimal access to the commands.
* ```MUTED :``` This role has no access to read or send the message and assigned to users if they are being muted by the bot for a specific interval of time.
* ```UNVERIFIED :``` If the Joinig verification is enabled, this role is assigned to users when they first join the server and this role has very limited access to the server for example: unverified users can only see welcome and Rules channel. If the joining verification is not enabled, members will be assigned default role.


</p>
<p id='settings'>

<h2 align='center'>
  <a href='https://github.com/foo290/Agness-Bot/blob/master/AGNESS_BOT/Settings.py'>
    settings.py ⚙
  </a>
</h2>

### COGS :

Add **name** of your cog / extension files here...

```
COGS = [
    'admin_cmds',
    'dm_cmds',
    'members_cmds',
    ...
   ]
```


### COGS directory path :

The dir path which contains COGS for loading. This is defined according to need of this project in <a href='https://github.com/foo290/Agness-Bot/blob/a4066dd35ec1fbf6b018e32ebe3eadc7b5b86722/AGNESS_BOT/settings.py#L26'>COGS_DIR</a> variable. **This is advised not to change untill you know what you dealing with.**

```
COGS_DIR = 'AGNESS_BOT.bot.cogs.'  # This is the directory that contains all the cogs
```

### Owner's Configs :
This is a dict containing names as key and their id as vaules..

```
OWNER_IDS = {
    'Nitin': your-id-here: int,
    ...
}
```

### Bot Configs :
The bot is operated based on the preferances defined in <a href='https://github.com/foo290/Agness-Bot/blob/a4066dd35ec1fbf6b018e32ebe3eadc7b5b86722/AGNESS_BOT/settings.py#L47'>BOT_CONFIGS</a> dict in settings.py which is explained below...

```
BOT_CONFIGS = {
    'BOT_NAME': "Agness",
    'COMMAND_PREFIX': ".",
    'BOT_TOKEN': os.environ.get('AGNESS_BOT_TOKEN'),
    'OWNER_IDS': list(OWNER_IDS.values()),
    'COGS_DIR': COGS_DIR,
    'COGS': COGS,
    'ACTIVITY_TYPE': act.watching,
    'ACTIVITY_NAME': 'the world collapse!',
    'SHOW_TYPING': False,
    'TYPING_INTERVAL': 0.5
}
```

* ```BOT_NAME``` : The name of bot which will be used in some embeds.
* ```BOT_TOKEN``` : This is obvious, define an environment variable ```AGNESS_BOT_TOKEN``` in your system for containing your bot's token.
* ```COMMAND_PREFIX``` : The command prefix for your bot's commands.
* ```OWNER_IDS``` : This will be automatically filled by ```OWNER_IDS```
* ```COGS_DIR``` : **Do not change this until you have reason**
* ```COGS``` : This will be automatically filled by ```COGS```
* ```SHOW_TYPING``` : This shows the bot's typing status. If set to ```True```, Bot will be shown as ```typing...``` before sending the message.
* ```TYPING_INTERVAL``` : The time for which the status ```typing...``` is shown.

### Guild's Config :

Global guild configs in <a href='https://github.com/foo290/Agness-Bot/blob/a4066dd35ec1fbf6b018e32ebe3eadc7b5b86722/AGNESS_BOT/settings.py#L60'>GUILDS_CONFIG</a>

```
GUILDS_CONFIG = {
    'FIRST_REDIRECT_CHANNEL': 773203865151602729,  # Welcome / Rules Channel!
    'RULES_CHANNEL': None,
    'GOODBYE_CHANNEL': None,

    'MEMBER_JOIN_SELF_VERIFICATION': True,

    'INVITE_LINK_TTL': 86400,
    'INVITE_LINK_MAX_USES': 50,
}
```

* ```FIRST_REDIRECT_CHANNEL``` : This is the first channel your user will be redirected when user clicks on invite link. This could be the id of dedicated welcome channel or rules channel.
* ```RULES_CHANNEL``` : The id of Rules channel.
* ```GOODBYE_CHANNEL``` : If set, a goodbye message will be sent to this channel on member kick/leave.
* ```INVITE_LINK_TTL``` : The time for which invite link generated by invite command will be valid. default set to 24 hours, set None for never expiire.
* ```INVITE_LINK_MAX_USES``` : Big name but pretty self explanatory...

### Functionalities handled :

If you have more than one bot in your server and other bot is managing these functionalities then set these to ```False``` in <a href='https://github.com/foo290/Agness-Bot/blob/a4066dd35ec1fbf6b018e32ebe3eadc7b5b86722/AGNESS_BOT/settings.py#L72'>FUNCTIONALITIES</a>

```
FUNCTIONALITIES = {
    'MANAGE_NEW_JOINING': True,
    'MANAGE_MEMBER_LEFT': True,
    'SEND_DM_ON_JOIN': True
}
```

* ```MANAGE_NEW_JOINING``` : if set True, Handles the role assigning on joining, member verification, role assignment. 
* ```MANAGE_MEMBER_LEFT``` : if set True, Handles sending msg in goodbye channel.
* ```SEND_DM_ON_JOIN``` : If set True, will send an instructed dm to joined user guiding how to use and gain access to server is verification is enabled.

</p>


Documentation has to be done yet... :/
