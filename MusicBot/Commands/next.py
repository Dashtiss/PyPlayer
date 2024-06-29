from discord.ext import commands
from discord import FFmpegPCMAudio
from .. import Playing
from ..Playing import queue



@commands.command()
async def next(ctx):
    """
    Plays the next song in the queue.
    """
    if len(queue) > 0:
        Music = queue.pop(0)
        Playing.Playing = True
        player = ctx.voice_client
        player.stop()
        player.play(FFmpegPCMAudio(Music.Path))
        await ctx.reply(f"Playing {Music.Name}")
    else:
        await ctx.reply("No more songs in queue")

async def setup(bot: commands.bot):
    bot.add_command(next)