import chess.pgn
import numpy as np

text = """1. e4 e6 2. d4 d5 3. Nc3 Bb4 4. e5 Ne7 5. a3 Bxc3+ 6. bxc3 c5 7. Qg4 Qc7 8. Qxg7 Rg8 9. Qxh7 cxd4 10. Ne2 dxc3 11. f4 d4 12. h4 Nbc6 13. h5 Bd7 14. h6 O-O-O 15. Qd3 Rg6 16. h7 Rh8 17. Nxd4 Nxd4 18. Qxd4 Kb8 19. Rh3 Nf5 20. Qb4 Bc6 21. a4 Bxg2 22. Rxc3 Qb6 23. Qxb6 axb6 24. Ba3 Bxf1 25. O-O-O Bg2 26. Bd6+ Ka7 27. Rc7 Rxh7 28. Rc8 Rhg7 29. Bb8+ Ka6 30. Bc7 Rg8 31. Rdd8 Rxd8 32. Rxd8 Ka7 33. Bb8+ Ka6 34. Bc7 Ka7 35. Bb8+ Ka8 36. Bc7+ Ka7 1/2-1/2"""
text = """1. e4"""

class Probability_Matrix():
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


    def move_value(self, move, stack, board):
            # this function just looks up a value      
            # network will output 8x8x76
            # figure out the value of the corresponding move played by the child
            # stack is returned and move given and we want to find value

            """
                - make 8 planes → each represent {N, NE, E, SE, S, SW, W, NW}
                - 7 stacks of them representing moving the shape 1 to 7
                - eight knight moves
                - move pawn up and promote to queen
                - capture left
                    - promote queen
                    - promote knight
                    - promote bishop
                    - promote rook
                - capture right
                    - promote queen
                    - promote knight
                    - promote bishop
                    - promote rook
            """
            
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
                        return stack[rank_s][file_s][56]
                    if file_s - file_e == -1: # right
                        return stack[rank_s][file_s][57]
                if rank_s - rank_e == 2: # down the board
                    if file_s - file_e == 1: # left
                        return stack[rank_s][file_s][58] 
                    if file_s - file_e == -1: # right
                        return stack[rank_s][file_s][59] 
                if file_s - file_e == -2: # right
                    if rank_s - rank_e == 1:
                        return stack[rank_s][file_s][60] 
                    if rank_s - rank_e == -1:
                        return stack[rank_s][file_s][61] 
                if file_s - file_e == 2: # left
                    if rank_s - rank_e == 1:
                        return stack[rank_s][file_s][62] 
                    if rank_s - rank_e == -1:
                        return stack[rank_s][file_s][63] 
                    
            if piece == "p":
                if len(str(move)) == 5:
                    if rank_s - rank_e == -1: # capture up
                        if file_s - file_e == -1: # capture left
                            if move[4] == "r": # promote to rook
                                return stack[rank_s][file_s][64]
                            if move[4] == "b": # promote to bishop
                                return stack[rank_s][file_s][65] 
                            if move[4] == "n": # promote to knight
                                return stack[rank_s][file_s][66] 
                        if file_s - file_e == 1: # capture right
                            if move[4] == "r": # promote to rook
                                return stack[rank_s][file_s][67] 
                            if move[4] == "b": # promote to bishop
                                return stack[rank_s][file_s][68] 
                            if move[4] == "n": # promote to knight
                                return stack[rank_s][file_s][69] 
                    if rank_s - rank_e == 1: # capture down
                        if file_s - file_e == -1: # capture left
                            if move[4] == "r": # promote to rook
                                return stack[rank_s][file_s][70] 
                            if move[4] == "b": # promote to bishop
                                return stack[rank_s][file_s][71] 
                            if move[4] == "n": # promote to knight
                                return stack[rank_s][file_s][72] 
                        if file_s - file_e == 1: # capture right
                            if move[4] == "r": # promote to rook
                                return stack[rank_s][file_s][73] 
                            if move[4] == "b": # promote to bishop
                                return stack[rank_s][file_s][74] 
                            if move[4] == "n": # promote to knight
                                return stack[rank_s][file_s][75] 
            
            if rank_s > rank_e and file_s - file_e == 0: # N # other cases of moving
                return stack[rank_s][file_s][distance - 1]
            if rank_s > rank_e and file_s > file_e: # NE
                return stack[rank_s][file_s][7 * 1 + distance - 1] 
            if rank_s == rank_e and file_s < file_e: # E
                return stack[rank_s][file_s][7 * 2 + distance - 1] 
            if rank_s < rank_e and file_s < file_e: # SE
                return stack[rank_s][file_s][7 * 3 + distance - 1]
            if rank_s < rank_e and file_s - file_e == 0: # S
                return stack[rank_s][file_s][7 * 4 + distance - 1] 
            if rank_s < rank_e and file_s < file_e: # SW
                return stack[rank_s][file_s][7 * 5 + distance - 1] 
            if rank_s == rank_e and file_s > file_e: # W
                return stack[rank_s][file_s][7 * 6 + distance - 1] 
            if rank_s > rank_e and file_s < file_e: # NW
                return stack[rank_s][file_s][7 * 7 + distance - 1]
            
            
            # return 0



split_text = text.split(" ")
print(split_text)

clean_list = []
for item in split_text:
    if item[0].isnumeric() == False:
        clean_list.append(item)

probability_matrix = Probability_Matrix()

print("")
print(clean_list)
board = chess.Board()

move_number = 0
for move in clean_list: 
    print("")
    print(move)
    move_made = str(board.push_san(move))
    print(move_made)
    print(board)

    stack = np.zeros((8, 8, 76))

    player = 2
    if move_number % 2 == 0:
        player = 1
    
    stack = probability_matrix.fill_stack(stack, move_made, player, board)

    move_number += 1

    print(stack.shape)



    

    


    




        

