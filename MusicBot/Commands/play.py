import os
import asyncio
import yt_dlp
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get

from ..Settings import BASE_DIR  # Assuming BASE_DIR is defined in Settings
from ..error import log  # Importing log function from error module

# Global variable to store the task for leaving voice channel if idle
leave_voice_task = None


def cancel_leave_task():
    """
    Cancel the leave voice task if it's active and not done.
    """
    global leave_voice_task
    if leave_voice_task and not leave_voice_task.done():
        leave_voice_task.cancel()


@commands.group()
async def play(ctx, *, url: str = None):
    """
    Play a specified YouTube video or a local file from the uploads directory.
    """
    if ctx.invoked_subcommand is None:
        # Cancel any existing leave task since bot is active
        cancel_leave_task()

        if not url:
            await ctx.send('You must specify a YouTube URL or file name to play.')
            return

        # Ensure the bot joins the voice channel
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)

            if voice_client and voice_client.is_connected():
                await voice_client.move_to(channel)
            else:
                voice_client = await channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            return

        upload_dir = os.path.join(BASE_DIR, "Uploads")
        file_path = None

        # Check if the input is a URL or a file name
        if url.startswith('http://') or url.startswith('https://'):
            # Download the YouTube video
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(upload_dir, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info_dict = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info_dict)
                except Exception as e:
                    await ctx.send(f"An error occurred while downloading the video: {e}")
                    return
        else:
            # Handle as a file name
            file_name = url
            valid_extensions = [".mp3", ".wav", ".mp4"]

            if os.path.isfile(os.path.join(upload_dir, file_name)):
                file_path = os.path.join(upload_dir, file_name)
            else:
                for ext in valid_extensions:
                    if os.path.isfile(os.path.join(upload_dir, file_name + ext)):
                        file_path = os.path.join(upload_dir, file_name + ext)
                        break

        if file_path:
            # Play the audio file
            audio_source = FFmpegPCMAudio(file_path)
            if not voice_client.is_playing():
                voice_client.play(audio_source)
                await ctx.send(f'Now playing: {file_path}')
            else:
                await ctx.send('Already playing an audio file. Please wait until it finishes.')
        else:
            await ctx.send(f'The file {url} was not found in the uploads directory or the video download failed.')

        async def leave_after_idle():
            """
            Task to disconnect from voice channel after a period of inactivity.
            """
            while True:
                await asyncio.sleep(5)  # Check every 5 seconds

                if not voice_client.is_playing():
                    await voice_client.disconnect()
                    await ctx.send("Leaving voice channel due to inactivity.")
                    break

        # Start the leave after idle task
        global leave_voice_task
        leave_voice_task = ctx.bot.loop.create_task(leave_after_idle())

@play.command()
async def spotify(ctx: commands.Context, Url: str = ""):
    log("Playing spotify")



async def setup(bot):
    bot.add_command(play)
