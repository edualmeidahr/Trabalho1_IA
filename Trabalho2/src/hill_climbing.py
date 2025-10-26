import random

from dataclasses import dataclass
from typing import Callable, Optional


from src.eight_queens import Board, apply_move, conflicts, neighbors, initial_board

@dataclass
class HillClimbingResult:

    final_board: Board
    final_cost: int
    total_steps: int
    restarts_done: int = 0
    initial_board: Optional[Board] = None # Armazena o tabuleiro inicial
    total_lateral_moves: int = 0         # Armazena o total de movimentos laterais


# Hill Climbing Simples (movimentos laterais)
def hill_climbing(  
    board_factory: Callable[[], Board], 
    max_iterations: int = 1000,
    lateral_moves_limits: int = 0
) -> HillClimbingResult:
    
    initial_board_log = board_factory()
    current_board = initial_board_log
    
    current_cost = conflicts(current_board)
    total_steps = 0
    lateral_moves_done = 0 # Contador de movimentos laterais *consecutivos*
    
    total_lateral_moves_accumulated = 0


    for _ in range(max_iterations):
        
        if current_cost == 0:
            # --- MUDANÇA: Retorna os novos campos de log ---
            return HillClimbingResult(
                final_board=current_board,
                final_cost=current_cost,
                total_steps=total_steps,
                initial_board=initial_board_log,
                total_lateral_moves=total_lateral_moves_accumulated
            )
        
        better_moves = []
        lateral_moves = []
        best_better_cost = current_cost

        # Passso 1: Avaliar os vizinhos
        for move in neighbors(current_board): 
            neighbor_board = apply_move(current_board, move)
            neighbor_cost = conflicts(neighbor_board)

            if neighbor_cost < current_cost:
                if neighbor_cost < best_better_cost:
                    best_better_cost = neighbor_cost
                    better_moves = [neighbor_board]
                elif neighbor_cost == best_better_cost:
                    better_moves.append(neighbor_board)
            elif neighbor_cost == current_cost:
                lateral_moves.append(neighbor_board)

        # Passo 2: Escolher o movimento a fazer
        if better_moves:
            current_board = random.choice(better_moves)
            current_cost = best_better_cost
            total_steps += 1
            lateral_moves_done = 0

        elif lateral_moves and lateral_moves_done < lateral_moves_limits:
            current_board = random.choice(lateral_moves)
            total_steps += 1
            lateral_moves_done += 1
            total_lateral_moves_accumulated += 1
        else:
            break

    return HillClimbingResult(
        final_board=current_board,
        final_cost=current_cost,
        total_steps=total_steps,
        initial_board=initial_board_log,
        total_lateral_moves=total_lateral_moves_accumulated
    )


# Hill Climbing com Reinícios Aleatórios
def hill_climbing_random_restart(
        max_restarts: int,
        max_iterations_per_restart: int,
        lateral_moves_limits: int = 0
    ) -> HillClimbingResult:

    best_overall_board =  None
    best_overall_cost = float('inf')
    total_steps_accumulated = 0
    
    first_initial_board = None


    for i in range(max_restarts + 1): 
        run_result = hill_climbing(
            board_factory=initial_board,
            max_iterations=max_iterations_per_restart,
            lateral_moves_limits=lateral_moves_limits
        )
        
        if i == 0:
            first_initial_board = run_result.initial_board

        total_steps_accumulated += run_result.total_steps

        if run_result.final_cost < best_overall_cost:
            best_overall_cost = run_result.final_cost
            best_overall_board = run_result.final_board

        if best_overall_cost == 0:

            return HillClimbingResult(
                final_board=best_overall_board,
                final_cost=best_overall_cost,
                total_steps=total_steps_accumulated,
                restarts_done=i,
                initial_board=first_initial_board
            )

    return HillClimbingResult(
        final_board=best_overall_board,
        final_cost=best_overall_cost,
        total_steps=total_steps_accumulated,
        restarts_done=max_restarts,
        initial_board=first_initial_board
    )