from search_agent import SearchAgent
from priority_queue import PriorityQueue


class AStarAgent(SearchAgent):

    def __init__(self, env, initial_state, end_state, model):
        super().__init__(env, initial_state, end_state, model)
        self.action_list = []
        self.heuristics = {}
        self._calculate_heuristics()

    def _calculate_heuristics(self):
        raise NotImplementedError


    def _next_action(self):
        #Usar action_list o llamar a a_star para actualizar self.action_list
        raise NotImplementedError

    def a_star(self):
        #Algoritmo de a_star que retorna la lista de acciones para llegar al destino
        raise NotImplementedError

