import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import yt_dlp
from ..Settings import UPLOADS_DIR
from ..error import error
from ..Classes import PlayableMusic
from youtubesearchpython import VideosSearch
from discord import FFmpegPCMAudio
from ..Audio import turntomp3

load_dotenv()

import os

username = os.environ["SpotifyUser"]
clientID = os.environ["ClientId"]
clientSecret = os.environ["ClientSecret"]
redirect_uri = 'http://google.com/callback/'

spotify = spotipy.Spotify(
    client_credentials_manager=
    SpotifyClientCredentials(
        client_id=clientID,
        client_secret=clientSecret,

    )
)


async def FindAndDownloadSong(song: str) -> PlayableMusic:

    results = spotify.search(song, type="track", limit=1)

    for item in results['tracks']['items']:
        # will get the name of the track
        name = item['name']
        # will get the artists of the track
        artists = item['artists'][0]['name']
        # will get the album of the track
        album = item['album']['name']


    # Download the YouTube video
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(UPLOADS_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
    }
    defaultUrl = "https://www.youtube.com/watch?v="
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        vid = VideosSearch(f"{name} {artists}", limit=1)
        title = vid.result()["result"][0]['title']
        print(f"{title}.mp3")
        for item in os.listdir(UPLOADS_DIR):
            if item == f"{title}.mp3":
                return PlayableMusic(Name=name, Duration=0, Path=os.path.join(UPLOADS_DIR, f"{name}.mp3"))
            
        ydl.download([vid.result()["result"][0]["link"]])
        if title[-4:] == ".webm":
            await turntomp3.webm_to_mp3(os.path.join(UPLOADS_DIR, f"{title}.webm"), os.path.join(UPLOADS_DIR, f"{title}.mp3"))
        return PlayableMusic(Name=name, Duration=0, Path=os.path.join(UPLOADS_DIR, f"{name}.mp3"))