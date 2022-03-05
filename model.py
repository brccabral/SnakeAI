import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
from settings import OUTPUT_SIZE


class Linear_QNet(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, output_size)
        self.drop = nn.Dropout(p=0.3)

    def forward(self, x: torch.Tensor):
        x = F.relu(self.drop(self.linear1(x)))
        x = F.relu(self.drop(self.linear2(x)))
        x = self.drop(self.linear3(x))
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        os.makedirs(model_folder_path, exist_ok=True)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

    def load(self, file_name='model.pth'):
        model_folder_path = './model'
        file_name = os.path.join(model_folder_path, file_name)
        self.load_state_dict(torch.load(file_name))


class QTrainer:
    def __init__(self, lr: float, gamma: float, input_size: int, hidden_size: int):
        self.lr = lr
        self.gamma = gamma
        self.input_size = input_size
        self.hidden_size = hidden_size

        self.model: Linear_QNet = Linear_QNet(
            self.input_size, self.hidden_size, OUTPUT_SIZE)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        self.loss: torch.Tensor = None

    def train_step(self, state_old, action, reward, state_new, done):

        if len(state_old.shape) == 1:
            # received only one state
            # need to change to shape (1, x)
            # appends one dimension at beginning of each tensor
            state_old = torch.unsqueeze(state_old, 0)
            state_new = torch.unsqueeze(state_new, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            # tuple with one dimension
            done = (done, )

        # 1: predict Q values with current state
        pred_action: torch.Tensor = self.model(state_old)  # list

        # 2: Q_new = r + y * max(next_predicted_Q_value) -> only do this if not done
        target = pred_action.clone()
        for index in range(len(done)):
            Q_new = reward[index]
            if not done[index]:
                Q_new = reward[index] + self.gamma * \
                    torch.max(self.model(state_new))

            target[index][torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()
        self.loss: torch.Tensor = self.criterion(target, pred_action)
        self.loss.backward()
        self.optimizer.step()

    def copy(self):
        new_copy = QTrainer(lr=self.lr, gamma=self.gamma,
                            input_size=self.input_size, hidden_size=self.hidden_size)
        new_copy.model.load_state_dict(self.model.state_dict())
        new_copy.optimizer.load_state_dict(self.optimizer.state_dict())
        new_copy.criterion.load_state_dict(self.criterion.state_dict())
        new_copy.loss = self.loss.clone()

        return new_copy

    def __repr__(self):
        return f'QTrainer(l1:{self.model.linear1.weight.data} l2:{self.model.linear2.weight.data})'
