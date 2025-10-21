#maze_representation.py
from typing import List, Tuple

Grid = List[List[str]]
Pos = Tuple[int, int]

class Maze:
   
    
    def __init__(self, grid: Grid):

        print("Mapa carregado:")
        for linha in grid:
            print("".join(linha))
    
        self.grid = grid
        self.H = len(grid)
        self.W = len(grid[0]) if self.H > 0 else 0
        self.start = self._find('S')
        self.goal = self._find('G')
        
    def _find(self, ch:str) -> Pos:
        for r in range(self.H):
            for c in range(self.W):
                if self.grid[r][c] == ch:
                    return (r, c)
        raise ValueError(f"Character {ch} not found in the grid")
    
    def in_bounds(self, pos: Pos) -> bool:
        r, c = pos
        return 0 <= r < self.H and 0 <= c < self.W
    
    def passable(self, pos: Pos) -> bool:
        r, c = pos
        return self.grid[r][c] != '#'
    
    def actions(self, p: Pos):
        # Retorna as ações possíveis a partir da posição p
        acts = []
        r, c = p
        candidates = {
            'N': (r-1, c),
            'S': (r+1, c),
            'O': (r, c-1),
            'L': (r, c+1)
        }
        for a, q in candidates.items():
            if self.in_bounds(q) and self.passable(q):
                acts.append(a)
        return acts
    
    def result(self, p:Pos, a:str) -> Pos:
        r, c = p
        delta = {
            'N': (-1, 0),
            'S': (1, 0),
            'O': (0, -1),
            'L': (0, 1)}
        dr, dc = delta[a]
        q = (r + dr, c + dc)
        if not (self.in_bounds(q) and self.passable(q)):
            raise ValueError(f"Action {a} from position {p} is not valid")
        return q
    
    def step_cost(self, p:Pos, a:str, q:Pos) -> float:
        return 1.0  # Custo uniforme para cada passo
    
    def goal_test(self, p:Pos) -> bool:
        return p == self.goal
    
