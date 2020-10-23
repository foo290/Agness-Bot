import random
import discord
import wavelink
import typing as t
import re
import asyncio
import enum
from discord.ext import commands
from ...utils.embeds_utils import MusicEmbeds
from ...settings import (
    MUSIC_HOST,
    MUSIC_PORT,
    MUSIC_SERVER_PW,
    MUSIC_SERVER_REGION,
    REST_URI,
    MUSIC_SEARCH_ENGINE,
    BOT_LEAVE_CHANNEL_DELAY,
    DEFAULT_VOLUME,
    MAX_VOLUME,
    KEEP_ALIVE_DELAY
)

MUSIC_SEARCH_ENGINE = MUSIC_SEARCH_ENGINE.lower()

KEEP_ALIVE = True


OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}

music_embads = MusicEmbeds()

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
JUMP_REGEX = r"^([1-9]|10)$"


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NotVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class PlayerIsAlreadyPlaying(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class NotInQueue(commands.CommandError):
    pass


class RepeatMode(enum.Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self.__queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self.__queue

    @property
    def all_tracks(self):
        if not self.__queue:
            raise QueueIsEmpty
        return self.__queue

    @property
    def first_track(self):
        if not self.__queue:
            raise QueueIsEmpty
        return self.__queue[0]

    @property
    def last_track(self):
        if not self.__queue:
            raise QueueIsEmpty
        return self.__queue[-1]

    @property
    def current_track(self):
        if not self.__queue:
            raise QueueIsEmpty
        return self.__queue[self.position]

    @property
    def upcoming(self):
        if not self.__queue:
            raise QueueIsEmpty
        return self.__queue[self.position + 1:]

    @property
    def history(self):
        if not self.__queue:
            raise QueueIsEmpty
        return self.__queue[:self.position]

    def empty(self):
        self.__queue.clear()

    @property
    def length(self):
        return len(self.__queue)

    def add(self, *args):
        self.__queue.extend(args)

    def get_next_track(self):
        if not self.__queue:
            raise QueueIsEmpty
        self.position += 1
        if self.position < 0:
            return None
        elif self.position > len(self.__queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:

                return None
                # print('something is terribly wrong')
        return self.__queue[self.position]

    def shuffle(self):
        if not self.__queue:
            raise QueueIsEmpty
        # upcoming = self.upcoming
        random.shuffle(self.__queue)
        # self.__queue = upcoming

    def set_repeat_mode(self, mode):
        if mode == 'none':
            self.repeat_mode = RepeatMode.NONE
        elif mode == '1':
            self.repeat_mode = RepeatMode.ONE
        elif mode == 'all':
            self.repeat_mode = RepeatMode.ALL


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.sender = None
        self.nowPlaying = None
        # Keys are song title and values are ctx.
        # use as self.song_and_requester[track.title] = ctx
        self.song_and_requester = dict()  # A dict containing songs and their requester.

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel
        channel = getattr(ctx.author.voice, "channel", channel)
        if channel is None:
            raise NotVoiceChannel
        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            await ctx.send('No Tracks found for given query')
            raise NoTracksFound
        if isinstance(tracks, wavelink.TrackPlaylist):  # if tracks are a playlist
            # self.queue.add(*tracks.tracks)
            pass
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            self.song_and_requester[tracks[0].title] = ctx  # ----> Set requester and song name
            await ctx.send(f" Added {tracks[0].title} to the queue")
            await ctx.send(f"Only one song found for given name.")
        else:
            track = await self.choose_track(ctx, tracks)  # Show option to choose from tracks
            if track is not None:
                self.queue.add(track)
                await ctx.send(f"Added {track.title} to the queue")
        if not self.is_playing:  # INITIAL Playing...
            await self.start_playback(self.queue.first_track)

    async def choose_track(self, ctx, tracks):
        self.sender = ctx

        def _check(r, u):
            return (
                    r.emoji in OPTIONS.keys()
                    and u == ctx.author and r.message.id == msg.id
            )

        msg = await ctx.send(embed=music_embads.choose_track_embed(ctx, tracks, show_limit=5))

        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=60, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            self.song_and_requester[tracks[OPTIONS[reaction.emoji]].title] = ctx  # ----> Set requester and song name
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self, track):
        requester = self.song_and_requester[track.title]  # get requester from dict
        await self.show_now_playing_embed(requester, track)
        await self.play(track)

    async def advance(self, song_index=0):
        """
        Plays songs, control is passed by on_player_stop()
        :return: None
        """
        try:
            if song_index != 0:  # if song play is requested by number.
                if song_index - 1 > len(self.queue.all_tracks):
                    await self.sender.send('Requested number of song is not in playlist.')
                    raise NotInQueue
                else:
                    request_index_track = self.queue.all_tracks[song_index - 1]  # --> get requester from dict
                    await self.delete_now_playing_embed()
                    requester = self.song_and_requester[request_index_track.title]  # --> get requester from dict
                    await self.show_now_playing_embed(requester, request_index_track)
                    await self.play(request_index_track)
            else:
                track = self.queue.get_next_track()
                if track is not None:
                    await self.delete_now_playing_embed()
                    requester = self.song_and_requester[track.title]
                    await self.show_now_playing_embed(requester, track)
                    await self.play(track)
                else:
                    await self.delete_now_playing_embed()
                    await self.stop()
                    self.queue.empty()
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)

    async def delete_now_playing_embed(self):
        if self.nowPlaying:
            await self.nowPlaying.delete()
            self.nowPlaying = None
            return
        return

    async def show_now_playing_embed(self, ctx, track):
        now_playing = music_embads.now_playing(
            track.title,
            ctx.author.display_name,
            ctx.author.avatar_url,
            ctx.author.color
        )
        self.nowPlaying = await ctx.send(embed=now_playing)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())
        # self.wavelink.loop.create_task(self.start_nodes())

        self.initial_connect_embed = None
        self.current_volume = DEFAULT_VOLUME
        self.song_index = 0  # used to play songs directly by no. This variable should be managed manually.

    @commands.command(name='connect_node')
    async def node_connect(self, ctx):
        await ctx.send('Connecting Node...')
        await self.start_nodes()
        await ctx.send('Node Connected!')

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        """
        This function triggers when the node is connected successfully to lava link server.
        :param node: The node defined in class
        :return: None
        """
        print(f"Wavelink node {node.identifier} connected.      OK!")

    @commands.command(name='connect', aliases=['join', 'jvc'])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        """
        :param ctx: context passed by DC command
        :param channel: An optional argument to pass discord channel.
        :return: None
        """
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)

        embed = music_embads.initial_connected(
            ctx.author.display_name,
            channel.name,
            ctx.author.avatar_url,
            ctx.author.color
        )
        self.initial_connect_embed = await ctx.send(embed=embed)
        await player.set_volume(DEFAULT_VOLUME)
        # await self.keep_server_alive()  # This function keeps pinging server to avoid ideal server timeout on heroku.

    # Error handling for connect command =============================================================================
    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        """
        :param ctx: context passed by DC command
        :param exc: Exception raised (in this case custom exception is raised) in Player class's connect method
        :return: None
        """
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send('Already connected to a voice channel')
        elif isinstance(exc, NotVoiceChannel):
            await ctx.send('No suitable voice channel provided')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        This is an event function which listens the events happening in the voice channel like member joined or leaves
        :param member: Members in the channel
        :param before: before state of joining of any member
        :param after: after state of joining of any member
        :return: None
        """
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await asyncio.sleep(BOT_LEAVE_CHANNEL_DELAY)  # After 10 seconds, bot will be removed
                await self.get_player(member.guild).delete_now_playing_embed()
                await self.remove_initial_connect_embed()
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener('on_track_stuck')
    @wavelink.WavelinkMixin.listener('on_track_end')
    @wavelink.WavelinkMixin.listener('on_track_exception')
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance(self.song_index)
            self.song_index = 0

    async def cog_check(self, ctx):
        """
        This function ensures that music commands are not being used in DMs.
        :param ctx: Context passed by DC command
        :return: None
        """
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send('Music commands are not allowed in DMs')
            return False
        return True

    # async def keep_server_alive(self):
    #     while KEEP_ALIVE:
    #         print('KEEPING ALIVE !')
    #         query = f'scsearch:Dynamite BTS{random.randint(10, 1000)}'
    #         await asyncio.sleep(KEEP_ALIVE_DELAY)
    #         await self.wavelink.get_tracks(query)
    #     else:
    #         return

    # @commands.command(name='keep_alive')
    # async def set_keep_alive_off(self, ctx, state):
    #     global KEEP_ALIVE
    #     KEEP_ALIVE = False if state.lower() == 'off' else True
    #     await ctx.send('Keep Alive is set to ')

    @commands.command(name="volume", aliases=['vol', 'v'])
    async def set_player_volume(self, ctx, v: t.Optional[str]):
        try:
            if v:
                v = int(v)
                if v <= MAX_VOLUME:
                    player = self.get_player(ctx)
                    await player.set_volume(v)
                    if v > self.current_volume:
                        await ctx.send(f'Volume Raised by : {v - self.current_volume}  ⤴.  Player volume is : {v}.  ')
                    elif v < self.current_volume:
                        await ctx.send(
                            f'Volume Decreased by : {self.current_volume - v}  ⤵.  Player volume set to {v}.  ')
                    else:
                        await ctx.send(f'Player volume not changed. Current volume : {self.current_volume}.')
                    self.current_volume = v
                else:
                    await ctx.send(f'Set volume in range 0-100')
            else:
                await ctx.send(f'Current volume level is : {self.current_volume}.')
        except ValueError:
            ctx.send(f"Volume must be Integer")

    async def remove_initial_connect_embed(self):
        if self.initial_connect_embed:
            await self.initial_connect_embed.delete()
            self.initial_connect_embed = None
            return
        return

    def set_search_engine(self, query):
        if MUSIC_SEARCH_ENGINE == 'soundcloud':
            return f"scsearch:{query}"
        elif MUSIC_SEARCH_ENGINE == 'youtube':
            return f"ytsearch:{query}"
        else:
            return f"scsearch:{query}"

    async def start_nodes(self):
        """
        Main Node function which declares and initialize the node to connect to lava link server.
        :return: None
        """
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": MUSIC_HOST,
                "port": MUSIC_PORT,
                "rest_uri": REST_URI,
                "password": MUSIC_SERVER_PW,
                "identifier": 'MAIN ',
                "region": MUSIC_SERVER_REGION
            }
        }
        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        """
        A get player utility implemented to quickly grab the player either by ctx or guild.
        :param obj: Either ctx or guild
        :return: player
        """
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name='disconnect', aliases=['leave', 'lv'])
    async def disconnect_command(self, ctx):
        """
        This function is used to disconnect the bot from voice channel.
        :param ctx: Context
        :return: None
        """
        player = self.get_player(ctx)
        await ctx.send('Leaving...')
        await player.delete_now_playing_embed()
        await player.teardown()
        await ctx.send('Disconnected!')
        await self.remove_initial_connect_embed()

    def check_query_or_jump(self, q):
        try:
            int(q)
            if re.match(JUMP_REGEX, q):
                return True
            return False
        except ValueError:
            return False

    @commands.command(name='play', aliases=['p', 'ply'])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        """
        A play command to search and give option for songs to play.
        :param ctx: context passed by DC
        :param query: The song name
        :return: None
        """
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)
        # ----------------------------------------------------------------------
        if query is None:  # Resume Track Checks
            if player.queue.is_empty:
                raise QueueIsEmpty
            if not player.is_paused:
                await ctx.send('🔊  Player is already playing...')
            else:  # Resume Music
                await player.set_pause(False)
                await ctx.send('▶    Playback resumed')
        # ----------------------------------------------------------------------
        else:  # Query Search
            if self.check_query_or_jump(query):  # Jump tracks by number (index)
                self.song_index = int(query)
                self
                await player.stop()  # Gives control to >> on_player_stop()
            else:
                query = query.strip("<>")  # search by link
                if not re.match(URL_REGEX, query):
                    query = self.set_search_engine(query)  # search by song name
                await player.add_tracks(ctx, await self.wavelink.get_tracks(query))
        # ----------------------------------------------------------------------

    # Error handling for Play command =============================================================================
    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("No songs to play as the queue is empty.")
        elif isinstance(exc, NotVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")

    @commands.command(name='stop', aliases=['s'])
    async def stop_command(self, ctx):
        """
        This function stops the current music stream and clears the queue
        :param ctx: context
        :return: None
        """
        player = self.get_player(ctx)
        await player.delete_now_playing_embed()
        player.queue.empty()
        await player.stop()
        await ctx.send('Playback Stopped')

    @commands.command(name='next', aliases=['skip', 'nxt', '+1'])
    async def next_command(self, ctx):
        """
        This function provides the functionality to skip a song form the current playlist and play the next one.
        :param ctx: context
        :return: None | Raises NoMoreTracks if no next song found
        """
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        await ctx.send(f'Playing next track   ⏭')

    # Error handling for next_command =============================================================================
    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("There are no more tracks in the queue.")

    @commands.command(name='previous', aliases=['-1', 'prv'])
    async def previous_command(self, ctx):
        """
        This function provides the functionality to paly the previous song in the playlist.
        :param ctx: context
        :return: None
        """
        player = self.get_player(ctx)
        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        await ctx.send('Playing previous track in queue.  ⏮')

    # Error handling for previous_command =============================================================================
    @previous_command.error
    async def previous_command_error(self, ctx, exc):

        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send("There are no previous tracks in the queue.")

    @commands.command(name='pause', aliases=['pa'])
    async def pause_command(self, ctx):
        """
        This function provides the functionality to pause the current song.
        :param ctx: Context
        :return: None
        """
        player = self.get_player(ctx)
        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.send('⏸    Playback Paused!')

    # Error handling for pause_command =============================================================================
    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send('⏸   Player is already paused!')

    @commands.command(name='shuffle', aliases=['shfl', 'sfl'])
    async def shuffle_command(self, ctx):
        """
        Shuffles the playlist.
        :param ctx: context
        :return: None
        """
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.send('Queue shuffled')

    # Error handling for shuffle_command =============================================================================
    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue could not be shuffled as it is currently empty.")

    @commands.command(name='repeat', aliases=['rpt', 'rp'])
    async def repeat_command(self, ctx, mode: str):
        mode = mode.lower()
        if mode not in ("none", '1', 'all', 'current'):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)

        if mode == 'none':
            response = f"Repeat Mode has been set to {mode.title()}. No song will be repeated."
        elif mode in ('1', 'current'):
            response = f'Repeat mode has been set to {mode}. Current song is on loooooooooooop  🔂'
        elif mode == 'all':
            response = f'Repeat mode has been set to {mode}. ' \
                       f'Current playlist will be played over and over and over and... .  .   . over again!  🔁'
        else:
            response = f"Repeat Mode has been set to {mode}."

        await ctx.send(response)

    @commands.command(name='queue', aliases=['playlist', 'plylst', 'plst', 'pl'])
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        all_songs = "\n\n".join(
            [f"{i + 1} -> {song.title}" for i, song in enumerate(player.queue.all_tracks)]
        )
        currently_playing = f'🔊 {getattr(player.queue.current_track, "title", "No tracks currently playing.")}'
        upcoming_song = player.queue.upcoming

        # Show Playlist
        await ctx.send(
            embed=music_embads.show_playlist(
                all_songs,
                currently_playing,
                upcoming_song,
                showlimit=show,
                requester=ctx.author.display_name,
                requester_icon=ctx.author.avatar_url,
                color=ctx.author.color
            )
        )

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is currently empty.")


def setup(bot):
    bot.add_cog(Music(bot))


