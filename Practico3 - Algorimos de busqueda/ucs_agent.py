from search_agent import SearchAgent
from priority_queue import PriorityQueue


class UCSAgent(SearchAgent):

    def __init__(self, env, initial_state, end_state, model):
        super().__init__(env, initial_state, end_state, model)
        self.action_list = []
        self.current_step = 0

    def _next_action(self):
        if not self.action_list:
            self.action_list = self.shortest_path(self.end_state)
            self.current_step = 0
        
        if self.current_step < len(self.action_list):
            action = self.action_list[self.current_step]
            self.current_step += 1
            return action
        else:
            raise Exception("No hay más acciones disponibles")

    def ucs(self):
        pq = PriorityQueue()
        pq.push(self.initial_state, 0, None)
        
        visited = set()
        predecessors = {}
        
        while not pq.is_empty():
            current_data, current_cost, prev = pq.pop()
            
            if current_data in visited:
                continue
            visited.add(current_data)
            
            predecessors[current_data] = prev
            
            if current_data == self.end_state:
                break
                
            for action, neighbor in self.model.graph[current_data].items():
                if neighbor not in visited and neighbor not in pq:
                    new_cost = current_cost + 1
                    pq.push(neighbor, new_cost, current_data)
        
        return predecessors
    
    def shortest_path(self, target):
        predecessors = self.ucs()
        
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