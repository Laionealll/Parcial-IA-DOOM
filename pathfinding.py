#Laioneall Williams
#23-EISN-2-035

from collections import deque
from functools import lru_cache
import math

class PathFinding:
    """
    Clase encargada de realizar el cálculo de rutas en el mapa.
    Utiliza por defecto A*, pero conserva BFS si se requiere.
    """
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        # Movimientos posibles (vertical, horizontal y diagonales)
        self.ways = [(-1, 0), (1, 0), (0, -1), (0, 1),
                     (-1, -1), (1, -1), (1, 1), (-1, 1)]
        self.graph = {}
        self.get_graph()  # Se construye el grafo para BFS

    @lru_cache
    def get_path(self, start, goal, method='astar'):
        """
        Retorna la siguiente posición en la ruta desde 'start' hasta 'goal'.
        El parámetro method puede ser 'bfs' o 'astar'.
        """
        if method == 'bfs':
            visited = self.bfs(start, goal, self.graph)
        else:
            visited = self.astar(start, goal)

        # Si no se encontró ruta, retorna la posición actual.
        if goal not in visited:
            return start

        # Reconstruir el camino desde 'goal' hacia atrás usando el dict visited.
        path = [goal]
        step = visited[goal]
        while step and step != start:
            path.append(step)
            step = visited[step]

        # El último elemento es la siguiente posición a la que moverse.
        return path[-1]

    def bfs(self, start, goal, graph):
        """
        Implementación de BFS para encontrar el camino más corto.
        Retorna un diccionario donde cada nodo apunta a su 'padre'.
        """
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break

            for next_node in graph.get(cur_node, []):
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node)
                    visited[next_node] = cur_node

        return visited

    def astar(self, start, goal):
        """
        Implementación de A*.
        Retorna un diccionario similar a BFS, donde cada nodo apunta a su "padre" para reconstruir el camino.
        """
        open_set = set([start])
        closed_set = set()
        came_from = {start: None}

        # g_score: costo desde 'start' hasta el nodo actual.
        g_score = {start: 0}
        # f_score: g_score + heurística
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))
            if current == goal:
                # Reconstruir dict similar a BFS.
                visited = {}
                visited[current] = came_from[current]
                tmp = current
                while tmp in came_from and came_from[tmp] is not None:
                    padre = came_from[tmp]
                    visited[padre] = came_from[padre]
                    tmp = padre
                return visited

            open_set.remove(current)
            closed_set.add(current)

            for neighbor in self.get_next_nodes(current[0], current[1]):
                if neighbor in closed_set or neighbor in self.game.object_handler.npc_positions:
                    continue

                tentative_g = g_score[current] + self.dist_between(current, neighbor)
                if neighbor not in open_set:
                    open_set.add(neighbor)
                elif tentative_g >= g_score.get(neighbor, float('inf')):
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)

        return {}

    def dist_between(self, current, neighbor):
        (x1, y1), (x2, y2) = current, neighbor
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def heuristic(self, node, goal):
        (x1, y1), (x2, y2) = node, goal
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def get_next_nodes(self, x, y):
        """
        Retorna las celdas vecinas (adyacentes y diagonales) que no sean pared.
        """
        return [
            (x + dx, y + dy)
            for dx, dy in self.ways
            if (x + dx, y + dy) not in self.game.map.world_map
        ]

    def get_graph(self):
        """
        Construye el grafo de celdas transitables para BFS.
        """
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:  # espacio transitable
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)
