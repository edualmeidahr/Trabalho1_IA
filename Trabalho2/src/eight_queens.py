import random

from typing import List, Tuple, Iterable

random.seed(42)

N: int = 8

Board = list[int]

Move = Tuple[int, int] 


def initial_board() -> Board: 

    return [random.randint(0, N - 1) for _ in range(N)]



#Função para calcular o número de conflitos no tabuleiro
def conflicts(board: Board) -> int: 

    total_conflicts: int = 0

    for collumn1 in range(N): 

        r1: int = board[collumn1]

        for collumn2 in range(collumn1 + 1, N):
            r2: int = board[collumn2]

            if r1 == r2:
                total_conflicts += 1
            elif abs(r1 - r2) == abs(collumn1 - collumn2):
                total_conflicts += 1


    return total_conflicts


def neighbors(board: Board) -> Iterable[Move]: 

    for collumn in range(N):

        current_row: int = board[collumn]
        for row in range(N):
            
            # Movimento é apenas válido se a rainha se mover para uma linha diferente
            if row != current_row:
                yield (collumn, row)


def apply_move(board: Board, move: Move) -> Board: 


    collumn, row = move

    new_board: Board = board.copy()

    new_board[collumn] = row
    
    return new_board

