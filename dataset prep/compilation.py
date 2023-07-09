import chess
import io
import chess.pgn
import numpy as np
from copy import deepcopy

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
    
    def fill_stack(self, stack, move, value, board):
        # fill up the array based on what the calculated values are
        # given a stack, move, and value
        
        stack = stack
        
        move_s = str(move)[0:2]
        move_e = str(move)[2:4]
        
        file_s, rank_s = int(ord(move_s[0]) - 97), int(move_s[1])-1
        file_e, rank_e = int(ord(move_e[0]) - 97), int(move_e[1])-1

        square_s = chess.parse_square(chess.square_name(chess.square(file_s, rank_s))) # converts file rank into square type
        square_e = chess.parse_square(chess.square_name(chess.square(file_e, rank_e))) # converts file rank into square type
        piece = str(board.piece_at(square_s)).lower() # piece at square location
        distance = chess.square_distance(square_s, square_e)
        
        if piece == "n":
            if rank_s - rank_e == -2: # up the board
                if file_s - file_e == 1: # left
                    stack[rank_s][file_s][56] = value
                if file_s - file_e == -1: # right
                    stack[rank_s][file_s][57] = value
            if rank_s - rank_e == 2: # down the board
                if file_s - file_e == 1: # left
                    stack[rank_s][file_s][58] = value
                if file_s - file_e == -1: # right
                    stack[rank_s][file_s][59] = value
            if file_s - file_e == -2: # right
                if rank_s - rank_e == 1:
                    stack[rank_s][file_s][60] = value
                if rank_s - rank_e == -1:
                    stack[rank_s][file_s][61] = value
            if file_s - file_e == 2: # left
                if rank_s - rank_e == 1:
                    stack[rank_s][file_s][62] = value
                if rank_s - rank_e == -1:
                    stack[rank_s][file_s][63] = value
                
        if piece == "p":
            if len(str(move)) == 5:
                if rank_s - rank_e == -1: # capture up
                    if file_s - file_e == -1: # capture left
                        if move[4] == "r": # promote to rook
                            stack[rank_s][file_s][64] = value
                        if move[4] == "b": # promote to bishop
                            stack[rank_s][file_s][65] = value
                        if move[4] == "n": # promote to knight
                            stack[rank_s][file_s][66] = value
                    if file_s - file_e == 1: # capture right
                        if move[4] == "r": # promote to rook
                            stack[rank_s][file_s][67] = value
                        if move[4] == "b": # promote to bishop
                            stack[rank_s][file_s][68] = value
                        if move[4] == "n": # promote to knight
                            stack[rank_s][file_s][69] = value
                if rank_s - rank_e == 1: # capture down
                    if file_s - file_e == -1: # capture left
                        if move[4] == "r": # promote to rook
                            stack[rank_s][file_s][70] = value
                        if move[4] == "b": # promote to bishop
                            stack[rank_s][file_s][71] = value
                        if move[4] == "n": # promote to knight
                            stack[rank_s][file_s][72] = value
                    if file_s - file_e == 1: # capture right
                        if move[4] == "r": # promote to rook
                            stack[rank_s][file_s][73] = value
                        if move[4] == "b": # promote to bishop
                            stack[rank_s][file_s][74] = value
                        if move[4] == "n": # promote to knight
                            stack[rank_s][file_s][75] = value
                    
        if rank_s > rank_e and file_s - file_e == 0: # N
            stack[rank_s][file_s][distance - 1] = value
        if rank_s > rank_e and file_s > file_e: # NE
            stack[rank_s][file_s][7 * 1 + distance - 1] = value
        if rank_s == rank_e and file_s < file_e: # E
            stack[rank_s][file_s][7 * 2 + distance - 1] = value
        if rank_s < rank_e and file_s < file_e: # SE
            stack[rank_s][file_s][7 * 3 + distance - 1] = value
        if rank_s < rank_e and file_s - file_e == 0: # S
            stack[rank_s][file_s][7 * 4 + distance - 1] = value 
        if rank_s < rank_e and file_s < file_e: # SW
            stack[rank_s][file_s][7 * 5 + distance - 1] = value 
        if rank_s == rank_e and file_s > file_e: # W
            stack[rank_s][file_s][7 * 6 + distance - 1] = value 
        if rank_s > rank_e and file_s < file_e: # NW
             stack[rank_s][file_s][7 * 7 + distance - 1] = value
        
        return stack

probability_matrix = Probability_Matrix()

text = """1. e4 e6 2. d4 d5 3. Nc3 Bb4 4. e5 Ne7 5. a3 Bxc3+ 6. bxc3 c5 7. Qg4 Qc7 8. Qxg7 Rg8 9. Qxh7 cxd4 10. Ne2 dxc3 11. f4 d4 12. h4 Nbc6 13. h5 Bd7 14. h6 O-O-O 15. Qd3 Rg6 16. h7 Rh8 17. Nxd4 Nxd4 18. Qxd4 Kb8 19. Rh3 Nf5 20. Qb4 Bc6 21. a4 Bxg2 22. Rxc3 Qb6 23. Qxb6 axb6 24. Ba3 Bxf1 25. O-O-O Bg2 26. Bd6+ Ka7 27. Rc7 Rxh7 28. Rc8 Rhg7 29. Bb8+ Ka6 30. Bc7 Rg8 31. Rdd8 Rxd8 32. Rxd8 Ka7 33. Bb8+ Ka6 34. Bc7 Ka7 35. Bb8+ Ka8 36. Bc7+ Ka7 1/2-1/2"""

split_text = text.split(" ")

clean_list = []
for item in split_text:
    if item[0].isnumeric() == False:
        clean_list.append(item)

dataset = []
board = chess.Board()
for move in clean_list:
    board_before = deepcopy(board)
    string_move = str(str(board.push_san(move)))
    dataset.append([board_before, string_move])

split_dataset = []
for i in range(0, len(dataset), 1):
    chunk = dataset[i:i + 2]
    if len(chunk) == 2:
        split_dataset.append(deepcopy(chunk))

player = 2
for couple in split_dataset:
    board = couple[0][0]
    if player == 2:
        player = 1
    else:
        player = 2

    probability_matrix.creating_data.fen_to_array(board.fen())
    stack = probability_matrix.stack_generation(board, player)
    couple[0] = stack # 8x8x6 input into network

    if player == 2:
        player = 1
    else:
        player = 2
    

    board, move_made = couple[1][0], couple[1][1]
    stack = np.zeros((8, 8, 76))
    value = 1
    if player == 2:
        value = -1
        
    stack = probability_matrix.fill_stack(stack, move_made, value, board)
    couple[1] = stack

for couple in split_dataset:
    print("")
    print(couple[0].shape, couple[1].shape)


    

    





