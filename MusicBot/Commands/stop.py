from discord.ext import commands
from discord import FFmpegPCMAudio
from .. import Playing

@commands.command()
async def stop(ctx):
    """
    Pauses the music and stops playing.
    """
    if Playing.Playing:
        Playing.Playing = False
        player = ctx.voice_client
        player.pause()
        await ctx.reply("Music has been paused")
    else:
        await ctx.reply("Music is already paused")


@commands.command()
async def unpause(ctx):
    """
    Continues playing the music where it stopped.
    """
    if not Playing.Playing:
        Playing.Playing = True
        player = ctx.voice_client
        player.resume()
        await ctx.reply("Music has been unpaused")
    else:
        await ctx.reply("Music is not paused")


@commands.command()
async def leave(ctx):
    """
    Leaves the voice channel.
    """
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        Playing.Playing = False

async def setup(bot):
    bot.add_command(stop)
    bot.add_command(unpause)
    bot.add_command(leave)
