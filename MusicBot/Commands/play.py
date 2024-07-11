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
from ..Classes import PlayableMusic, FutureMusic
from .. import Playing
from ..Playing import UploadFiles, spotifyPlayer
from os.path import join
import requests
import asyncio
import spotipy
from spotipy import SpotifyClientCredentials
from ..Audio import turntomp3


async def LeaveCall(ctx: commands.Context):
    raise NotImplementedError("You havent emplemted the LeaveFunction")

@commands.command()
async def play(ctx: commands.Context, *, url: str = None):
    """
    Command to play music from a YouTube URL or attached file.

    Args:
        ctx (commands.Context): The context of the command.
        url (str, optional): The URL of the YouTube video to play.
    """
    # Check if the user is the bot owner
    # if ctx.author.id != 0:
    #     await ctx.reply("Only the bot owner can use this command", ephemeral=True)
    #     return

    if url:
        # Split the URL to get the domain
        url_parts = url.strip("https://").split("/")

        # Check if the URL is a file in the uploads directory
        if url in os.listdir(UPLOADS_DIR):
            playable_music = PlayableMusic(Name=url, Duration=0, Path=join(UPLOADS_DIR, url))
            Playing.AddToQueue(playable_music)
        # Check if the URL is a YouTube video
        elif url_parts[0] in ("youtube.com", "youtu.be", "www.youtube.com", "www.youtu.be"):
            playable_music = await DownloadYT(url)
            if playable_music:
                Playing.AddToQueue(playable_music)
        # Check if the URL is a Spotify link
        elif url_parts[0] in ("open.spotify.com", "spotify.com", "www.spotify.com"):
            # Check if the link is for a track
            if "track" in url_parts[1]:
                song = await spotifyPlayer.AddToQueueTrack(url)
                Playing.AddToQueue(song)
            # Check if the link is for a playlist
            if "playlist" in url_parts[1]:
                await ctx.reply("DONT USE THIS ERRORS HAPPEN")
                for song in spotifyPlayer.AddToQueuePlaylist(url):
                    Playing.AddToQueue(song)
        # Check if the URL is a generic Spotify link
        else:
            song = await spotifyPlayer.FindAndDownloadSong(url)
            if song.Name.endswith(".webm"):
                await turntomp3.webm_to_mp3(song.Path, f"{song.Path[:-4]}.mp3")
            Playing.AddToQueue(song)
    ############################################################
    #                        ADD ATTACHMENT                   #
    ############################################################

    # Check if there are any attachments in the message
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            # Check if the attachment is a file in the uploads directory
            if attachment.filename in os.listdir(UPLOADS_DIR):
                playable_music = PlayableMusic(
                    Name=attachment.filename, Duration=0, Path=join(UPLOADS_DIR, attachment.filename)
                )
                Playing.AddToQueue(playable_music)
            # Check if the attachment is a valid URL
            elif await UploadFiles.scan_url(attachment.url):
                r = requests.get(attachment.url)
                with open(join(UPLOADS_DIR, attachment.filename), "wb") as file:
                    file.write(r.content)
                playable_music = PlayableMusic(
                    Name=attachment.filename, Duration=0, Path=join(UPLOADS_DIR, attachment.filename)
                )
                Playing.AddToQueue(playable_music)

    # Start playing the music if not already playing
    if not Playing.Playing:
        if not ctx.voice_client:
            # Join the voice channel of the user
            await ctx.author.voice.channel.connect()
            # Set the bot to self-deaf mode
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
        # Start playing the music in the queue
        for music in Playing.StartPlaying():
            ctx.voice_client.play(music)
            Playing.playing = True


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


async def setup(bot: commands.Bot):
    bot.add_command(play)
