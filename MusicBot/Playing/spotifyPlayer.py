import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import yt_dlp
from ..Settings import UPLOADS_DIR
from ..error import error
from ..Classes import PlayableMusic, FutureMusic
from youtubesearchpython import VideosSearch
from discord import FFmpegPCMAudio
from ..Audio import turntomp3
from typing import Generator
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

def GetVideoUrl(Name: str, Artist: str, Album: str) -> str:
    vid = VideosSearch(f"{Name} {Artist} {Album}", limit=1)
    return vid.result()["result"][0]["link"]

def AddToQueuePlaylist(PlaylistURL: str) -> Generator[FutureMusic, None, None]:
    offset = 0
    limit = 100  # This is Spotify's typical limit for playlist items
    SongLimit = 10
    AmmountItems = 0
    while AmmountItems < SongLimit:
        results = spotify.playlist_items(PlaylistURL, offset=offset, limit=limit)
        if not results['items']:
            break  # Exit the loop if no more items are returned

        for item in results['items']:
            try:
                song = FutureMusic(
                    Name=item['track']['name'],
                    VideoURL=GetVideoUrl(
                        item['track']['name'],
                        item['track']['artists'][0]['name'],
                        item['track']['album']['name']
                    ),
                    artists=item['track']['artists'][0]['name'],
                    album=item['track']['album']['name']
                )
                yield song

                AmmountItems += 1
            except KeyError as e:
                print(f"KeyError: {e} in item {item}")  # Handle potential missing keys

        #offset += limit  # Move to the next batch

async def AddToQueueTrack(TrackURL: str) -> PlayableMusic:
    Track = spotify.track(TrackURL)["external_urls"]['name']
    Song = await FindAndDownloadSong(Track)
    # will add song to queue

    return Song

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
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        vid = VideosSearch(f"{name} {artists}, {album}", limit=1)
        title = vid.result()["result"][0]['title']
        print(f"{title}.mp3")
        for item in os.listdir(UPLOADS_DIR):
            if item == f"{title}.mp3":
                return PlayableMusic(Name=name, Duration=0, Path=os.path.join(UPLOADS_DIR, f"{name}.mp3"))
            
        ydl.download([vid.result()["result"][0]["link"]])
        if title[-4:] == ".webm":
            await turntomp3.webm_to_mp3(os.path.join(UPLOADS_DIR, f"{title}.webm"), os.path.join(UPLOADS_DIR, f"{title}.mp3"))
        return PlayableMusic(Name=name, Duration=0, Path=os.path.join(UPLOADS_DIR, f"{name}.mp3"))
    

def DownloadSong(URL: str, Name: str) -> PlayableMusic:


    # Download the YouTube video
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(UPLOADS_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"{Name}.mp3")
        for item in os.listdir(UPLOADS_DIR):
            if item == f"{Name}.mp3":
                return PlayableMusic(Name=Name, Duration=0, Path=os.path.join(UPLOADS_DIR, f"{Name}.mp3"))
        ydl.download(URL)
        if Name[-4:] == ".webm":
            turntomp3.webm_to_mp3(os.path.join(UPLOADS_DIR, f"{Name}.webm"), os.path.join(UPLOADS_DIR, f"{Name}.mp3"))
        return PlayableMusic(Name=Name, Duration=0, Path=os.path.join(UPLOADS_DIR, f"{Name}.mp3"))