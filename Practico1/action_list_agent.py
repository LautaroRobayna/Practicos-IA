from agent import Agent

class ActionListAgent(Agent):
    def __init__(self, env):
        self.env = env
        self.action_list = [{"direction": 1, "person1": 0, "person2": 1},  # A y B cruzan a la derecha
                            {"direction": 0, "person1": 0, "person2": 0},  # A regresa a la izquierda
                            {"direction": 1, "person1": 2, "person2": 3},  # C y D cruzan a la derecha
                            {"direction": 0, "person1": 1, "person2": 1},  # B regresa a la izquierda
                            {"direction": 1, "person1": 0, "person2": 1}]  # A y B cruzan a la derecha
        self.current_index = 0

    def next_action(self, obs):
        # Verificar si aún hay acciones en la lista
        if self.current_index < len(self.action_list):
            action = self.action_list[self.current_index]
            self.current_index += 1
            return action
        else:
            return None