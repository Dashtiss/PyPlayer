from dataclasses import dataclass


@dataclass
class PlayableMusic:
    Name: str
    Duration: int
    Path: str


@dataclass
class FutureMusic:
    Name: str
    artists: str
    album: str
    VideoURL: str