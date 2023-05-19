import asyncio
from disnake.ext import commands
import disnake
from disnake import FFmpegPCMAudio


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
intents = disnake.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='$')


class MusicPlayer:
    def __init__(self):
        self.playlist = []

    async def join(self, ctx) -> bool:
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
        else:
            self.clear()
            await ctx.send('Queue cleared')

        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
            return True
        else:
            await ctx.send('You are not in a voice channel')
            return False

    async def leave(self, ctx):
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send('The bot is not in a voice channel')

    def add_song(self, song):
        self.playlist.append(song)

    async def play_next(self, ctx):
        self.playlist.pop(0)
        if len(self.playlist) > 0:
            self.play(ctx, self.playlist[0])
        else:
            await ctx.send('Queue ended')

    def play(self, ctx, song):
        audio = song.getbestaudio()
        source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
        ctx.guild.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), bot.loop))

    def get_first(self):
        return self.playlist[0]

    def get_size(self) -> int:
        return len(self.playlist)

    def is_empty(self) -> bool:
        return len(self.playlist) == 0

    def clear(self):
        self.playlist.clear()
