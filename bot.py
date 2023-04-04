import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
import pafy
import validators
import re
import urllib.request
from config import TOKEN

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='$')

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
playlist = asyncio.Queue()


@bot.event
async def on_ready():
    print(f'{bot.user} is now running')


@bot.command()
async def bbl(ctx, *, args):
    try:
        await ctx.send(f'{args} bbl')
    except Exception as e:
        print(e)


@bot.command()
async def join(ctx):
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()

    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
        return True
    else:
        await ctx.send('You are not in a voice channel')
        return False


@bot.command()
async def leave(ctx):
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send('The bot is not in a voice channel')


@bot.command()
async def play(ctx, *, args):
    if not ctx.guild.voice_client:
        if not (await join(ctx)):
            return

    if validators.url(args.split()[0]):
        url = args.split()[0]
    else:
        search = args.replace(' ', '+')

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        url = "https://www.youtube.com/watch?v=" + video_ids[0]

    playlist.put(pafy.new(url))

    if len(playlist) - 1 == 0:
        _play(ctx, playlist.get(0))
    else:
        await ctx.send(f'**{playlist[-1].title}** has been added to the queue')


@bot.command()
async def pause(ctx):
    if ctx.guild.voice_client.is_playing():
        ctx.guild.voice_client.pause()
        await ctx.send('Player paused')
    else:
        await ctx.send('Player is already paused')


@bot.command()
async def resume(ctx):
    if ctx.guild.voice_client.is_paused():
        ctx.guild.voice_client.resume()
        await ctx.send('Player resumed')
    else:
        await ctx.send('Player is already playing')


@bot.command()
async def stop(ctx):
    ctx.guild.voice_client.stop()
    playlist._queue.clear()
    await ctx.send('Player stopped and queue cleared')
    await ctx.guild.voice_client.disconnect()


@bot.command()
async def skip(ctx):
    if ctx.guild.voice_client.is_playing():
        ctx.guild.voice_client.stop()
    play_next(ctx)


def play_next(ctx):
    playlist.pop(0)
    if len(playlist):
        _play(ctx, playlist[0])
    else:
        asyncio.run_coroutine_threadsafe(ctx.send('Queue ended'), bot.loop)


@bot.command()
async def queue(ctx):
    if not playlist.empty:
        queue_string_array = [f'{i+1}: {song.title}' for i, song in enumerate(playlist)]
        queue_string = '\n'.join(queue_string_array)
        await ctx.send(queue_string)
    else:
        await ctx.send('Queue is empty')


def _play(ctx, song):
    asyncio.run_coroutine_threadsafe(ctx.send(f'Playing **{song.title}**'), bot.loop)
    audio = song.getbestaudio()
    source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
    ctx.guild.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))


bot.run(TOKEN)
