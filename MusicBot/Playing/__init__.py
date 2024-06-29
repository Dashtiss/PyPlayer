from typing import Generator
from discord import FFmpegPCMAudio
import random
from ..Classes import PlayableMusic

# Initialize the queue with a PlayableMusic object
queue: list[PlayableMusic] = []
Playing: bool = False


def StartPlaying():
    for Music in queue:
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
