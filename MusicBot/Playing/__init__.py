from discord import FFmpegPCMAudio
import random
from ..Classes import PlayableMusic

# Initialize the queue with a PlayableMusic object
queue: list[PlayableMusic] = []
Playing: bool = False


def StartPlaying(MusicName: str = None) -> FFmpegPCMAudio | None:
    if MusicName:
        if any(file.Name == MusicName for file in queue):
            index = next((index for index, file in enumerate(queue) if file.Name == MusicName), None)
            if index is not None:
                print(queue[index].Name)
                return FFmpegPCMAudio(queue[index].Path)
        return None
    else:
        for Item in queue:
            yield FFmpegPCMAudio(Item.Path)

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
    return False
