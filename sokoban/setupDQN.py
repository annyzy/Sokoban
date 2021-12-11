import copy
import os
import numpy as np
import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class DeepQNetwork(nn.Module):
    #暂定两层全连接
    def __init__(self,lr,input_dims,n_actions,name,chkpt_dir="saved_model/"):
        super(DeepQNetwork,self).__init__()
        self.checkpoint_dir = chkpt_dir
        self.checkpoint_file = os.path.join(self.checkpoint_dir, name)

        self.input_dims = input_dims
        self.n_actions=n_actions
        C=input_dims[0]
        D=input_dims[1]
        H=input_dims[2]
        W=input_dims[3]
        # input: C*D*H *W
        #        1*7*10*10
        self.conv3D1=nn.Conv3d(1,8,(7,7,5),padding=(3,3,2))     # ?*8C*D*H*W
        self.conv3D2=nn.Conv3d(8,16,(5,5,5),padding=2)    # ?*16C*D*H*W
        self.conv3D3=nn.Conv3d(16,16,(3,3,3),padding=1)    # ?*16C*D*H*W
        self.flatten=nn.Flatten()
        self.fc1=nn.Linear(16*D*H*W,128)
        self.fc2=nn.Linear(128,4)

        self.optimizer=optim.Adam(self.parameters(),lr=lr)
        self.loss = nn.MSELoss()
        # self.device=T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.device=T.device('cuda:0')
        self.to(self.device)

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))

    def forward(self,state):
        # print(state.size())
        # layer 1
        x=self.conv3D1(state)
        # print(x.size())
        # layer 2
        x=self.conv3D2(x)
        # print(x.size())
        # layer 3
        x=self.conv3D3(x)
        # print(x.size())
        # Flatten
        x = self.flatten(x)
        # print(x.size())
        # layer 4
        x=self.fc1(x)
        # print(x.size())
        # layer 5
        actions=self.fc2(x)
        # print(actions.size())
        # actions = T.sigmoid(actions)
        return actions

class Agent():
    def __init__(self,gamma,epsilon,lr,input_dims,batch_size,n_actions,name,chkpt_dir="saved_model/",max_mem_size=1000000,eps_end=0.15,eps_dec=5e-5):
        self.gamma=gamma
        self.epsilon=epsilon
        self.lr=lr
        self.eps_min=eps_end
        self.eps_dec=eps_dec
        self.action_space=[i for i in range(n_actions)]
        self.mem_size=max_mem_size
        self.batch_size=batch_size
        self.mem_cntr = 0
        self.Q_eval=DeepQNetwork(self.lr, n_actions=n_actions, input_dims=input_dims,name=name+"_Q_eval",chkpt_dir=chkpt_dir)
        self.Q_targ=DeepQNetwork(self.lr, n_actions=n_actions, input_dims=input_dims,name=name+"_Q_targ",chkpt_dir=chkpt_dir)
        self.state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool)

    def save_models(self):
        print('... saving checkpoint ...')
        self.Q_eval.save_checkpoint()
        self.Q_targ.save_checkpoint()

    def load_models(self):
        print('... loading checkpoint ...')
        self.Q_eval.load_checkpoint()
        self.Q_targ.load_checkpoint()

    def store_trasition(self, state, action, reward, state_,done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index]=state
        self.new_state_memory[index]=state_
        self.reward_memory[index]=reward
        self.action_memory[index]=action
        self.terminal_memory[index]=done

        self.mem_cntr += 1

    def predict(self,observation):
        if np.random.rand() > 0.1:
            state = T.tensor(observation).to(self.Q_eval.device)
            actions = self.Q_eval.forward(state)
            action = T.argmax(actions).item()
            # print("argmax :"+str(action))
        else:
            # print("random")
            action = np.random.choice(self.action_space)

        return action

    def choose_action(self,observation):
        # if True:
        if np.random.rand() > self.epsilon:
            state = T.tensor(observation).to(self.Q_eval.device)
            actions = self.Q_eval.forward(state)
            action = T.argmax(actions).item()
            # print("argmax :"+str(action))
        else:
            # print("random")
            action = np.random.choice(self.action_space)

        return action

    def learn(self,syncTargetQ):
        if self.mem_cntr < self.batch_size:
            return

        self.Q_eval.optimizer.zero_grad()

        max_mem = min(self.mem_cntr,self.mem_size)
        batch = np.random.choice(max_mem,self.batch_size,replace=False)

        batch_index=np.arange(self.batch_size, dtype=np.int32)
        state_batch=T.tensor(self.state_memory[batch]).to(self.Q_eval.device)
        new_state_batch=T.tensor(self.new_state_memory[batch]).to(self.Q_eval.device)
        reward_batch = T.tensor(self.reward_memory[batch]).to(self.Q_eval.device)
        terminal_batch=T.tensor(self.terminal_memory[batch]).to(self.Q_eval.device)

        action_batch = self.action_memory[batch]

        q_eval=self.Q_eval.forward(state_batch)[batch_index,action_batch]

        # q_next = self.Q_eval.forward(new_state_batch)
        q_next = self.Q_targ.forward(new_state_batch)  # target network
        q_next[terminal_batch]=0.0

        q_target = reward_batch+self.gamma*T.max(q_next,dim=1)[0]
        loss=self.Q_eval.loss(q_target,q_eval).to(self.Q_eval.device)
        # loss=-loss
        loss.backward()
        self.Q_eval.optimizer.step()
        # print(q_eval)
        # print("---------------------------------------")

        self.epsilon=self.epsilon-self.eps_dec if self.epsilon> self.eps_min else self.eps_min

        if (syncTargetQ):
            # print("updated target net")
            self.Q_targ.conv3D1=copy.deepcopy(self.Q_eval.conv3D1)
            self.Q_targ.conv3D2=copy.deepcopy(self.Q_eval.conv3D2)
            self.Q_targ.conv3D3=copy.deepcopy(self.Q_eval.conv3D3)
            self.Q_targ.flatten=copy.deepcopy(self.Q_eval.flatten)
            self.Q_targ.fc1=copy.deepcopy(self.Q_eval.fc1)
            self.Q_targ.fc2=copy.deepcopy(self.Q_eval.fc2)







