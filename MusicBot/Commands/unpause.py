from discord.ext import commands
import discord


@commands.command()
async def unpause(ctx):
    guild: discord.guild = ctx.guild
    if guild.voice_client and guild.voice_client.is_playing():
        guild.voice_client.resume()
        await ctx.send("Paused the audio.")
    else:
        await ctx.send("No audio is playing to pause.")

async def setup(bot):
    bot.add_command(unpause)