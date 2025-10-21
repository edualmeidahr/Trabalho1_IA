from typing import Tuple

Pos = Tuple[int, int]

def manhattan_distance(pos1: Pos, pos2: Pos) -> int: 

    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

