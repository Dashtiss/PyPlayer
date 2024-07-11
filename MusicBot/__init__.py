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
    command_prefix="m!",
    intents=intents
)
InVoice = False


@bot.event
async def on_ready():
    """
    Event that is called when the bot is ready to start working.
    """
    # Log that the bot has started
    log("MusicBot Starting")

    # Create the uploads directory if it doesn't exist
    os.makedirs(UPLOADS_DIR, exist_ok=True)

    # Check if the bot is in any server
    if len(bot.guilds) == 0:
        warn("The bot is not in a server")

    for guild in bot.guilds:
        print(f"Loaded MusicBot in {guild.name}")

    # Log that the bot is loading the commands
    log("Loading Commands")

    # Iterate over each file in the commands directory
    for file in CMD_DIR.glob("*.py"):
        try:
            # Load the extension from the file
            await bot.load_extension(f"MusicBot.Commands.{file.name[:-3]}")

            # Log that the command has been loaded
            log(f"Loaded MusicBot.Commands.{file.name[:-3]}")
        except commands.errors.ExtensionFailed as e:
            # Print the error and log that the command failed to load
            error(e)
            error(
                f"MusicBot.Commands.{file.name[:-3]} failed to load skipping but it may break the bot. If you have problems, please report it in Issues of the github repo\n {e}")
        except commands.errors.NoEntryPointError:
            # Continue to the next file if there is no entry point
            continue


@bot.command()
async def reload(ctx: commands.Context):
    if ctx.author.id != 690225608474492934:
        await ctx.reply("You do not have permission to run this")
        return
    await ctx.send("Reloading")
    for file in CMD_DIR.glob("*.py"):
        try:
            try:
                await bot.unload_extension(f"MusicBot.Commands.{file.name[:-3]}")
                await asyncio.sleep(0.2)
                # Load the extension from the file
                await bot.load_extension(f"MusicBot.Commands.{file.name[:-3]}")
                await ctx.reply(f"Reloaded MusicBot.Commands.{file.name[:-3]} Successfully")
            except commands.errors.ExtensionNotLoaded:
                await ctx.reply(f"Failed to Load MusicBot.Commands.{file.name[:-3]}")
            # Log that the command has been loaded
            log(f"Loaded MusicBot.Commands.{file.name[:-3]}")
        except Exception as e:
            # Print the error and log that the command failed to load
            error(e)
            await ctx.reply(f"Failed To Load MusicBot.Commands.{file.name[:-3]}")
            error(
                f"MusicBot.Commands.{file.name[:-3]} failed to load skipping but it may break the bot. If you have problems, please report it in Issues of the github repo\n {e}")



def Startup(TOKEN: str):
    bot.run(TOKEN)


def main() -> None:
    from dotenv import load_dotenv
    load_dotenv()
    Startup(os.environ["TOKEN"])


if __name__ == "__main__":
    main()
