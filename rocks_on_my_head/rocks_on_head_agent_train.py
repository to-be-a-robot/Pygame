import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from rocks_on_head_agent_env import AsteroidGame
from DQN_agent import DQNAgent

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

#create game
game = AsteroidGame()

#create agent
# state = [ship_x_norm] + 2 values (dx, dy) per tracked asteroid
agent = DQNAgent(state_size=1 + 2 * game.N_TRACKED, action_size=3)

NUM_EPISODES= 1600
TARGET_UPDATE_FREQ = 10

episode_rewards = []
episode_survival = []

for episode in range(NUM_EPISODES):
       state = game.reset()
       total_reward = 0
       done = False

       while not done:
           action = agent.act(state)
           next_state, reward, done, info = game.step(action)
           agent.remember(state, action, reward, next_state, done)
           agent.learn()

           state = next_state
           total_reward += reward

       episode_rewards.append(total_reward)
       episode_survival.append(info["survived_frames"])
       agent.decay_epsilon() 

       if episode % TARGET_UPDATE_FREQ == 0:
           agent.update_target_network()

       print(f"Episode {episode}: reward={total_reward}, survived={info['survived_frames']}, epsilon={agent.epsilon:.3f}")


# save trained weights
torch.save(agent.q_network.state_dict(), os.path.join(SCRIPT_DIR, "trained_model.pth"))


RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

plt.figure()
plt.plot(episode_survival)
plt.xlabel("Episode")
plt.ylabel("Survival (frames)")
plt.title("DQN Training Progress")
plt.savefig(os.path.join(RESULTS_DIR, "learning_curve.png"))
plt.show()

window = 30
rolling_avg = np.convolve(episode_survival, np.ones(window)/window, mode='valid')

plt.figure()  # ← new, separate figure
plt.plot(rolling_avg)
plt.xlabel("Episode")
plt.ylabel("Survival (rolling avg, frames)")
plt.title("DQN Training Progress (smoothed)")
plt.savefig(os.path.join(RESULTS_DIR, "learning_curve_smoothed.png"))
plt.show()