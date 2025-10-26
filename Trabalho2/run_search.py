"""
Arquivo: run_search.py

Este script executa os experimentos de busca para o problema das 8 Rainhas,
comparando as duas variações do Hill Climbing conforme solicitado:
(i)  Hill Climbing com Movimentos Laterais
(ii) Hill Climbing com Reinícios Aleatórios (Random-Restart)

Ele roda cada algoritmo N vezes para coletar estatísticas e
reporta as métricas de desempenho (taxa de sucesso, tempo, etc.)
e salva um log detalhado de cada execução em arquivos .txt.
"""

import time
import statistics
from typing import List

from src.eight_queens import initial_board, Board 
from src.hill_climbing import (
    hill_climbing, 
    hill_climbing_random_restart, 
    HillClimbingResult
)

# --- Constantes do Experimento ---
N_EXECUTIONS = 100

MAX_ITERATIONS_LATERAL = 1000
LATERAL_MOVES_LIMITS = 100 

MAX_RESTARTS = 100
MAX_ITERATIONS_PER_RESTART = 100
LATERAL_MOVES_PER_RESTART = 0

# --- Nomes dos Arquivos de Log ---
LOG_FILE_LATERAL = "relatorios/relatorio_lateral_moves.txt"
LOG_FILE_RESTART = "relatorios/relatorio_random_restart.txt"
SEPARATOR = "-" * 60 + "\n"




def format_board_as_grid(board: Board) -> str:
    """
    Converte um tabuleiro em formato de vetor (ex: [1, 5, ...])
    em uma grade 8x8 visual com 'x' marcando as rainhas.
    """
    # Constante N=8 
    N = 8

    if not board:
        return "    (Tabuleiro não disponível)"
        
    grid_lines = []
    for r in range(N): 
        line_str = ""
        for c in range(N): # Itera pelas colunas
            # Verifica se a rainha da coluna 'c' está na linha 'r'
            if board[c] == r:
                line_str += " x "
            else:
                line_str += " . " # Ponto para espaço vazio
        grid_lines.append(line_str)
    
    # Junta todas as linhas com uma quebra de linha
    return "\n".join(grid_lines)


# --- Função de Relatório (Consolidado) ---
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
        avg_time_per_run_ms = (total_time / total_runs) * 1000
        avg_steps_on_success = statistics.mean(r.total_steps for r in successful_runs)
        avg_restarts_on_success = statistics.mean(r.restarts_done for r in successful_runs)
        
    else:
        avg_time_per_run_ms = (total_time / total_runs) * 1000
        avg_steps_on_success = float('nan')
        avg_restarts_on_success = float('nan')

    
    # Imprime o relatório (no console)
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
    print(f"Salvando relatório detalhado em: {LOG_FILE_LATERAL}\n")
    
    results_lateral_moves = []
    start_time_exp1_total = time.perf_counter()
    
    with open(LOG_FILE_LATERAL, "w", encoding="utf-8") as f_log:
        f_log.write(f"RELATÓRIO DE DESEMPENHO: Hill Climbing com Movimentos Laterais\n")
        f_log.write(f"Parâmetros: max_iter={MAX_ITERATIONS_LATERAL}, lateral_moves={LATERAL_MOVES_LIMITS}\n")
        f_log.write(SEPARATOR)

        for i in range(N_EXECUTIONS):
            start_time_run = time.perf_counter()
            
            result = hill_climbing(
                board_factory=initial_board,
                max_iterations=MAX_ITERATIONS_LATERAL,
                lateral_moves_limits=LATERAL_MOVES_LIMITS
            )
            
            end_time_run = time.perf_counter()
            run_time_ms = (end_time_run - start_time_run) * 1000
            
            results_lateral_moves.append(result)
            
            
            initial_board_grid = format_board_as_grid(result.initial_board)
            final_board_grid = format_board_as_grid(result.final_board)
            
            # Indenta a grade para o log ficar alinhado
            initial_board_str = "\n".join(f"        {line}" for line in initial_board_grid.split('\n'))
            final_board_str = "\n".join(f"        {line}" for line in final_board_grid.split('\n'))
            
            solucao_str = "Sim" if result.final_cost == 0 else f"Não (Conflitos: {result.final_cost})"
            
            
            log_entry = (
                f"Execução {i + 1}:\n"
                f"    Estado inicial do tabuleiro:\n{initial_board_str}\n\n"
                f"    Estado final do tabuleiro:\n{final_board_str}\n"
                f"    Solução encontrada? {solucao_str}\n"
                f"    Tempo de execução: {run_time_ms:.4f} ms\n"
                f"    Passos totais: {result.total_steps}\n"
                f"    Número de movimentos laterais: {result.total_lateral_moves}\n"
                f"{SEPARATOR}"
            )
            f_log.write(log_entry)
            
    end_time_exp1_total = time.perf_counter()
    total_time_exp1 = end_time_exp1_total - start_time_exp1_total
    
    print(f"...Experimento 1 concluído.")
    
    
    # --- Experimento 2: (ii) Hill Climbing com Random-Restart ---
    
    print(f"\nIniciando Experimento 2: Hill Climbing com Random-Restart...")
    print(f"Parâmetros: {N_EXECUTIONS} execuções, max_restarts={MAX_RESTARTS}, iter/restart={MAX_ITERATIONS_PER_RESTART}")
    print(f"Salvando relatório detalhado em: {LOG_FILE_RESTART}\n")
    
    results_random_restart = []
    start_time_exp2_total = time.perf_counter()

    with open(LOG_FILE_RESTART, "w", encoding="utf-8") as f_log:
        f_log.write(f"RELATÓRIO DE DESEMPENHO: Hill Climbing com Random-Restart\n")
        f_log.write(f"Parâmetros: max_restarts={MAX_RESTARTS}, iter/restart={MAX_ITERATIONS_PER_RESTART}, lateral_moves/restart={LATERAL_MOVES_PER_RESTART}\n")
        f_log.write(SEPARATOR)

        for i in range(N_EXECUTIONS):
            start_time_run = time.perf_counter()
            
            result = hill_climbing_random_restart(
                max_restarts=MAX_RESTARTS,
                max_iterations_per_restart=MAX_ITERATIONS_PER_RESTART,
                lateral_moves_limits=LATERAL_MOVES_PER_RESTART
            )
            
            end_time_run = time.perf_counter()
            run_time_ms = (end_time_run - start_time_run) * 1000
            
            results_random_restart.append(result)
            
            
            initial_board_grid = format_board_as_grid(result.initial_board)
            final_board_grid = format_board_as_grid(result.final_board)
            
            # Indenta a grade para o log ficar alinhado
            initial_board_str = "\n".join(f"        {line}" for line in initial_board_grid.split('\n'))
            final_board_str = "\n".join(f"        {line}" for line in final_board_grid.split('\n'))
            
            solucao_str = "Sim" if result.final_cost == 0 else f"Não (Conflitos: {result.final_cost})"
            
           
            log_entry = (
                f"Execução {i + 1}:\n"
                f"    Estado inicial do tabuleiro:\n{initial_board_str}\n\n"
                f"    Estado final do tabuleiro:\n{final_board_str}\n"
                f"    Solução encontrada? {solucao_str}\n"
                f"    Tempo de execução: {run_time_ms:.4f} ms\n"
                f"    Passos totais (acumulados): {result.total_steps}\n"
                f"    Número de reinícios feitos: {result.restarts_done}\n"
                f"{SEPARATOR}"
            )
            f_log.write(log_entry)

    end_time_exp2_total = time.perf_counter()
    total_time_exp2 = end_time_exp2_total - start_time_exp2_total
    
    print(f"...Experimento 2 concluído.")

    
    # --- Apresentação dos Resultados ---
    
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
