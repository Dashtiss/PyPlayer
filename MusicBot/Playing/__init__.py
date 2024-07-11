from typing import Generator
from discord import FFmpegPCMAudio
import random
from ..Classes import PlayableMusic, FutureMusic
from . import spotifyPlayer
# Initialize the queue with a PlayableMusic object
queue: list[PlayableMusic] = []
Playing: bool = False


def StartPlaying():
    for Music in queue:
        if type(Music) == FutureMusic:
            song = spotifyPlayer.DownloadSong(Music.VideoURL, Music.Name)
            yield FFmpegPCMAudio(song.Path)
        else:
            yield FFmpegPCMAudio(Music.Path)



def AddToQueue(Music: PlayableMusic):
    queue.append(Music)


def ShuffleQueue() -> bool:
    if len(queue) > 0:
        try:
            random.shuffle(queue)
            return True
        except Exception as E:
            # Handle the exception if needed
            print(f"Exception caught at shuffle: {E}")
            return False
