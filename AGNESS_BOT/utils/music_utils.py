import enum
import wavelink
import asyncio
import random
from .decorators import (
    check_empty_queue,
    check_connected_to_channel,
    NoTracksFound,
    export
)
from AGNESS_BOT import (
    NotVoiceChannel,
    QueueIsEmpty,
    NotInQueue,
    MusicEmbeds,
    logger
)

putlog = logger.get_custom_logger(__name__)
music_embeds = MusicEmbeds()
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


@export
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
    @check_empty_queue
    def all_tracks(self):
        return self.__queue

    @property
    @check_empty_queue
    def first_track(self):
        return self.__queue[0]

    @property
    @check_empty_queue
    def last_track(self):
        return self.__queue[-1]

    @property
    @check_empty_queue
    def current_track(self):
        return self.__queue[self.position]

    @property
    @check_empty_queue
    def upcoming(self):
        return self.__queue[self.position + 1:]

    @property
    @check_empty_queue
    def history(self):
        return self.__queue[:self.position]

    @property
    @check_empty_queue
    def length(self):
        return len(self.__queue)

    @check_empty_queue
    def shuffle(self):
        random.shuffle(self.__queue)

    def add(self, *args):
        self.__queue.extend(args)
        putlog.info(f'Song added!   len of queue is : {len(self.__queue)} Pointer is : {self.position}')

    def empty(self):
        self.__queue.clear()
        self.position = 0

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

    def get_track_by_index(self, ind):
        if not self.__queue:
            return None
        if ind > len(self.__queue):
            return None
        self.position += ind - 1
        return self.__queue[ind - 1]

    def set_repeat_mode(self, mode: str) -> None:
        if mode == 'none':
            self.repeat_mode = RepeatMode.NONE
        elif mode == '1':
            self.repeat_mode = RepeatMode.ONE
        elif mode == 'all':
            self.repeat_mode = RepeatMode.ALL


# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================

@export
class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.sender = None
        self.nowPlaying = None
        # Keys are song title and values are ctx.
        # use as self.song_and_requester[track.title] = ctx
        self.song_and_requester = dict()  # A dict containing songs and their requester.

    @check_connected_to_channel
    async def connect(self, ctx, channel=None):
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
            await ctx.send('Oops! . . . I didnt found any song for given query! 😕')
            raise NoTracksFound
        if isinstance(tracks, wavelink.TrackPlaylist):  # if tracks are a playlist
            putlog.debug('Search results is a play list. Adding playlist to queue.')
            for track in tracks.tracks:
                self.song_and_requester[track.title] = ctx  # ----> Set requester for each song in playlist.
            self.queue.add(*tracks.tracks)
            await ctx.send('Your playlist added in queue successfully! Keep the party going...🎉 🥳')
        elif len(tracks) == 1:
            putlog.debug('Only one track found. Adding it in queue.')
            self.queue.add(tracks[0])
            self.song_and_requester[tracks[0].title] = ctx  # ----> Set requester and song name
            await ctx.send(
                f"Only one song found for given name but anyway, I added it in queue. Keep ROckinG the party  🎊 🥳 🎉")
            await ctx.send(f"✅ Added {tracks[0].title} to the queue")
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
        try:
            # ------------------------------------------------------------------ if song play is requested by number.
            if song_index != 0:
                putlog.debug(
                    f'Song is requested by Number. Given no. : {song_index}, Playlist length : '
                    f'{len(self.queue.all_tracks)}')
                if song_index - 1 > len(self.queue.all_tracks):
                    putlog.debug('Requested number of song is not in playlist.  NotInQueue!')
                    await self.sender.send('Requested number of song is not in playlist.')
                    raise NotInQueue
                else:
                    request_index_track = self.queue.get_track_by_index(song_index)
                    putlog.debug('Song found!')
                    await self.delete_now_playing_embed()

                    requester = self.song_and_requester.get(
                        request_index_track.title,
                        r'Someone ¯\_(ツ)_/¯'
                    )  # --> get requester from dict

                    await self.show_now_playing_embed(requester, request_index_track)
                    await self.play(request_index_track)
                    putlog.debug('Song requested by number(user) played successfully.       SUCCESS!')
                    putlog.info(f"Pointer is {self.position} and length of queue is {len(self.queue.all_tracks)}")
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
                    putlog.info('Song requested by autoplay played successfully.       SUCCESS!')
                else:
                    putlog.warning('Track not found coz playlist is over. Stopping Player')
                    self.queue.empty()
                    await self.stop()
                    await self.delete_now_playing_embed()
                    putlog.warning('Player stopped successfully and queue is cleared explicitly.')
        except QueueIsEmpty as err:
            putlog.exception(err)

    async def repeat_track(self):
        putlog.info('Repeating Current track!')
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
        now_playing = music_embeds.now_playing(
            track.title,
            ctx.author.display_name,
            ctx.author.avatar_url,
            clr=ctx.author.color,
            thumb=track.thumb
        )
        self.nowPlaying = await ctx.send(embed=now_playing)


if __name__ == '__main__':
    obj = Queue()
    obj.add((1, 2, 3, 4))
    # print(dir(obj))
    print(obj.first_track)
