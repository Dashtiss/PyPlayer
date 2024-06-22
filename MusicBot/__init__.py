import discord
from discord.ext import commands
from .error import error, warn, log
import os
from os.path import join
intents = discord.Intents.all()
import asyncio
from .Settings import BASE_DIR, CMD_DIR, UPLOADS_DIR
# Start a task to leave voice channel if idle for more than 5 seconds




bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    log("MusicBot Starting")
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    if len( bot.guilds ) == 0:
        warn("The bot is not in a server")

    log("Loading Commands")
    for file in CMD_DIR.glob("*.py"):
        try:
            await bot.load_extension(f"MusicBot.Commands.{file.name[:-3]}")
            log(f"Loaded MusicBot.Commands.{file.name[:-3]}")
        except (commands.errors.ExtensionFailed, commands.errors.NoEntryPointError):
            error(f"MusicBot.Commands.{file.name[:-3]} failed to load skipping but it may break the bot. If you have problems, please report it in Issues of the github repo")



def Startup(TOKEN: str):
    bot.run(TOKEN)