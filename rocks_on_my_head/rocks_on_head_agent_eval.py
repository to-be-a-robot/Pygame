import os
import torch
import pygame
from rocks_on_head_agent_env import AsteroidGame
from DQN_agent import DQNAgent

N_EVAL_EPISODES = 10

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trained_model.pth")

#create a game
game = AsteroidGame(render_mode="human")

#create an agent
agent = DQNAgent(state_size=1 + 2 * game.N_TRACKED, action_size=3)

# load trained weights
agent.q_network.load_state_dict(torch.load(MODEL_PATH))
agent.q_network.eval()
agent.epsilon = 0

clock = pygame.time.Clock()

for episode in range(N_EVAL_EPISODES):
    state = game.reset()
    done = False
    while not done:
        action = agent.act(state)
        print("state:", state)
        print("q-values:", agent.q_network(torch.from_numpy(state).float().unsqueeze(0)))
        print("action:", action)
        next_state, reward, done, info = game.step(action)
        state = next_state
        game.draw()                     


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        clock.tick(30)

    print("survival time:", info["survived_frames"])