class SearchAgent:
    def __init__(self, env, initial_state, end_state, model):
        self.env = env
        self.initial_state = initial_state
        self.end_state = end_state
        self.model = model

    def run(self):
        return self._loop()

    def _loop(self):
        obs = self.env.reset()
        
        # Solo actualizar si initial_state/end_state son None (se pasan como placeholder)
        if self.initial_state is None or self.end_state is None or self.model is None:
            from main import find_start_and_goal  # Import aquí para evitar circular
            from model import Model
            
            start_state, goal_state = find_start_and_goal(self.env)
            self.initial_state = start_state
            self.end_state = goal_state
            self.model = Model(self.env.unwrapped.desc)
        
        done = False
        step_counter = 0
        self.env.render()

        while not done:
            action = self._next_action()
            self._check_action(action)
            obs, reward, done, _, _ = self.env.step(action)
            step_counter += 1
            self.env.render()

        return reward, step_counter

    def _next_action(self):
        return int(input())

    def _check_action(self, action):
        if not (self.env.action_space.contains(action)):
            raise Exception("Action not in action space")