import asyncio
from disnake.ext import commands
import disnake
from disnake import FFmpegPCMAudio


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
intents = disnake.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='$')


class MusicPlayer:
    def __init__(self):
        self.playlist = asyncio.Queue()

    
    async def join(self, ctx) -> bool:
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()

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

    
    async def add_song(self, song):
        await self.playlist.put(song)


    async def play_next(self, ctx):
        if self.playlist.qsize:
            self.play(ctx, await self.playlist.get())
        else:
            asyncio.run_coroutine_threadsafe(ctx.send('Queue ended'), bot.loop)

    
    def play(self, ctx, song):
        asyncio.run_coroutine_threadsafe(ctx.send(f'Playing **{song.title}**'), bot.loop)
        audio = song.getbestaudio()
        source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
        ctx.guild.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), bot.loop))


    def get_size(self) -> int:
        return self.playlist.qsize()
    

    def is_empty(self) -> bool:
        return self.playlist.empty()


    def clear(self):
        self.playlist._queue.clear()
