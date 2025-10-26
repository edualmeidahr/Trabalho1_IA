"""
Arquivo: run_search.py

Este script executa os experimentos de busca para o problema das 8 Rainhas,
comparando as duas variações do Hill Climbing conforme solicitado:
(i)  Hill Climbing com Movimentos Laterais
(ii) Hill Climbing com Reinícios Aleatórios (Random-Restart)

Ele roda cada algoritmo N vezes para coletar estatísticas e
reporta as métricas de desempenho (taxa de sucesso, tempo, etc.).
"""

import time
import statistics
from typing import List

from src.eight_queens import initial_board
from src.hill_climbing import (
    hill_climbing, 
    hill_climbing_random_restart, 
    HillClimbingResult
)

N_EXECUTIONS = 100

MAX_ITERATIONS_LATERAL = 1000

LATERAL_MOVES_LIMITS = 100

MAX_RESTARTS = 100

MAX_ITERATIONS_PER_RESTART = 100

LATERAL_MOVES_PER_RESTART = 0


# feita por IA
def print_results(title: str, results_list: List[HillClimbingResult], total_time: float):
    """
    Calcula e imprime as métricas de um conjunto de execuções.
    
    Args:
        title (str): O título do experimento.
        results_list (List[HillClimbingResult]): A lista de objetos de resultado.
        total_time (float): O tempo total para rodar N_EXECUTIONS.
    """
    total_runs = len(results_list)
    successful_runs = [r for r in results_list if r.final_cost == 0]
    num_success = len(successful_runs)

    total_runs = len(results_list)
    successful_runs = [r for r in results_list if r.final_cost == 0]
    num_success = len(successful_runs)
    
    # 1. Taxa de Sucesso
    success_rate = (num_success / total_runs) * 100
    
    # 2. Métricas de execuções COM SUCESSO
    if num_success > 0:
        # Tempo médio para encontrar uma solução
        # (O tempo de cada "run" foi armazenado no total_steps 
        # para este exemplo simples, mas vamos usar o tempo total / execuções)
        # Nota: O tempo individual por "run" é mais preciso.
        # Vamos calcular o tempo médio por execução *total* (incluindo falhas)
        avg_time_per_run_ms = (total_time / total_runs) * 1000
        
        # Média de passos em execuções de sucesso
        avg_steps_on_success = statistics.mean(r.total_steps for r in successful_runs)
        
        # Média de reinícios (só se aplica ao Random-Restart)
        avg_restarts_on_success = statistics.mean(r.restarts_done for r in successful_runs)
        
    else:
        avg_time_per_run_ms = (total_time / total_runs) * 1000
        avg_steps_on_success = float('nan')
        avg_restarts_on_success = float('nan')

    
    # Imprime o relatório
    print("\n" + "="*50)
    print(f"RELATÓRIO DE DESEMPENHO: {title}")
    print("="*50)
    print(f"Executado {total_runs} vezes em {total_time:.4f} segundos.")
    print(f"Tempo médio por execução: {avg_time_per_run_ms:.4f} ms")
    print(f"Taxa de Sucesso: {success_rate:.2f}% ({num_success} / {total_runs})")
    
    print("\nMétricas (apenas para execuções com SUCESSO):")
    if num_success > 0:
        print(f"  - Média de Passos (totais) por Solução: {avg_steps_on_success:.2f}")
        
        # Só imprime a métrica de reinício se ela for relevante (i.e., > 0)
        if avg_restarts_on_success > 0:
            print(f"  - Média de Reinícios por Solução: {avg_restarts_on_success:.2f}")
    else:
        print("  - Nenhuma execução encontrou a solução.")
    
    print("="*50 + "\n")



def main():
    """
    Roda os dois experimentos e compara os resultados.
    """
    
    # --- Experimento 1: (i) Hill Climbing com Movimentos Laterais ---
    
    print(f"Iniciando Experimento 1: Hill Climbing com Movimentos Laterais...")
    print(f"Parâmetros: {N_EXECUTIONS} execuções, max_iter={MAX_ITERATIONS_LATERAL}, lateral_moves={LATERAL_MOVES_LIMITS}")
    
    results_lateral_moves = []
    start_time_exp1 = time.perf_counter()
    
    for i in range(N_EXECUTIONS):
        # O 'initial_board' é passado como a fábrica
        # Graças ao random.seed(42), ele gerará a mesma
        # sequência de tabuleiros para ambos os experimentos.
        result = hill_climbing(
            board_factory=initial_board,
            max_iterations=MAX_ITERATIONS_LATERAL,
            lateral_moves_limits=LATERAL_MOVES_LIMITS
        )
        results_lateral_moves.append(result)
        
    end_time_exp1 = time.perf_counter()
    total_time_exp1 = end_time_exp1 - start_time_exp1
    
    print(f"...Experimento 1 concluído.")
    
    
    # --- Experimento 2: (ii) Hill Climbing com Random-Restart ---
    
    print(f"\nIniciando Experimento 2: Hill Climbing com Random-Restart...")
    print(f"Parâmetros: {N_EXECUTIONS} execuções, max_restarts={MAX_RESTARTS}, iter/restart={MAX_ITERATIONS_PER_RESTART}")
    
    results_random_restart = []
    start_time_exp2 = time.perf_counter()

    for i in range(N_EXECUTIONS):
        # Esta função já chama 'initial_board' internamente
        result = hill_climbing_random_restart(
            max_restarts=MAX_RESTARTS,
            max_iterations_per_restart=MAX_ITERATIONS_PER_RESTART,
            lateral_moves_limits=LATERAL_MOVES_PER_RESTART
        )
        results_random_restart.append(result)

    end_time_exp2 = time.perf_counter()
    total_time_exp2 = end_time_exp2 - start_time_exp2
    
    print(f"...Experimento 2 concluído.")

    
    # --- Apresentação dos Resultados ---
    
    # Imprime os relatórios
    print_results(
        "Hill Climbing com Movimentos Laterais", 
        results_lateral_moves, 
        total_time_exp1
    )
    
    print_results(
        "Hill Climbing com Random-Restart", 
        results_random_restart, 
        total_time_exp2
    )

if __name__ == "__main__":
    main()
