#!/usr/bin/env python3
"""
Script para testar todos os algoritmos de busca em múltiplos labirintos
"""

import time 
from datetime import datetime
from typing import List
import os
import glob

from src.search import a_star_search, dfs, bfs, greedy_search
from src.maze import Maze, Grid

ALGORITHMS_TO_RUN = {
    "Depth-First Search (DFS)": dfs,
    "Breadth-First Search (BFS)": bfs,
    "A* Search (A-Star)": a_star_search,
    "Greedy Best-First Search": greedy_search,
}

def read_mazes_from_file(input_file: str) -> List[Grid]:
    """Lê labirintos de um arquivo"""
    mazes = []
    current_maze = []
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                if not stripped_line: # Encontrou uma linha em branco (delimitador)
                    if current_maze:
                        mazes.append(current_maze)
                        current_maze = []
                else:
                    current_maze.append(list(stripped_line))
            
            # Adiciona o último labirinto se não terminou com linha em branco
            if current_maze:
                mazes.append(current_maze)
        return mazes
    except FileNotFoundError:
        print(f"Erro: O arquivo de entrada '{input_file}' não foi encontrado.")
        return []

def save_results(all_experiments_data, output_file):
    """Salva os resultados em um arquivo de relatório"""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("="*80 + "\n")
            file.write("        RELATÓRIO COMPARATIVO DOS ALGORITMOS DE BUSCA\n")
            file.write("="*80 + "\n\n")
            file.write(f"Data da Execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            file.write(f"Total de Labirintos Testados: {len(all_experiments_data)}\n\n")

            # Resumo geral
            file.write("="*50 + " RESUMO GERAL " + "="*50 + "\n\n")
            
            # Coleta estatísticas gerais
            algorithm_stats = {}
            for algorithm_name in ALGORITHMS_TO_RUN.keys():
                algorithm_stats[algorithm_name] = {
                    'total_time': 0,
                    'total_nodes': 0,
                    'total_memory': 0,
                    'solutions_found': 0,
                    'total_cost': 0,
                    'mazes_tested': 0
                }

            for maze_number, results_for_maze in all_experiments_data:
                for result in results_for_maze:
                    alg_name = result['algorithm']
                    algorithm_stats[alg_name]['mazes_tested'] += 1
                    algorithm_stats[alg_name]['total_time'] += result['time']
                    algorithm_stats[alg_name]['total_nodes'] += result['metrics']['nodes_expanded']
                    algorithm_stats[alg_name]['total_memory'] += result['metrics']['max_memory_usage']
                    
                    if result['solution_found']:
                        algorithm_stats[alg_name]['solutions_found'] += 1
                        algorithm_stats[alg_name]['total_cost'] += result['cost']

            # Escreve estatísticas gerais
            file.write(f"{'Algoritmo':<30} {'Sucessos':<10} {'Tempo Médio':<15} {'Nós Médios':<12} {'Memória Média':<15} {'Custo Médio':<12}\n")
            file.write("-" * 100 + "\n")
            
            for alg_name, stats in algorithm_stats.items():
                if stats['mazes_tested'] > 0:
                    success_rate = (stats['solutions_found'] / stats['mazes_tested']) * 100
                    avg_time = stats['total_time'] / stats['mazes_tested']
                    avg_nodes = stats['total_nodes'] / stats['mazes_tested']
                    avg_memory = stats['total_memory'] / stats['mazes_tested']
                    avg_cost = stats['total_cost'] / stats['solutions_found'] if stats['solutions_found'] > 0 else 0
                    
                    file.write(f"{alg_name:<30} {success_rate:>6.1f}% {avg_time:>12.6f}s {avg_nodes:>10.1f} {avg_memory:>13.1f} {avg_cost:>10.1f}\n")

            file.write("\n" + "="*80 + "\n\n")

            # Detalhes por labirinto
            for maze_number, results_for_maze in all_experiments_data:
                file.write("="*20 + f" ANÁLISE DO LABIRINTO {maze_number} " + "="*20 + "\n\n")

                for result in results_for_maze: 
                    file.write('-'*50 + "\n")
                    file.write(f"Algoritmo: {result['algorithm']}\n")
                    file.write("-"*50 + "\n")

                    if result['solution_found']:
                        file.write("Solução Encontrada: Sim\n")
                        file.write(f"Custo do Caminho: {result['cost']}\n")
                    else:
                        file.write("Solução Encontrada: Não\n")

                    file.write(f"Tempo de Execução (s): {result['time']:.6f}\n")
                    file.write(f"Nós Expandidos: {result['metrics']['nodes_expanded']}\n")
                    file.write(f"Uso Máximo de Memória: {result['metrics']['max_memory_usage']}\n")
                    file.write("\n")
                    
        print(f"Resultados salvos com sucesso em '{output_file}'")
    except Exception as e:
        print(f"Erro ao salvar resultados: {e}")

def main():
    """Função principal que testa todos os labirintos"""
    
    # Encontra todos os arquivos de labirinto
    maze_files = glob.glob('data/labirinto*.txt')
    maze_files.sort()  # Ordena para garantir ordem consistente
    
    if not maze_files:
        print("Nenhum arquivo de labirinto encontrado em 'data/'. Encerrando.")
        return
    
    print(f"Encontrados {len(maze_files)} arquivos de labirinto:")
    for file in maze_files:
        print(f"  - {file}")
    
    all_experiments_results = []
    total_mazes = 0
    
    # Processa cada arquivo de labirinto
    for maze_file in maze_files:
        print(f"\n--- Processando {maze_file} ---")
        
        list_of_grids = read_mazes_from_file(maze_file)
        if not list_of_grids:
            print(f"Nenhum labirinto encontrado em {maze_file}. Pulando.")
            continue
        
        print(f"{len(list_of_grids)} labirinto(s) carregado(s) de '{maze_file}'.")
        
        # Processa cada labirinto do arquivo
        for i, grid in enumerate(list_of_grids):
            maze_number = total_mazes + i + 1
            print(f"\n  -> Processando Labirinto {maze_number}...")
            
            try:
                maze_problem = Maze(grid)
                print(f"     Dimensões: {maze_problem.H}x{maze_problem.W}")
                print(f"     Start: {maze_problem.start}, Goal: {maze_problem.goal}")
            except Exception as e:
                print(f"     Erro ao criar o labirinto: {e}")
                continue

            # Armazena os resultados para o labirinto atual
            current_maze_results = []
            
            for name, search_function in ALGORITHMS_TO_RUN.items():
                print(f"     -> Executando {name}...")
             
                    "time": end_time - start_time,
                    "metrics": metrics
                }
                current_maze_results.append(result_data)
            
            all_experiments_results.append((maze_number, current_maze_results))
        
        total_mazes += len(list_of_grids)
    
    print(f"\n=== TESTE CONCLUÍDO ===")
    print(f"Total de labirintos processados: {total_mazes}")
    print(f"Total de algoritmos testados: {len(ALGORITHMS_TO_RUN)}")
    print(f"Total de experimentos: {total_mazes * len(ALGORITHMS_TO_RUN)}")
    
    # Salva os resultados
    output_file = 'data/relatorio_completo.txt'
    save_results(all_experiments_results, output_file)

if __name__ == "__main__"   start_time = time.time()
                path, metrics = search_function(maze_problem)
                end_time = time.time()
                
                result_data = {
                    "algorithm": name,
                    "solution_found": path is not None,
                    "cost": len(path) - 1 if path else "N/A",:
    main()
