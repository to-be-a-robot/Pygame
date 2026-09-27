import torch
import torch.nn as nn
from collections import deque
import random
import numpy as np 

class QNetwork(nn.Module):
    """Maps a state vector to a Q-value for each possible action."""
    def __init__(self, state_size, action_size,hidden_layer = 64):
        super().__init__()
        self.input_layer = nn.Linear(state_size, hidden_layer) 
        self.output_layer = nn.Linear(hidden_layer,action_size) #One Q-value per action 


    def forward(self, state):
        hidden_activated = torch.relu(self.input_layer(state))
        q_values=self.output_layer(hidden_activated) #Q-values
        return q_values


    

class ReplayBuffer:
    """Fixed-size memory of past experiences, sampled randomly during training."""
    def __init__(self,capacity):
        self.memory = deque(maxlen= capacity)

    def push (self,state,action, reward, next_state, done):
        self.memory.append((state,action,reward,next_state,done))


    def sample(self, batch_size):
        batch= random.sample(self.memory,batch_size) #returns a list of random tuples 
        states,actions,rewards,next_states,dones = zip(*batch)
        return (
             np.array(states, dtype= np.float32),
             np.array(actions, dtype= np.float64),
             np.array(rewards, dtype= np.float32),
             np.array(next_states, dtype= np.float32),
             np.array(dones, dtype= np.float32)
        )


    def __len__(self):
        return len(self.buffer)



    


