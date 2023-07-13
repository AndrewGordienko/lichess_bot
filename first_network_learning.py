import pickle
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
import random
import chess
import chess.pgn
from copy import deepcopy
import numpy as np

class Creating_Data():
    def __init__(self):
        self.pieces = ["P", "R", "N", "B", "Q", "K"]

    def fen_to_array(self, fen):
        numpy_board = np.zeros((8, 8))
        row = 0
        column = 0

        for char in range(len(fen)):
            number = 0
            if fen[char] == " " or row == 8:
                break
            if fen[char] == "/":
                row += 1
                column = -1

            if fen[char].isalpha():
                character = fen[char]
                adjusted = character.upper()

                number = self.pieces.index(adjusted) + 1
                if character.islower(): number += 8
            
            if fen[char].isnumeric():
                if int(fen[char]) != 8:
                    column += int(fen[char]) - 1

                    if column > 7:
                        row += 1
                        column = -1

            numpy_board[row][column] = number
            column += 1
        
        return numpy_board

class Probability_Matrix():
    def __init__(self):
        self.creating_data = Creating_Data()

    def stack_generation(self, board, player):
        # make the 8x8x6 stack thats passed in
        numpy_board = self.creating_data.fen_to_array(board.fen())
        player = np.full((8, 8), player)
        
        white_king_castling = int(board.has_kingside_castling_rights(color=chess.WHITE))
        white_king_castling = np.full((8, 8), white_king_castling)
        white_queen_castling = int(board.has_queenside_castling_rights(color=chess.WHITE))
        white_queen_castling = np.full((8, 8), white_queen_castling)
        black_king_castling = int(board.has_kingside_castling_rights(color=chess.BLACK))
        black_king_castling = np.full((8, 8), black_king_castling)
        black_queen_castling = int(board.has_queenside_castling_rights(color=chess.BLACK))
        black_queen_castling = np.full((8, 8), black_queen_castling)
        
        stack = []
        stack.extend([deepcopy(numpy_board), deepcopy(player)])
        stack.extend([deepcopy(white_king_castling), deepcopy(white_queen_castling)])
        stack.extend([deepcopy(black_king_castling), deepcopy(black_queen_castling)])
        stack = np.stack(stack)
        return stack
    
class Policy_Network(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.input_shape = 49
        self.action_space = 1
        self.hidden1 = 1024
        self.hidden2 = 8*8*76
        
        self.fc0 = nn.Conv3d(11, 1, kernel_size=(2, 2, 1), padding=0)
        self.fc1 = nn.Linear(self.input_shape, self.hidden1)
        self.fc2 = nn.Linear(self.hidden1, 2048)
        self.fc3 = nn.Linear(2048, 512)
        self.fc4 = nn.Linear(512, self.hidden2)

        self.optimizer = optim.Adam(self.parameters(), lr=0.0001)
        self.loss = nn.MSELoss()
        self.to("cpu")
    
    def forward(self, x):
        x = x.reshape(1, 11, 8, 8, 1)
        x = F.relu(self.fc0(x))
        x = x.flatten()
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)

        x = x.reshape(1, 8, 8, 76)

        return x

policy_network = Policy_Network()


with open('listfile.pkl', 'rb') as f:
    loaded_list = pickle.load(f)
random.shuffle(loaded_list)

print(len(loaded_list))
total_loss = 0
for i in range(len(loaded_list)):
    if i % 1000 == 0:
        print(i, total_loss/100)
        total_loss = 0

    input_array = loaded_list[i][0]

    if input_array.shape == (11, 8, 8):

        x = torch.Tensor(input_array)
        x = x.unsqueeze(0)

        calculated = policy_network.forward(x)
        output_array = torch.Tensor(loaded_list[i][1])
        loss = ((calculated -  output_array)**2).mean()

        loss = torch.Tensor(loss)
        loss = Variable(loss, requires_grad=True)

        policy_network.optimizer.zero_grad()
        loss.backward()
        policy_network.optimizer.step()

        total_loss += loss


board = chess.Board()
creating_data = Creating_Data()


probability_matrix = Probability_Matrix()
stack = probability_matrix.stack_generation(board, 1)

stack = np.vstack((stack, creating_data.fen_to_array(board.fen()).reshape(1, 8, 8)))
stack = np.vstack((stack, creating_data.fen_to_array(board.fen()).reshape(1, 8, 8)))
stack = np.vstack((stack, creating_data.fen_to_array(board.fen()).reshape(1, 8, 8)))
stack = np.vstack((stack, creating_data.fen_to_array(board.fen()).reshape(1, 8, 8)))
stack = np.vstack((stack, creating_data.fen_to_array(board.fen()).reshape(1, 8, 8)))

print(stack.shape)

result = policy_network.forward(torch.Tensor(stack))
print(result.shape)

# Find the index of the largest number
max_index = np.argmax(result.detach().numpy())

# Convert the 1D index to 3D index
index_3d = np.unravel_index(max_index, result.shape)

print(index_3d)
