import random
import discord
import wavelink
import typing as t
import re
import asyncio
import enum
from discord.ext import commands
from AGNESS_BOT.utils.embeds_utils import MusicEmbeds
from AGNESS_BOT.utils.track_utils import scale_to_10
from AGNESS_BOT import configs, logger
from AGNESS_BOT.utils.custom_exceptions import (
    AlreadyConnectedToChannel,
    NotVoiceChannel,
    QueueIsEmpty,
    NoTracksFound,
    PlayerIsAlreadyPaused,
    PlayerIsAlreadyPlaying,
    NoMoreTracks,
    NoPreviousTracks,
    InvalidRepeatMode,
    NotInQueue
)

KEEP_ALIVE = True

putlog = logger.get_custom_logger(__name__)

REST_URI = configs.REST_URI
MUSIC_HOST = configs.MUSIC_HOST
MUSIC_PORT = configs.MUSIC_PORT
MAX_VOLUME = configs.MAX_VOLUME
DEFAULT_VOLUME = configs.DEFAULT_VOLUME
MUSIC_SERVER_PW = configs.MUSIC_SERVER_PW
MUSIC_SERVER_REGION = configs.MUSIC_SERVER_REGION
MUSIC_SEARCH_ENGINE = configs.MUSIC_SEARCH_ENGINE
BOT_LEAVE_CHANNEL_DELAY = configs.BOT_LEAVE_DELAY

MUSIC_SEARCH_ENGINE = MUSIC_SEARCH_ENGINE.lower()

OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}

debug_index = 1

music_embeds = MusicEmbeds()

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
JUMP_REGEX = r"^([1-9]|10)$"


class RepeatMode(enum.Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self.__queue = list()
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
            putlog.debug(f'Exception raised! <Queue is empty>, pointer position is : {self.position}')
            raise QueueIsEmpty
        putlog.debug(f'Next song played, pointer position is : {self.position}')
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

    @property
    def length(self):
        return len(self.__queue)

    def add(self, *args):
        self.__queue.extend(args)
        putlog.debug('Song added!')

    def empty(self):
        self.__queue.clear()

    def track_index(self, track):
        return self.__queue.index(track)

    def get_next_track(self):
        if not self.__queue:
            return None
            # raise QueueIsEmpty
        self.position += 1
        if self.position < 0:
            return None
        elif self.position > len(self.__queue) - 1:  # Queue Finished...
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0  # If queue is finished and repeat mode is on loop
            else:
                return None
        return self.__queue[self.position]

    def shuffle(self):
        if not self.__queue:
            raise QueueIsEmpty
        random.shuffle(self.__queue)

    def set_repeat_mode(self, mode: str) -> None:
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

    async def add_tracks(self, ctx, tracks) -> None:
        if not tracks:
            putlog.debug('No search results. Raising Exception.     NoTracksFound!')
            await ctx.send('No Tracks found for given query')
            raise NoTracksFound
        if isinstance(tracks, wavelink.TrackPlaylist):  # if tracks are a playlist
            putlog.debug('Search results is a play list. Adding playlist to queue.')
            for track in tracks.tracks:
                self.song_and_requester[track.title] = ctx  # ----> Set requester for each song in playlist.
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            putlog.debug('Only one track found. Adding it in queue.')
            self.queue.add(tracks[0])
            self.song_and_requester[tracks[0].title] = ctx  # ----> Set requester and song name
            await ctx.send(f" Added {tracks[0].title} to the queue")
            await ctx.send(f"Only one song found for given name.")
        else:
            putlog.debug('Multiple songs found. Asking user to choose which one to put in queue.')
            track = await self.choose_track(ctx, tracks)  # Show option to choose from tracks
            if track is not None:
                self.queue.add(track)
                await ctx.send(
                    embed=music_embeds.track_added(
                        track,
                        self.queue.track_index(track) + 1,
                        ctx.author.display_name,
                        ctx.author.avatar_url,
                        ctx.author.color
                    )
                )
            else:
                putlog.debug('User didnt selected from the choice. Skipping further processing on this operation.')

        if not self.is_playing:  # INITIAL Playing...
            putlog.debug('Starting player for the first time from a fresh queue.')
            await self.start_playback(self.queue.first_track)

    async def start_playback(self, track):
        requester = self.song_and_requester.get(track.title, r'Someone ¯\_(ツ)_/¯')  # get requester from dict
        await self.show_now_playing_embed(requester, track)
        await self.play(track)
        putlog.debug('Fresh Player started...')
        return


    async def choose_track(self, ctx, tracks):
        self.sender = ctx

        def _check(r, u):
            return (
                    r.emoji in OPTIONS.keys()
                    and u == ctx.author and r.message.id == msg.id
            )

        msg = await ctx.send(embed=music_embeds.choose_track_embed(ctx, tracks, show_limit=5))

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

    async def advance(self, song_index=0):
        """
        Plays songs, control is passed by on_player_stop()
        :return: None
        """
        global debug_index
        try:
            # ------------------------------------------------------------------ if song play is requested by number.
            if song_index != 0:
                putlog.debug(f'Song is requested by Number. Given no. : {song_index}, Playlist length : {len(self.queue.all_tracks)}')
                if song_index - 1 > len(self.queue.all_tracks):
                    putlog.debug('Requested number of song is not in playlist.  NotInQueue!')
                    await self.sender.send('Requested number of song is not in playlist.')
                    raise NotInQueue
                else:
                    request_index_track = self.queue.all_tracks[song_index - 1]
                    putlog.debug('Song found!')
                    await self.delete_now_playing_embed()

                    requester = self.song_and_requester.get(
                        request_index_track.title,
                        r'Someone ¯\_(ツ)_/¯'
                    )  # --> get requester from dict

                    await self.show_now_playing_embed(requester, request_index_track)
                    await self.play(request_index_track)
                    putlog.debug('Song requested by number(user) played successfully.       SUCCESS!')
            # ------------------------------------------------------------------ if song play is invoked by auto play.
            else:
                putlog.debug('Song requested by autoplay. Getting next track from queue')
                track = self.queue.get_next_track()
                if track is not None:
                    putlog.debug('Next song found. Playing Now!')
                    await self.delete_now_playing_embed()
                    requester = self.song_and_requester.get(
                        track.title,
                        r'Someone ¯\_(ツ)_/¯'
                    )  # --> get requester from dict

                    await self.show_now_playing_embed(requester, track)
                    await self.play(track)
                    putlog.debug('Song requested by autoplay played successfully.       SUCCESS!')
                else:
                    putlog.debug('Track not found coz playlist is over. Stopping Player')
                    self.queue.empty()
                    await self.stop()
                    await self.delete_now_playing_embed()
                    putlog.debug('Player stopped successfully and queue is cleared explicitly.')
        except QueueIsEmpty as err:
            putlog.exception(err)

    async def repeat_track(self):
        putlog.debug('Repeating Current track!')
        await self.play(self.queue.current_track)

    async def delete_now_playing_embed(self):
        if self.nowPlaying:
            try:
                await self.nowPlaying.delete()
                self.nowPlaying = None
                return
            except:
                pass
        return

    async def show_now_playing_embed(self, ctx, track):
        # if isinstance(ctx, str):
        #     author = ctx
        #     now_playing = music_embeds.now_playing(
        #         track.title,
        #         author,
        #         icon=None,
        #         thumb=track.thumb
        #     )
        # else:
            author = ctx.author.display_name,
            avatar = ctx.author.avatar_url,
            color = ctx.author.color,

            now_playing = music_embeds.now_playing(
                track.title,
                ctx.author.display_name,
                ctx.author.avatar_url,
                clr=ctx.author.color,
                thumb=track.thumb
            )
            self.nowPlaying = await ctx.send(embed=now_playing)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())
        self.initial_connect_embed = None
        self.current_volume = DEFAULT_VOLUME
        self.song_index = 0  # used to play songs directly by no. This variable should be managed manually.

    @staticmethod
    def check_query_or_jump(q):
        try:
            int(q)
            if re.match(JUMP_REGEX, q):
                return True
            return False
        except ValueError:
            return False

    @staticmethod
    def set_search_engine(query):
        if MUSIC_SEARCH_ENGINE == 'soundcloud':
            return f"scsearch:{query}"
        elif MUSIC_SEARCH_ENGINE == 'youtube':
            return f"ytsearch:{query}"
        else:
            return f"scsearch:{query}"

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

    async def start_nodes(self):
        """
        Main Node function which declares and initialize the node to connect to lava link server.
        :return: None
        """
        putlog.debug('Starting Music Node...')
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

    async def remove_initial_connect_embed(self):
        if self.initial_connect_embed:
            await self.initial_connect_embed.delete()
            self.initial_connect_embed = None
            return
        return

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
        putlog.debug(f"Wavelink node {node.identifier} connected.      OK!")

    @commands.command(name='connect', aliases=['join', 'jvc'])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        """
        :param ctx: context passed by DC command
        :param channel: An optional argument to pass discord channel.
        :return: None
        """
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)

        embed = music_embeds.initial_connected(
            ctx.author.display_name,
            channel.name,
            ctx.author.avatar_url,
            ctx.author.color
        )
        self.initial_connect_embed = await ctx.send(embed=embed)
        await player.set_volume(DEFAULT_VOLUME)

    @commands.command(name='disconnect', aliases=['leave', 'lv'])
    async def disconnect_command(self, ctx):
        """
        This function is used to disconnect the bot from voice channel.
        :param ctx: Context
        :return: None
        """
        putlog.warning('Disconnecting Node.')
        player = self.get_player(ctx)
        await ctx.send('Leaving...')
        await player.teardown()
        await ctx.send('Disconnected!')
        await player.delete_now_playing_embed()
        await self.remove_initial_connect_embed()
        putlog.warning('Node Disconnected by disconnect_command!')

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
                putlog.warning(f'No human is in voice channel. Bot will leave the channel after : {BOT_LEAVE_CHANNEL_DELAY}s')
                await asyncio.sleep(BOT_LEAVE_CHANNEL_DELAY)  # After 10 seconds, bot will be removed
                await self.remove_initial_connect_embed()
                await self.get_player(member.guild).teardown()
                await self.get_player(member.guild).delete_now_playing_embed()
                putlog.warning(f'Bot left channel after {BOT_LEAVE_CHANNEL_DELAY}s coz no human was in there.')

    @wavelink.WavelinkMixin.listener('on_track_stuck')
    @wavelink.WavelinkMixin.listener('on_track_end')
    @wavelink.WavelinkMixin.listener('on_track_exception')
    async def on_player_stop(self, node, payload):
        """
        The control is passed to this function on any of the condition from above decorators.
        :param node:
        :param payload:
        :return:
        """
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            putlog.debug('Repeat single song mode activated. Playing current song on loop.')
            await payload.player.repeat_track()
        elif self.song_index != 0:
            putlog.debug('Control received by play command after validating the command that its a song jump by number.')
            putlog.debug('Passing control to advance() method and setting self.song_index=0 again.')
            await payload.player.advance(self.song_index)
            self.song_index = 0
        else:
            putlog.debug('Command is not a song jump. Passing control to advance()')
            await payload.player.advance()

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
            putlog.debug('Resume player command given')
            if player.queue.is_empty:
                putlog.debug('Resume player command given but queue is empty. Raising Exception!')
                raise QueueIsEmpty
            if not player.is_paused:
                putlog.debug('Resume command given but player is already playing. Sending message to user.')
                await ctx.send('🔊  Player is already playing...')
            else:  # Resume Music
                putlog.debug('Resume command given and executing successfully.')
                await player.set_pause(False)
                await ctx.send('▶    Playback resumed')

        # ----------------------------------------------------------------------
        else:  # Query Search
            if self.check_query_or_jump(query):  # Jump tracks by number (index)
                putlog.debug('validating command if it is a song jump or another query.')
                self.song_index = int(query)
                await player.stop()  # Gives control to >> on_player_stop()
                putlog.debug('Playback stopped and control passed to on_player_stop() method.')
            else:
                putlog.debug('Query was not a song jump. now checking if query is a link')
                query = query.strip("<>")  # search by link
                if not re.match(URL_REGEX, query):
                    putlog.debug('Query is song name. NOT A LINK')
                    query = self.set_search_engine(query)  # search by song name
                else:
                    putlog.debug('Query is a link')
                putlog.debug('Adding Search results in queue')
                songs_found = await self.wavelink.get_tracks(query)
                await player.add_tracks(ctx, songs_found)

        # ----------------------------------------------------------------------

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

    @commands.command(name='stop', aliases=['s'])
    async def stop_command(self, ctx):
        """
        This function stops the current music stream and clears the queue
        :param ctx: context
        :return: None
        """
        putlog.debug('Song stop requested. Stopping player and destroying playlist.')
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.send('Playback Stopped')
        await player.delete_now_playing_embed()
        putlog.debug('Player stopped and playlist destroyed.')

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

    @commands.command(name='previous', aliases=['-1', 'prv'])
    async def previous_command(self, ctx):
        """
        This function provides the functionality to play the previous song in the playlist.
        :param ctx: context
        :return: None
        """
        player = self.get_player(ctx)
        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        await ctx.send('Playing previous track in queue.  ⏮')

    @commands.command(name='seek', aliases=['sk'])
    async def seek_command(self, ctx, stride: t.Optional[int] = 1):
        player = self.get_player(ctx)
        ct = player.queue.current_track

        length = ct.duration
        seek_length = scale_to_10(int(length), int(stride))
        if seek_length is not False:
            await player.seek(seek_length)
            await ctx.send(
                f"Song is seeked by {seek_length // 1000} seconds, Current position is : "
                f"{str(seek_length // 60000).zfill(2)}:{str(seek_length % 60).zfill(2)}")
        else:
            await ctx.send('stride is wrong')

    @commands.command(name='repeat', aliases=['rpt', 'rp'])
    async def repeat_command(self, ctx, mode: str):
        mode = mode.lower()
        if mode not in ("none", '1', 'all', 'current'):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        putlog.debug(f'Repeat mode set to {mode}')

        if mode == 'none':
            response = f"Repeat Mode has been set to {mode.title()}. No song will be repeated."
        elif mode in ('1', 'current'):
            response = f'Repeat mode has been set to {mode}. Current song is on loop  🔂'
        elif mode == 'all':
            response = f'Repeat mode has been set to {mode}. ' \
                       f'Current playlist will be played over and over and over and... .  .   . over again!  🔁'
        else:
            response = f"Repeat Mode has been set to {mode}."

        await ctx.send(response)

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

    @commands.command(name='queue', aliases=['playlist', 'plylst', 'plst', 'pl'])
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        player = self.get_player(ctx)
        if show > 20:
            await ctx.send('Only 20 songs can be shown in embed!')
            return

        if player.queue.is_empty:
            raise QueueIsEmpty

        all_songs = "\n\n".join(
            [f"{i + 1} -> {song.title}" for i, song in enumerate(player.queue.all_tracks)][:show]
        )
        currently_playing = f'🔊 {getattr(player.queue.current_track, "title", "No tracks currently playing.")}'
        upcoming_song = player.queue.upcoming

        # Show Playlist
        await ctx.send(
            embed=music_embeds.show_playlist(
                all_songs,
                currently_playing,
                upcoming_song,
                showlimit=show,
                requester=ctx.author.display_name,
                requester_icon=ctx.author.avatar_url,
                color=ctx.author.color
            )
        )

    # Exception handling for Play command =============================================================================
    # Exception handling for next_command =============================================================================
    # Exception handling for previous_command =========================================================================
    # Exception handling for pause_command ============================================================================
    # Exception handling for shuffle_command ==========================================================================
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

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("No songs to play as the queue is empty.")
        elif isinstance(exc, NotVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send("There are no previous tracks in the queue.")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send('⏸   Player is already paused!')

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("There are no more tracks in the queue.")

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue could not be shuffled as it is currently empty.")

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is currently empty.")


def setup(bot):
    bot.add_cog(Music(bot))
