#!/usr/bin/env python3
"""
Script para testar todos os algoritmos de busca em múltiplos labirintos
"""

import time
from datetime import datetime
from typing import List
import os
import glob
import matplotlib.pyplot as plt

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
                stripped_line = line.rstrip('\n')
                if not stripped_line:
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


def generate_and_save_graphs(results_for_maze: List[dict], maze_number: int, output_dir: str):
    """
    Gera e salva gráficos de barras comparativos para um único labirinto.
    """
    algorithms = [r['algorithm'] for r in results_for_maze]
    times = [r['time'] for r in results_for_maze]
    costs = [r['cost'] if isinstance(r['cost'], (int, float)) else 0 for r in results_for_maze]
    nodes = [r['metrics']['nodes_expanded'] for r in results_for_maze]
    memory = [r['metrics']['max_memory_usage'] for r in results_for_maze]

    # Função auxiliar interna para criar um gráfico de barras
    def create_bar_chart(data, title, ylabel, filename):
        try:
            plt.figure(figsize=(10, 6))  # Define o tamanho da imagem
            bars = plt.bar(algorithms, data, color=['blue', 'green', 'red', 'purple'])

            # Adiciona os valores numéricos no topo de cada barra
            plt.bar_label(bars, fmt='%.6f' if min(data) > 0 and min(data) < 0.01 else '%.2f')

            plt.title(title, fontsize=16)
            plt.ylabel(ylabel, fontsize=12)
            plt.xticks(rotation=10)  # Rotaciona levemente os nomes dos algoritmos
            plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adiciona um grid suave
            plt.tight_layout()  # Ajusta o layout para não cortar os rótulos

            full_path = os.path.join(output_dir, filename)
            plt.savefig(full_path)  # Salva o gráfico como um arquivo PNG
            plt.close()  # Fecha a figura para liberar memória
        except Exception as e:
            print(f"Erro ao gerar gráfico {filename}: {e}")

    # Gráfico de Tempo de Execução
    create_bar_chart(times,
                     f'Mapa {maze_number}: Comparativo de Tempo de Execução',
                     'Tempo (segundos)',
                     f'mapa_{maze_number}_01_tempo.png')

    # Gráfico de Custo do Caminho
    create_bar_chart(costs,
                     f'Mapa {maze_number}: Comparativo de Custo do Caminho',
                     'Custo (Nº de Passos)',
                     f'mapa_{maze_number}_02_custo.png')

    # Gráfico de Nós Expandidos
    create_bar_chart(nodes,
                     f'Mapa {maze_number}: Comparativo de Nós Expandidos',
                     'Nós Expandidos',
                     f'mapa_{maze_number}_03_nos.png')

    # Gráfico de Uso de Memória
    create_bar_chart(memory,
                     f'Mapa {maze_number}: Comparativo de Uso de Memória',
                     'Uso Máximo de Memória (Nós)',
                     f'mapa_{maze_number}_04_memoria.png')


def save_results(all_experiments_data, output_file):
    """Salva os resultados em um arquivo de relatório"""
    try:
        output_dir = os.path.dirname(output_file)  # Pega o diretório do arquivo de saída

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("=" * 80 + "\n")
            file.write("        RELATÓRIO COMPARATIVO DOS ALGORITMOS DE BUSCA\n")
            file.write("=" * 80 + "\n\n")
            file.write(f"Data da Execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

            total_mazes_tested = len(all_experiments_data)
            file.write(f"Total de Labirintos Testados: {total_mazes_tested}\n\n")

            # Resumo geral
            file.write("=" * 34 + " RESUMO GERAL " + "=" * 34 + "\n\n")

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

            # Itera uma vez para coletar estatísticas
            for maze_number, source_file,results_for_maze in all_experiments_data:
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

            file.write("\n" + "=" * 80 + "\n\n")

            # Detalhes por labirinto
            for maze_number, source_file, results_for_maze in all_experiments_data:
                file.write("=" * 20 + f" ANÁLISE DO LABIRINTO {maze_number} " + "=" * 20 + "\n\n")
                file.write(f"Gráficos de resultados salvos em: {output_dir}/mapa_{maze_number}_*.png\n\n")
                file.write(f"Arquivo de origem: {os.path.basename(source_file)}\n\n")

                for result in results_for_maze:
                    file.write('-' * 50 + "\n")
                    file.write(f"Algoritmo: {result['algorithm']}\n")
                    file.write("-" * 50 + "\n")

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

    # Define os caminhos de entrada e saída
    output_dir = 'data'
    
    # Garante que o diretório de saída exista
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Diretório '{output_dir}' criado.")

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
                start_time = time.time()
                path, metrics = search_function(maze_problem)
                end_time = time.time()

                result_data = {
                    "algorithm": name,
                    "solution_found": path is not None,
                    "cost": len(path) - 1 if path else "N/A",
                    "time": end_time - start_time,
                    "metrics": metrics
                }
                current_maze_results.append(result_data)

            all_experiments_results.append((maze_number, maze_file, current_maze_results))

            # --- NOVA CHAMADA PARA GERAR GRÁFICOS ---
            print(f"  -> Gerando gráficos para o Mapa {maze_number}...")
            generate_and_save_graphs(current_maze_results, maze_number, output_dir)
        
        total_mazes += len(list_of_grids)

    print(f"\n=== TESTE CONCLUÍDO ===")
    print(f"Total de labirintos processados: {total_mazes}")
    print(f"Total de algoritmos testados: {len(ALGORITHMS_TO_RUN)}")
    print(f"Total de experimentos: {total_mazes * len(ALGORITHMS_TO_RUN)}")

    # Salva os resultados
    output_file = os.path.join(output_dir, 'relatorio_completo.txt')
    save_results(all_experiments_results, output_file)


if __name__ == "__main__":
    main()