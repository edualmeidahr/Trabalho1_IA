import time 
from datetime import datetime
from typing import List


from src.search import a_star_search, dfs
from src.maze import Maze, Grid


ALGORITHMS_TO_RUN = {
    "Depth-First Search (DFS)": dfs,
    "A* Search (A-Star)": a_star_search,
    # Adicione  buscas aqui quando estiverem prontas
    # "Breadth-First Search (BFS)": bfs,
    # "Greedy Best-First Search": greedy_search,
}

def read_mazes_from_file(input_file: str) -> List[Grid]:


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
            
            
            if current_maze:
                mazes.append(current_maze)
        return mazes
    except FileNotFoundError:
        print(f"Erro: O arquivo de entrada '{input_file}' não foi encontrado.")
        return []

def save_results(input_file, all_experiments_data, output_file):
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("="*60 + "\n")
            file.write("        RELATÓRIO DE DESEMPENHO DOS ALGORITMOS DE BUSCA\n")
            file.write("=" * 60 + "\n\n")
            file.write(f"Arquivo de Entrada: {input_file}\n")
            file.write(f"Data da Execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

            # Itera sobre os resultados de cada mapa
            for maze_number, results_for_maze in all_experiments_data:
                file.write("\n" + "="*20 + f" ANÁLISE DO MAPA {maze_number} " + "="*20 + "\n\n")

                for result in results_for_maze: 
                    file.write('-'*40 + "\n")
                    file.write(f"Algoritmo: {result['algorithm']}\n")
                    file.write("-"*40 + "\n")

                    
                    if result['solution_found']:
                        file.write("Solução Encontrada: Sim\n")
                        file.write(f"Custo do Caminho: {result['cost']}\n")
                    else:
                        file.write("Solução Encontrada: Não\n")

                    file.write(f"Tempo de Execução (s): {result['time']:.6f}\n")

                    for key, value in result['metrics'].items():
                        readable_key = key.replace('_', ' ').capitalize()
                        file.write(f"{readable_key}: {value}\n")
                    file.write("\n")
        print(f"Resultados salvos com sucesso em '{output_file}'")
    except Exception as e:
        print(f"Erro ao salvar resultados: {e}")


def main():
    
    input_file = 'data/labirinto.txt'
    output_file = 'data/relatorio_resultados.txt'

    
    list_of_grids = read_mazes_from_file(input_file)
    if not list_of_grids:
        print("Nenhum labirinto encontrado no arquivo. Encerrando.")
        return
    
    print(f"{len(list_of_grids)} labirintos carregados com sucesso de '{input_file}'.")

    
    all_experiments_results = []
    
    
    for i, grid in enumerate(list_of_grids):
        maze_number = i + 1
        print(f"\n--- Processando Mapa {maze_number} ---")
        
        try:
            maze_problem = Maze(grid)
        except Exception as e:
            print(f"Erro ao criar o labirinto para o Mapa {maze_number}: {e}")
            continue # Pula para o próximo labirinto

        # Armazena os resultados apenas para o labirinto atual
        current_maze_results = []
        
        for name, search_function in ALGORITHMS_TO_RUN.items():
            print(f"  -> Executando {name}...")
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
        
        
        all_experiments_results.append((maze_number, current_maze_results))

   
    save_results(input_file, all_experiments_results, output_file)

if __name__ == "__main__":
    main()