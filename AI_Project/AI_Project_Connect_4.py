import tkinter as tk
import numpy as np 
winning_score = 1000000
losing_score = -1000000
tie_score = 0
class ConnectFour:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.current_player = 1
    
    def drop_piece(self, col):
        row = 5
        while row >= 0:
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return (row, col)
            row -= 1
        return None
    
    def is_valid_move(self, col):
        return self.board[0][col] == 0
    
    def get_valid_moves(self):
        return [col for col in range(7) if self.is_valid_move(col)]
    
    def check_win(self, player):
        # Check horizontal
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == player and self.board[row][col+1] == player and self.board[row][col+2] == player and self.board[row][col+3] == player:
                    return True
        
        # Check vertical
        for row in range(3):
            for col in range(7):
                if self.board[row][col] == player and self.board[row+1][col] == player and self.board[row+2][col] == player and self.board[row+3][col] == player:
                    return True
        
        # Check diagonal (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == player and self.board[row+1][col+1] == player and self.board[row+2][col+2] == player and self.board[row+3][col+3] == player:
                    return True
        
        # Check diagonal (bottom-left to top-right)
        for row in range(3, 6):
            for col in range(4):
                if self.board[row][col] == player and self.board[row-1][col+1] == player and self.board[row-2][col+2] == player and self.board[row-3][col+3] == player:
                    return True
        
        return False
    
    
    def is_game_over(self):
        return self.check_win(1) or self.check_win(2) or False,None
    
    def switch_player(self):
        self.current_player = 3 - self.current_player
    
    def print_board(self):
        print(np.flip(self.board, axis=0))

class MinimaxAgent:
    def __init__(self, max_depth):
        self.max_depth = max_depth
    def check_game_over(self,game):
        if game.check_win(1):
        
            return True
        elif game.check_win(2):
            
            return True
        elif len(self.get_valid_moves(game)) == 0:
            return True    
    def get_valid_moves(self,game):
        return [col for col in range(7) if game.is_valid_move(col)]
    
    def get_move(self, game):
        best_move = None
        best_score = -np.inf
        for move in game.get_valid_moves():
            new_game = ConnectFour()
            new_game.board = np.copy(game.board)
            new_game.current_player = game.current_player
            new_game.drop_piece(move)
            score = self.minimax(new_game, 0, False)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move
    
    
    def minimax(self,game, depth, maximizing_player):
        game_over=self.check_game_over(game)

        if depth == 0 or game_over:
            if game_over:
                if game.check_win(2) :
                    return winning_score
                elif game.check_win(1):
                    return losing_score
                else:
                    return tie_score
            else:
                return self.evaluate_board(2,game)

        if maximizing_player:
            max_score = -np.Inf
            for column in game.get_valid_moves():
                new_game = ConnectFour()
                new_game.board = np.copy(game.board)
                new_game.current_player=2
                new_game.drop_piece(column)
                score = self.minimax(new_game, depth-1, False)
                max_score = max(max_score, score)
            return max_score

        else:
            min_score = np.Inf
            for column in game.get_valid_moves():
                new_game = ConnectFour()
                new_game.board = np.copy(game.board)
                new_game.current_player=2
                new_game.drop_piece(column)
                score = self.minimax(new_game, depth+1, False)
                min_score = min(min_score, score)
            return min_score
    
    
    
    
    
    
    def evaluate_board(self,player,game):
        score = 0

        # Check for horizontal streaks
        for r in range(6):
            row_array = [int(i) for i in list(game.board[r,:])]
            for c in range(7 - 3):
                window = row_array[c:c+4]
                score += self.evaluate_window(window, player)

        # Check for vertical streaks
        for c in range(7):
            col_array = [int(i) for i in list(game.board[:,c])]
            for r in range(6 - 3):
                window = col_array[r:r+4]
                score += self.evaluate_window(window, player)

        # Check for diagonal streaks (top-left to bottom-right)
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [game.board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        # Check for diagonal streaks (bottom-left to top-right)
        for r in range(3, 6):
            for c in range(7 - 3):
                window = [game.board[r-i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score
    
    def evaluate_window(self,window, player):
        score = 0
        opponent = 2 if player == 1 else 1

        if window.count(player) == 4:
            score += winning_score
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 4

        return score
    
    
    
    


class AlphaBetaAgent:
    def __init__(self, max_depth):
        self.max_depth = max_depth
    
    def get_move(self, game):
        best_move = None
        best_score = -np.inf
        alpha = -np.inf
        beta = np.inf
        for move in game.get_valid_moves():
            new_game = ConnectFour()
            new_game.board = np.copy(game.board)
            new_game.current_player = game.current_player
            new_game.drop_piece(move)
            score = self.alphabeta(new_game, 0, False, alpha, beta)
            if score > best_score:
                best_move = move
                best_score = score
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # beta cut-off
        return best_move
    
    def alphabeta(self, game, depth, maximizing_player, alpha, beta):
        if depth == self.max_depth or game.is_game_over():
            return self.evaluate_board(2,game)
        
        if maximizing_player:
            best_score = -np.inf
            for move in game.get_valid_moves():
                new_game = ConnectFour()
                new_game.board = np.copy(game.board)
                new_game.current_player = game.current_player
                new_game.drop_piece(move)
                score = self.alphabeta(new_game, depth+1, False, alpha, beta)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # beta cut-off
            return best_score
        
        else:
            best_score = np.inf
            for move in game.get_valid_moves():
                new_game = ConnectFour()
                new_game.board = np.copy(game.board)
                new_game.current_player = game.current_player
                new_game.drop_piece(move)
                score = self.alphabeta(new_game, depth+1, True, alpha, beta)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # alpha cut-off
            return best_score
    
    
    
    
    def evaluate_board(self,player,game):
        score = 0

        # Check for horizontal streaks
        for r in range(6):
            row_array = [int(i) for i in list(game.board[r,:])]
            for c in range(7 - 3):
                window = row_array[c:c+4]
                score += self.evaluate_window(window, player)

        # Check for vertical streaks
        for c in range(7):
            col_array = [int(i) for i in list(game.board[:,c])]
            for r in range(6 - 3):
                window = col_array[r:r+4]
                score += self.evaluate_window(window, player)

        # Check for diagonal streaks (top-left to bottom-right)
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [game.board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        # Check for diagonal streaks (bottom-left to top-right)
        for r in range(3, 6):
            for c in range(7 - 3):
                window = [game.board[r-i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score
    
    def evaluate_window(self,window, player):
        score = 0
        opponent = 2 if player == 1 else 1

        if window.count(player) == 4:
            score += winning_score
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 4

        return score
    
    
    
    


class ConnectFourGUI:
    def __init__(self):
        self.game = ConnectFour()
        self.agent = None
        self.difficulty = None
        
        self.window = tk.Tk()
        self.window.title("Connect 4")
        
        self.canvas = tk.Canvas(self.window, width=700, height=600, background='blue')
        self.canvas.pack(side=tk.LEFT)
        
        self.game_frame = tk.Frame(self.window)
        self.game_frame.pack(side=tk.RIGHT)
        
        self.algorithm_label = tk.Label(self.game_frame, text="Algorithm:")
        self.algorithm_label.pack()
        
        self.algorithm_var = tk.StringVar(value="Minimax")
        self.algorithm_menu = tk.OptionMenu(self.game_frame, self.algorithm_var, "Minimax", "Alpha-Beta")
        self.algorithm_menu.pack()
        
        self.difficulty_label = tk.Label(self.game_frame, text="Difficulty:")
        self.difficulty_label.pack()
        
        self.difficulty_var = tk.StringVar(value="Easy")
        self.difficulty_menu = tk.OptionMenu(self.game_frame, self.difficulty_var, "Easy", "Medium", "Hard")
        self.difficulty_menu.pack()
        
        self.new_game_button = tk.Button(self.game_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack()
        
        self.message_label = tk.Label(self.game_frame, text="")
        self.message_label.pack()
        
        self.draw_board()
        self.window.mainloop()
    
    def new_game(self):
        self.game = ConnectFour()
        self.message_label.config(text="")
        self.draw_board()
        
        if self.algorithm_var.get() == "Minimax":
            if self.difficulty_var.get() == "Easy":
                self.agent = MinimaxAgent(2)
            elif self.difficulty_var.get() == "Medium":
                self.agent = MinimaxAgent(4)
            else:
                self.agent = MinimaxAgent(6)
        else:
            if self.difficulty_var.get() == "Easy":
                self.agent = AlphaBetaAgent(2)
            elif self.difficulty_var.get() == "Medium":
                self.agent = AlphaBetaAgent(4)
            else:
                self.agent = AlphaBetaAgent(6)
        self.run(self.agent)
        
    
    def run(self,agent):
        game_over = False
        while not game_over:
            # if turn == 0:
            if  self.game.current_player == 1:    
                self.draw_board()
                
                init_column_1 = np.random.randint(0, 6)
                if self.game.is_valid_move(init_column_1):
                    self.game.drop_piece(init_column_1)
                    
                
                
            else:
                
                column = agent.get_move(self.game)
                self.game.drop_piece(column)

            self.draw_board()

            if self.check_game_over():
                break
            else:
                self.game.switch_player()    
        

    def draw_board(self):
        self.canvas.delete("all")
        
        for row in range(6):
            for col in range(7):
                x1 = col * 100
                y1 = row * 100
                x2 = x1 + 100
                y2 = y1 + 100
                color = "white" if self.game.board[row][col] == 0 else "red" if self.game.board[row][col] == 1 else "yellow"
                self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill=color, outline="black")
        
        if self.game.current_player == 2:
            self.message_label.config(text="Red's turn")
        else:
            self.message_label.config(text="Yellow's turn")
    
    def check_game_over(self):
        if self.game.check_win(1):
            self.message_label.config(text="Red wins!")
            return True,1
        elif self.game.check_win(2):
            self.message_label.config(text="Yellow wins!")
            return True,2
        elif len(self.game.get_valid_moves()) == 0:
            self.message_label.config(text="Tie!")
            return True,None
        

    def drop_piece(self, col):
        if not self.game.is_valid_move(col):
            return
        
        self.game.drop_piece(col)
        self.draw_board()
        self.check_game_over()
        
        

gui = ConnectFourGUI()

