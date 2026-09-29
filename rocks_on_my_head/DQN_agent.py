import torch
import torch.nn as nn
import torch.optim as optim
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
        return len(self.memory)




class DQNAgent:

    def __init__(self,
                state_size, 
                action_size, 
                hidden_layers = 64,
                lr=1e-3,gamma=0.99,
                buffer_capacity=10000,
                batch_size=64,
                epsilon_start=1.0,
                epsilon_decay= 0.995,
                epsilon_min=0.01):
        self.state_size= state_size
        self.action_size= action_size
        self.gamma= gamma
        self.batch_size= batch_size

        # Original Network
        self.q_network = QNetwork(state_size, action_size, hidden_layers)

        # Target Network 
        self.target_Network = QNetwork(state_size, action_size, hidden_layers) # similar to the original q-network

        #Copying the weights and bias on to the target Network from the original Network 
        self.target_Network.load_state_dict(self.q_network.state_dict())

        #optimizer - adjusts the network's weights during training
        self.optimizer = optim.Adam(self.q_network.parameters(),lr=lr) 

        #exploration (epsilon-greedy)
        self.epsilon = epsilon_start 
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        #memory 
        self.buffer= ReplayBuffer(buffer_capacity)

    def act(self, state):
        rand_num = np.random.rand()
        if rand_num < self.epsilon:
            return np.random.randint(self.action_size)
        else:
            state_tensor = torch.from_numpy(state).float().unsqueeze(0)
            with torch.no_grad():
                q_values= self.q_network(state_tensor)
            return torch.argmax(q_values, dim=1).item()

    def remember(self,state,action,reward,next_state,done):
        self.buffer.push(state,action,reward,next_state,done)

    #learn 
    def learn(self):
        if len(self.buffer) < self.batch_size:
            return 
        
        # Sample a batch from the buffer
        states,actions,rewards, next_states, dones = self.buffer.sample(self.batch_size)

        # Convert all to torch tensors
        states_tensor = torch.from_numpy(states)
        actions_tensor = torch.from_numpy(actions).long()
        rewards_tensor = torch.from_numpy(rewards)
        next_states_tensor= torch.from_numpy(next_states)
        dones_tensor = torch.from_numpy(dones)

        #CURRENT Q-values
        q_all= self.q_network(states_tensor)
        q_current = q_all.gather(1,actions_tensor.unsqueeze(1)).squeeze(1)

        #target Q-values (Double DQN: online network picks the action, target network
        #evaluates it - decouples selection from evaluation to reduce the overestimation
        #bias plain DQN gets from always taking max over the target network's own noisy
        #estimates)
        with torch.no_grad():
            next_actions = self.q_network(next_states_tensor).argmax(dim=1)
            q_next_all = self.target_Network(next_states_tensor)
            q_next = q_next_all.gather(1, next_actions.unsqueeze(1)).squeeze(1)
            q_target=rewards_tensor + self.gamma * q_next * (1 - dones_tensor)


        loss = nn.MSELoss()(q_current,q_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def decay_epsilon(self):
         self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def update_target_network(self):
        self.target_Network.load_state_dict(self.q_network.state_dict())





            



    


