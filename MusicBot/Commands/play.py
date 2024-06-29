"""
This file contains the commands for the play command which allows the user to play songs from YouTube and other sources.

The play command takes either a URL or a file attachment. If a URL is given the bot will download the song from YouTube and add it to the queue.

If a file is attached to the message, the bot will download the file and add it to the queue, also checking if the file is a virus using Virus Total.

The play command also handles the play functionality for the bot, starting the audio after any pause commands have been used. 

This file also contains the setup function which is used to add the play command to the bot.
"""
import os
import yt_dlp
from discord.ext import commands
from discord import FFmpegPCMAudio
from ..Settings import UPLOADS_DIR
from ..error import error
from ..Classes import PlayableMusic
from .. import Playing
from ..Playing import UploadFiles, spotifyPlayer
from os.path import join
import requests
import asyncio
import spotipy
from spotipy import  SpotifyClientCredentials
from ..Audio import turntomp3




@commands.command()
async def play(ctx: commands.Context, *, url: str = None):
    """
    Command to play music from a YouTube URL or attached file.

    Parameters:
    - ctx (commands.Context): The context of the command.
    - url (str, optional): The URL of the YouTube video to play.

    This function checks if a URL is provided. If so, it downloads the video and adds it to the queue.
    If not, it checks if any files are attached to the message and downloads them, checking if they are viruses.
    """

    if ctx.author.id != 690225608474492934:
        await ctx.reply("Only the bot owner can use this command", ephemeral=True)
        return

    # Check if a YouTube URL is provided
    if url:
        # Strip the URL of the "https://" prefix and split it by "/"
        url_parts = url.strip("https://").split("/")
        print(url_parts[0])
        print(os.listdir(UPLOADS_DIR))
        if url in os.listdir(UPLOADS_DIR):
            Playing.AddToQueue(PlayableMusic(Name=url, Duration=0, Path=join(UPLOADS_DIR, url)))
            print(f"Adding {url} to queue")
        elif url_parts[0] in ("youtube.com", "youtu.be", "www.youtube.com", "www.youtu.be"):    
            # Download the YouTube video
            Music = await DownloadYT(url)
            # Add the downloaded music to the queue if successful
            if Music:
                Playing.AddToQueue(Music)
                print(f"Adding {Music.Name} to queue")
        elif url_parts[0] in ("open.spotify.com", "spotify.com"):
            # will log into spotify
            ...
        else:
            song = await spotifyPlayer.FindAndDownloadSong(url)
            if song.Name[-4:] == ".webm":
                await turntomp3.webm_to_mp3(song.Path, song.Path[:-4] + ".mp3")
            Playing.AddToQueue(song)
            print(f"Adding {song.Name} to queue")

    # Check if any files are attached to the message
    if len(ctx.message.attachments) > 0:
        # Create the uploads directory if it doesn't exist
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        # Iterate over each attached file
        for File in ctx.message.attachments:
            # Check if the file has already been downloaded
            if File.filename in os.listdir(UPLOADS_DIR):
                Playing.AddToQueue(
                    PlayableMusic(
                        Name=File.filename,
                        Duration=0,
                        Path=join(
                                UPLOADS_DIR, 
                                File.filename
                        )
                    )
                )
                print(f"Adding {File.filename} to queue")
                continue

            # Check if the file is not a virus
            if await UploadFiles.ScanURL(File.url):
                # Download the file
                r = requests.get(File.url)
                # Save the file to the uploads directory
                with open(join(UPLOADS_DIR, File.filename), "wb") as AudioFile:
                    AudioFile.write(r.content)
                Playing.AddToQueue(
                    PlayableMusic(
                        Name=File.filename,
                        Duration=0,
                        Path=join(
                                UPLOADS_DIR, 
                                File.filename
                        )
                    )
                )
                print(f"Adding {File.filename} to queue")
            else:
                # Reply to the user that the file is a virus
                print(f"File {File.filename} has been detected as a virus")
    # Start playing the queue if it is not already playing
    if not Playing.Playing:
        for music in Playing.StartPlaying():
            # Will join the voice channel if it is not already in one
            if not ctx.voice_client:
                
                await ctx.author.voice.channel.connect()
            # Play the music
            ctx.voice_client.play(music)
            Playing.Playing = True
            # Wait until the music is finished
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

async def DownloadYT(url: str) -> PlayableMusic | None:
    """
    Download the YouTube video
    
    Parameters:
    - url: str - The URL of the video to download.
    
    Returns:
    - PlayableMusic | None
    """
    # Download the YouTube video
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(UPLOADS_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            duration = info_dict.get('duration', 0)  # Duration in seconds
            #            print(f"Title: {info_dict['title']}")
            #            print(f"Duration: {duration} seconds")
            return PlayableMusic(Name=info_dict["title"], Duration=duration, Path=file_path)
        except Exception as e:
            error(f"An error occurred while downloading the video: {e}")
            return None


async def setup(bot):
    bot.add_command(play)
