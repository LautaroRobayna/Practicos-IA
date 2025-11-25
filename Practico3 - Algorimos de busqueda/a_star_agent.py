from search_agent import SearchAgent
from priority_queue import PriorityQueue


class AStarAgent(SearchAgent):

    def __init__(self, env, initial_state, end_state, model):
        super().__init__(env, initial_state, end_state, model)
        self.action_list = []
        self.heuristics = {}
        self.current_step = 0
        self.heuristics_calculated = False

    def _calculate_heuristics(self):
        ncols = self.model.map.shape[1]

        # Convertir el estado objetivo a coordenadas (fila, columna)
        goal_row = self.end_state // ncols
        goal_col = self.end_state % ncols

        # Calcular la heurística para cada estado posible
        for state in self.model.graph.keys():
            # Convertir el estado actual a coordenadas
            state_row = state // ncols
            state_col = state % ncols

            # Distancia Manhattan: |x1 - x2| + |y1 - y2|
            manhattan_distance = abs(state_row - goal_row) + abs(state_col - goal_col)
            self.heuristics[state] = manhattan_distance

    def _next_action(self):
        # Calcular heurísticas la primera vez (cuando el model ya está inicializado)
        if not self.heuristics_calculated:
            self._calculate_heuristics()
            self.heuristics_calculated = True

        # Si la lista de acciones está vacía, calcular el camino usando A*
        if not self.action_list:
            self.action_list = self.shortest_path(self.end_state)
            self.current_step = 0

        # Retornar la siguiente acción y avanzar el contador
        if self.current_step < len(self.action_list):
            action = self.action_list[self.current_step]
            self.current_step += 1
            return action
        else:
            raise Exception("No hay más acciones disponibles")

    def a_star(self):
        pq = PriorityQueue()
        # Push: (estado, costo_f, predecesor)
        # costo_f = g(n) + h(n)
        # Para el estado inicial: g(0) = 0, entonces f(0) = 0 + h(inicial)
        pq.push(self.initial_state, self.heuristics[self.initial_state], None)

        visited = set()
        predecessors = {}
        g_costs = {self.initial_state: 0}  # Costo real acumulado desde el inicio

        while not pq.is_empty():
            current_state, _, prev = pq.pop()  # current_f no se usa, solo desempaquetamos

            # Si ya visitamos este estado, lo ignoramos
            if current_state in visited:
                continue
            visited.add(current_state)

            # Guardamos el predecesor para reconstruir el camino
            predecessors[current_state] = prev

            # Si llegamos al objetivo, terminamos
            if current_state == self.end_state:
                break

            # Explorar vecinos
            for _, neighbor in self.model.graph[current_state].items():
                if neighbor not in visited:
                    # g(n) = costo acumulado hasta current_state + 1 (costo de moverse)
                    new_g_cost = g_costs[current_state] + 1

                    # Si encontramos un camino mejor o es la primera vez que vemos este vecino
                    if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                        g_costs[neighbor] = new_g_cost
                        # f(n) = g(n) + h(n)
                        f_cost = new_g_cost + self.heuristics[neighbor]

                        # Si el vecino ya está en la cola, actualizarlo
                        if neighbor in pq:
                            pq.update(neighbor, f_cost, current_state)
                        else:
                            pq.push(neighbor, f_cost, current_state)

        return predecessors

    def shortest_path(self, target):
        predecessors = self.a_star()

        # Obtener el camino de estados
        state_path = []
        current_node = target

        while current_node is not None:
            state_path.append(current_node)
            current_node = predecessors.get(current_node)

        state_path.reverse()

        # Convertir estados a acciones
        action_path = self.get_actions_from_path(state_path)
        return action_path

    def get_actions_from_path(self, path):
        actions = []
        for i in range(len(path) - 1):
            current_state = path[i]
            next_state = path[i + 1]

            # Buscar qué acción lleva de current_state a next_state
            for action, neighbor in self.model.graph[current_state].items():
                if neighbor == next_state:
                    actions.append(action)
                    break
        return actions
