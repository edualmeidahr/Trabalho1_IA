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


# Hill Climbing Simples (movimentos laterais)
def hill_climbing(  
    board_factory: Callable[[], Board], 
    max_iterations: int = 1000,
    lateral_moves_limits: int = 0
) -> HillClimbingResult:
    


    current_board = board_factory()
    current_cost = conflicts(current_board)
    total_steps = 0
    lateral_moves_done = 0


    for _ in range(max_iterations):
        
        if current_cost == 0:

            return HillClimbingResult(
                final_board=current_board,
                final_cost=current_cost,
                total_steps=total_steps
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

            # mover para o melhor vizinho
            current_board = random.choice(better_moves)
            current_cost = best_better_cost
            total_steps += 1
            lateral_moves_done = 0

        elif lateral_moves and lateral_moves_done < lateral_moves_limits:

            # mover lateralmente
            current_board = random.choice(lateral_moves)
            total_steps += 1
            lateral_moves_done += 1

        else:
            # nenhum movimento possível
            break

    return HillClimbingResult(
        final_board=current_board,
        final_cost=current_cost,
        total_steps=total_steps
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


    for i in range(max_restarts + 1): 

        run_result = hill_climbing(
            board_factory=initial_board,
            max_iterations=max_iterations_per_restart,
            lateral_moves_limits=lateral_moves_limits
        )


        total_steps_accumulated += run_result.total_steps

        if run_result.final_cost < best_overall_cost:
            
            best_overall_cost = run_result.final_cost
            best_overall_board = run_result.final_board

        if best_overall_cost == 0:
            return HillClimbingResult(
                final_board=best_overall_board,
                final_cost=best_overall_cost,
                total_steps=total_steps_accumulated,
                restarts_done=i
            )

    return HillClimbingResult(
        final_board=best_overall_board,
        final_cost=best_overall_cost,
        total_steps=total_steps_accumulated,
        restarts_done=max_restarts  
    )    


