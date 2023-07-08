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

    def fen_to_color(self, fen):
        for char in range(len(fen)):
            if fen[char] == " ":
                if fen[char+1] == "w":
                    return 0
                if fen[char+1] == "b":
                    return 1

    def fen_to_movenumber(self, fen):
        counter = 0
        for char in range(len(fen)):
            if fen[char] == " ":
                counter += 1
            
            if counter == 5:
                return int(fen[char:len(fen)])
            
creating_data = Creating_Data()

text = """1. e4 e6 2. d4 d5 3. Nc3 Bb4 4. e5 Ne7 5. a3 Bxc3+ 6. bxc3 c5 7. Qg4 Qc7 8. Qxg7 Rg8 9. Qxh7 cxd4 10. Ne2 dxc3 11. f4 d4 12. h4 Nbc6 13. h5 Bd7 14. h6 O-O-O 15. Qd3 Rg6 16. h7 Rh8 17. Nxd4 Nxd4 18. Qxd4 Kb8 19. Rh3 Nf5 20. Qb4 Bc6 21. a4 Bxg2 22. Rxc3 Qb6 23. Qxb6 axb6 24. Ba3 Bxf1 25. O-O-O Bg2 26. Bd6+ Ka7 27. Rc7 Rxh7 28. Rc8 Rhg7 29. Bb8+ Ka6 30. Bc7 Rg8 31. Rdd8 Rxd8 32. Rxd8 Ka7 33. Bb8+ Ka6 34. Bc7 Ka7 35. Bb8+ Ka8 36. Bc7+ Ka7 1/2-1/2"""

split_text = text.split(" ")

clean_list = []
for item in split_text:
    if item[0].isnumeric() == False:
        clean_list.append(item)

dataset = []
board = chess.Board()
move_number = 0
for move in clean_list:
    board.push_san(move)

    numpy_board = creating_data.fen_to_array(board.fen())

    move_board = np.ones((8, 8))
    if move_number % 2 == 0:
        move_board = np.zeros((8, 8))

    white_king_castling = int(board.has_kingside_castling_rights(color=chess.WHITE))
    white_king_castling = np.full((8, 8), white_king_castling)
    white_queen_castling = int(board.has_queenside_castling_rights(color=chess.WHITE))
    white_queen_castling = np.full((8, 8), white_queen_castling)
    black_king_castling = int(board.has_kingside_castling_rights(color=chess.BLACK))
    black_king_castling = np.full((8, 8), black_king_castling)
    black_queen_castling = int(board.has_queenside_castling_rights(color=chess.BLACK))
    black_queen_castling = np.full((8, 8), black_queen_castling)

    stack = []
    stack.extend([deepcopy(numpy_board), deepcopy(move_board)])
    stack.extend([deepcopy(white_king_castling), deepcopy(white_queen_castling)])
    stack.extend([deepcopy(black_king_castling), deepcopy(black_queen_castling)])
    stack = np.stack(stack)

    move_number += 1
    dataset.append(deepcopy(stack))

print(len(dataset))

split_dataset = []

#dataset = [1, 2, 3, 4, 5, 6]
for i in range(0, len(dataset), 1):
    chunk = dataset[i:i + 2]
    if len(chunk) == 2:
        split_dataset.append(deepcopy(chunk))

print(len(split_dataset))
#print(split_dataset)

