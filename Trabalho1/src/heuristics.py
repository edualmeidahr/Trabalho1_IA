from typing import Tuple
import math

Pos = Tuple[int, int]

def manhattan_distance(pos1: Pos, pos2: Pos) -> int: 

    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def euclidean_distance(pos1: Pos, pos2: Pos) -> float:
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return math.sqrt(dx * dx + dy * dy)

