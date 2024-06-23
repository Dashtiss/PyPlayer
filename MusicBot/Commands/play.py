import os
import yt_dlp
from discord.ext import commands
from ..Settings import UPLOADS_DIR
from ..error import error
from ..Classes import PlayableMusic
from .. import Playing
from ..Playing import UploadFiles
from os.path import join
import requests


@commands.command()
async def play(ctx: commands.Context, *, url: str = None):
    if url:
        if url.strip("https://").split("/")[0] in ("youtube.com", "youtu.be"):
            Music = await DownloadYT(url)
            if Music:
                Playing.AddToQueue(Music)
    if len(ctx.message.attachments) > 0:
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        for File in ctx.message.attachments:
            if await UploadFiles.ScanURL(File.url):
                r = requests.get(File.url)
                with open(join(UPLOADS_DIR, File.filename), "wb") as AudioFIle:
                    AudioFIle.write(r.content)
                await ctx.reply(f"Uploaded {File.filename}", ephemeral=True)
            else:
                await ctx.reply(f"File {File.filename} has been detected as a virus", ephemeral=True)








async def DownloadYT(url: str) -> PlayableMusic | None:
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
