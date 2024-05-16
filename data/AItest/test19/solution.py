
from typing import List


def parse_music(music_string: str) -> List[int]:
    music_string = music_string.split()
    res = []
    for char in music_string:
        if char == 'o':
            res.append(4)
        elif char == 'o|':
            res.append(2)
        elif char == '.':
            res.append(1)
        else:
            print("Unsupported note value")
            return []
    return res
