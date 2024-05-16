
from typing import List

def parse_music(music_string: str) -> List[int]:
    beats = {'o': 4, 'o|': 2, '.|': 1}
    notes = music_string.split()
    return [beats[note] for note in notes]

# Test the function
print(parse_music('o o| .| o| o| .| .| .| .| o o'))
