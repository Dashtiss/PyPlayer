from discord.ext import commands
from discord import FFmpegPCMAudio


@commands.command()
async def Stop(ctx):
    guild = ctx.guild

    if guild.voice_client and guild.voice_client.is_playing():
        guild.voice_client.pause()
        await ctx.send("Paused the audio.")
    else:
        await ctx.send("No audio is playing to pause.")


async def setup(bot):
    bot.add_command(Stop)
