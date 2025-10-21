#Implementação das buscas (BFS,DFS,A*, Gulosa pelo menor custo)

import heapq
from typing import Dict , List, Tuple, Optional

from src.maze import Maze, Pos
from src.heuristics import manhattan_distance, euclidean_distance


# Função para reconstruir o caminho do início ao objetivo
def reconstruct_path(came_from: Dict[Pos, Optional[Pos]], start: Pos, goal: Pos):
    
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path



def a_star_search(maze: Maze ):

    start_node = maze.start
    goal_node = maze.goal


    nodes_expanded = 0
    max_memory_usage = 0


    frontier = []



    f_start = manhattan_distance(start_node, goal_node)
    heapq.heappush(frontier, (f_start, start_node))



    came_from: Dict[Pos, Pos] = {start_node: None}


    g_cost: Dict[Pos, int] = {start_node: 0}

    while frontier:

        current_memory = len(frontier) + len(g_cost)
        if current_memory > max_memory_usage:
            max_memory_usage = current_memory

        
        _, current_node = heapq.heappop(frontier)
        nodes_expanded += 1


        if maze.goal_test(current_node):
            path = reconstruct_path(came_from, start_node, goal_node)
            metrics = {
                "nodes_expanded": nodes_expanded,
                "max_memory_usage": max_memory_usage
            }
            return path, metrics
        
        for action in maze.actions(current_node):

            neighbor_node = maze.result(current_node, action)

            # Custo do caminho até o nó vizinho
            step_cost = maze.step_cost(current_node, action, neighbor_node)
            g_cost_tentative = g_cost[current_node] + step_cost
            
            # Se o nó vizinho não foi visitado ou se encontramos um caminho mais barato
            if neighbor_node not in g_cost or g_cost_tentative < g_cost[neighbor_node]:

                came_from[neighbor_node] = current_node
                g_cost[neighbor_node] = g_cost_tentative

                f_cost = g_cost_tentative + manhattan_distance(neighbor_node, goal_node)
                heapq.heappush(frontier, (f_cost, neighbor_node))
        
    metrics = {
        "nodes_expanded": nodes_expanded,
        "max_memory_usage": max_memory_usage
    }

    return None, metrics



def dfs( maze: Maze):

    start_node = maze.start
    goal_node = maze.goal

    nodes_expanded = 0
    max_memory_usage = 0

    frontier: List[Pos] = [start_node]

    came_from: Dict[Pos, Optional[Pos]] = {start_node: None}

    while frontier:

        current_memory = len(frontier) + len(came_from)
        
        if current_memory > max_memory_usage:
            max_memory_usage = current_memory

        current_node = frontier.pop()
        nodes_expanded += 1

        if maze.goal_test(current_node):
            path = reconstruct_path(came_from, start_node, goal_node)
            metrics = {
                "nodes_expanded": nodes_expanded,
                "max_memory_usage": max_memory_usage
            }
            return path, metrics
        
        for action in maze.actions(current_node):
            neighbor_node = maze.result(current_node, action)

            if neighbor_node not in came_from:
                came_from[neighbor_node] = current_node
                frontier.append(neighbor_node)
        
    metrics = {
        "nodes_expanded": nodes_expanded,
        "max_memory_usage": max_memory_usage
    }  

    return None, metrics


def bfs(maze: Maze):
    """
    Breadth-First Search - Busca em largura
    Explora todos os nós em um nível antes de passar para o próximo nível.
    Garante encontrar o caminho mais curto em termos de número de passos.
    """
    start_node = maze.start
    goal_node = maze.goal

    nodes_expanded = 0
    max_memory_usage = 0

    # BFS usa uma fila (FIFO) ao invés de pilha
    frontier = [start_node]  # Lista que será tratada como fila
    came_from: Dict[Pos, Optional[Pos]] = {start_node: None}

    while frontier:
        current_memory = len(frontier) + len(came_from)
        if current_memory > max_memory_usage:
            max_memory_usage = current_memory

        # Remove o primeiro elemento (FIFO)
        current_node = frontier.pop(0)
        nodes_expanded += 1

        if maze.goal_test(current_node):
            path = reconstruct_path(came_from, start_node, goal_node)
            metrics = {
                "nodes_expanded": nodes_expanded,
                "max_memory_usage": max_memory_usage
            }
            return path, metrics
        
        for action in maze.actions(current_node):
            neighbor_node = maze.result(current_node, action)

            if neighbor_node not in came_from:
                came_from[neighbor_node] = current_node
                frontier.append(neighbor_node)  # Adiciona no final da fila
        
    metrics = {
        "nodes_expanded": nodes_expanded,
        "max_memory_usage": max_memory_usage
    }

    return None, metrics


def greedy_search(maze: Maze):
    """
    Greedy Best-First Search - Busca gulosa
    Usa apenas a heurística h(n) para escolher o próximo nó a expandir.
    Não considera o custo acumulado, apenas a distância estimada até o objetivo.
    """
    start_node = maze.start
    goal_node = maze.goal

    nodes_expanded = 0
    max_memory_usage = 0

    # Usa heap para manter nós ordenados por heurística
    frontier = []
    h_start = manhattan_distance(start_node, goal_node)
    heapq.heappush(frontier, (h_start, start_node))


    came_from: Dict[Pos, Optional[Pos]] = {start_node: None}

    while frontier:
        current_memory = len(frontier) + len(came_from)
        if current_memory > max_memory_usage:
            max_memory_usage = current_memory

        _, current_node = heapq.heappop(frontier)
        nodes_expanded += 1

        if maze.goal_test(current_node):
            path = reconstruct_path(came_from, start_node, goal_node)
            metrics = {
                "nodes_expanded": nodes_expanded,
                "max_memory_usage": max_memory_usage
            }
            return path, metrics
        
        for action in maze.actions(current_node):
            neighbor_node = maze.result(current_node, action)

            if neighbor_node not in came_from:
                came_from[neighbor_node] = current_node
                # Usa apenas a heurística h(n), sem custo acumulado
                h_cost = manhattan_distance(neighbor_node, goal_node)
                heapq.heappush(frontier, (h_cost, neighbor_node))
        
    metrics = {
        "nodes_expanded": nodes_expanded,
        "max_memory_usage": max_memory_usage
    }

    return None, metrics


# Versões com heurística euclidiana para comparação
def a_star_search_euclidean(maze: Maze):
    """A* Search usando heurística euclidiana"""
    start_node = maze.start
    goal_node = maze.goal
    nodes_expanded = 0
    max_memory_usage = 0
    frontier = []
    f_start = euclidean_distance(start_node, goal_node)
    heapq.heappush(frontier, (f_start, start_node))
    came_from: Dict[Pos, Pos] = {start_node: None}
    g_cost: Dict[Pos, int] = {start_node: 0}

    while frontier:
        current_memory = len(frontier) + len(g_cost)
        if current_memory > max_memory_usage:
            max_memory_usage = current_memory
        _, current_node = heapq.heappop(frontier)
        nodes_expanded += 1

        if maze.goal_test(current_node):
            path = reconstruct_path(came_from, start_node, goal_node)
            metrics = {
                "nodes_expanded": nodes_expanded,
                "max_memory_usage": max_memory_usage
            }
            return path, metrics
        
        for action in maze.actions(current_node):
            neighbor_node = maze.result(current_node, action)
            step_cost = maze.step_cost(current_node, action, neighbor_node)
            g_cost_tentative = g_cost[current_node] + step_cost
            
            if neighbor_node not in g_cost or g_cost_tentative < g_cost[neighbor_node]:
                came_from[neighbor_node] = current_node
                g_cost[neighbor_node] = g_cost_tentative
                f_cost = g_cost_tentative + euclidean_distance(neighbor_node, goal_node)
                heapq.heappush(frontier, (f_cost, neighbor_node))
        
    metrics = {
        "nodes_expanded": nodes_expanded,
        "max_memory_usage": max_memory_usage
    }
    return None, metrics


def greedy_search_euclidean(maze: Maze):
    """Greedy Search usando heurística euclidiana"""
    start_node = maze.start
    goal_node = maze.goal
    nodes_expanded = 0
    max_memory_usage = 0
    frontier = []
    h_start = euclidean_distance(start_node, goal_node)
    heapq.heappush(frontier, (h_start, start_node))
    came_from: Dict[Pos, Optional[Pos]] = {start_node: None}

    while frontier:
        current_memory = len(frontier) + len(came_from)
        if current_memory > max_memory_usage:
            max_memory_usage = current_memory
        _, current_node = heapq.heappop(frontier)
        nodes_expanded += 1

        if maze.goal_test(current_node):
            path = reconstruct_path(came_from, start_node, goal_node)
            metrics = {
                "nodes_expanded": nodes_expanded,
                "max_memory_usage": max_memory_usage
            }
            return path, metrics
        
        for action in maze.actions(current_node):
            neighbor_node = maze.result(current_node, action)
            if neighbor_node not in came_from:
                came_from[neighbor_node] = current_node
                h_cost = euclidean_distance(neighbor_node, goal_node)
                heapq.heappush(frontier, (h_cost, neighbor_node))
        
    metrics = {
        "nodes_expanded": nodes_expanded,
        "max_memory_usage": max_memory_usage
    }
    return None, metrics

