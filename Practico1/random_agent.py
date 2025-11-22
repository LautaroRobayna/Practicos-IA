from agent import Agent

class RandomAgent(Agent):
    def __init__(self, env):
        self.env = env

    def next_action(self, obs):
        return self.env.action_space.sample()