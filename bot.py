import disnake
from disnake.ext import commands
from disnake import FFmpegPCMAudio
import asyncio
import pafy
import validators
import re
import urllib.request
from MusicPlayer import MusicPlayer, bot
from config import TOKEN


mp = MusicPlayer()


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
    await mp.join(ctx)


@bot.command()
async def leave(ctx):
    await mp.leave(ctx)
    


@bot.command()
async def play(ctx, *, args):
    if not ctx.guild.voice_client:
        if not (await mp.join(ctx)):
            return

    if validators.url(args.split()[0]):
        url = args.split()[0]
    else:
        search = args.replace(' ', '+')

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        url = "https://www.youtube.com/watch?v=" + video_ids[0]

    song = pafy.new(url)
    await mp.add_song(song)

    if (mp.get_size() - 1) == 0 and not ctx.guild.voice_client.is_playing():
        mp.play(ctx, await mp.playlist.get())
    else:
        await ctx.send(f'**{song.title}** has been added to the queue')


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
    mp.playlist._queue.clear()
    await ctx.send('Player stopped and queue cleared')
    await ctx.guild.voice_client.disconnect()


@bot.command()
async def skip(ctx):
    if ctx.guild.voice_client.is_playing():
        ctx.guild.voice_client.stop()
    await mp.play_next(ctx)


@bot.command()
async def queue(ctx):
    if not mp.is_empty():
        queue_string_array = [f'{i+1}: {song.title}' for i, song in enumerate(list(mp.playlist._queue))]
        queue_string = '\n'.join(queue_string_array)
        await ctx.send(queue_string)
    else:
        await ctx.send('Queue is empty')


bot.run(TOKEN)
