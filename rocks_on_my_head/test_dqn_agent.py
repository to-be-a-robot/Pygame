import torch
import numpy as np
from DQN_agent import QNetwork, ReplayBuffer


state_size = 11
action_size = 3

network = QNetwork(state_size, action_size)

dummy_state= torch.rand(state_size)
output = network(dummy_state)

print("QNetwork Output:", output)
print("QNetwork Output shape", output.shape)

buffer = ReplayBuffer(capacity= 100)

for i in range(10):
    state= np.random.rand(state_size)
    next_state = np.random.rand(state_size)
    buffer.push(state,action=1,reward=1.0, next_state=next_state, done=False)

print("Buffer Length :", len(buffer))
states, actions, rewards, next_states, dones = buffer.sample(batch_size=4)

print("states shape:", states.shape)         
print("actions shape:", actions.shape)       
print("rewards shape:", rewards.shape)      
print("next_states shape:", next_states.shape)  
print("dones shape:", dones.shape)           
