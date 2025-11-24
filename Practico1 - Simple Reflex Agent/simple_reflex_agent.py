from agent import Agent

class SimpleReflexAgent(Agent):
    def __init__(self, env):
        self.env = env

    def next_action(self, obs):
        # Estado inicial: todos en la izquierda
        if obs["Aside"] == 0 and obs["Bside"] == 0 and obs["Cside"] == 0 and obs["Dside"] == 0:
            return {"direction": 1, "person1": 0, "person2": 1}  # Paso 1: A y B cruzan a la derecha (2 min)

        # A y B en la derecha, C y D en la izquierda
        elif obs["Aside"] == 1 and obs["Bside"] == 1 and obs["Cside"] == 0 and obs["Dside"] == 0:
            return {"direction": 0, "person1": 0, "person2": 0}  # Paso 2: A regresa a la izquierda (1 min)

        # A, C, D en la izquierda, B en la derecha
        elif obs["Aside"] == 0 and obs["Bside"] == 1 and obs["Cside"] == 0 and obs["Dside"] == 0:
            return {"direction": 1, "person1": 2, "person2": 3}  # Paso 3: C y D cruzan a la derecha (8 min)

        # A en la izquierda, B, C, D en la derecha
        elif obs["Aside"] == 0 and obs["Bside"] == 1 and obs["Cside"] == 1 and obs["Dside"] == 1:
            return {"direction": 0, "person1": 1, "person2": 1}  # Paso 4: B regresa a la izquierda (2 min)

        # A y B en la izquierda, C y D en la derecha
        elif obs["Aside"] == 0 and obs["Bside"] == 0 and obs["Cside"] == 1 and obs["Dside"] == 1:
            return {"direction": 1, "person1": 0, "person2": 1}  # Paso 5: A y B cruzan a la derecha (2 min)

        # Si llegamos a un estado no esperado, no hacemos nada
        else:
            return None