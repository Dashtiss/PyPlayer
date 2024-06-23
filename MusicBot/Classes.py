from dataclasses import dataclass


@dataclass
class PlayableMusic:
    Name: str
    Duration: int
    Path: str