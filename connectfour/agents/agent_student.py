#from connectfour.agents.computer_player import RandomAgent
from connectfour.agents.agent import Agent
import random
import copy

class StudentAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 1


    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """



        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, 1) )

        bestMove = moves[vals.index( max(vals) )]

        #Checking for empty board
        empty = 0
        for i in range(0, board.width):
                if board.board[5][i] == 0:
                    empty += 1
        if empty == 7:
            #Board is empty, best move is center
            return 5, 3
        else:
            return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states
        
        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])
                
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1) )

        
        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    def evaluateBoardState(self, board):
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """
        
        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """
        #return random.uniform(-1, 1)

        current_score = 0
        current_player = self.id

        #Horizontal check
        for row in board.board:
            curr = row[0]
            same_count = 1
            for i in range(1, board.width):
                if row[i] == curr:
                    same_count += 1
                    if same_count == 2 and curr != 0:
                        if curr == current_player:
                            current_score += 10
                        else:
                            current_score -= 10
                else:
                    same_count = 1
                    curr = row[i]

        for row in board.board:
            curr = row[0]
            same_count = 1
            for i in range(1, board.width):
                if row[i] == curr:
                    same_count += 1
                    if same_count == 3 and curr != 0:
                        if curr == current_player:
                            current_score += 100
                        else:
                            current_score -= 100
                else:
                    same_count = 1
                    curr = row[i]

        for row in board.board:
            curr = row[0]
            same_count = 1
            for i in range(1, board.width):
                if row[i] == curr:
                    same_count += 1
                    if same_count == 4 and curr != 0:
                        if curr == current_player:
                            current_score += 1000
                        else:
                            current_score -= 1000
                else:
                    same_count = 1
                    curr = row[i]


        #vertical check
        for i in range(board.width):
            same_count = 1
            curr = board.board[0][i]
            for j in range(1, board.height):
                if board.board[j][i] == curr:
                    same_count += 1
                    if same_count == 2 and curr != 0:
                        if curr == current_player:
                            current_score += 10
                        else:
                            current_score -= 10
                    else:
                        same_count = 1
                        curr = board.board[j][i]

        for i in range(board.width):
            same_count = 1
            curr = board.board[0][i]
            for j in range(1, board.height):
                if board.board[j][i] == curr:
                    same_count += 1
                    if same_count == 3 and curr != 0:
                        if curr == current_player:
                            current_score += 100
                        else:
                            current_score -= 100
                    else:
                        same_count = 1
                        curr = board.board[j][i]

        for i in range(board.width):
            same_count = 1
            curr = board.board[0][i]
            for j in range(1, board.height):
                if board.board[j][i] == curr:
                    same_count += 1
                    if same_count == 4 and curr != 0:
                        if curr == current_player:
                            current_score += 1000
                        else:
                            current_score -= 1000
                    else:
                        same_count = 1
                        curr = board.board[j][i]

        #diagonal check
        boards = [
            board.board,
            [row[::-1] for row in copy.deepcopy(board.board)]
        ]
        for b in boards:
            for i in range(board.width - 2 + 1):
                for j in range(board.height - 2 + 1):
                    if i > 0 and j > 0:
                        continue

                    same_count = 1
                    curr = b[j][i]
                    k, m = j + 1, i + 1
                    while k < board.height and m < board.width:
                        if b[k][m] == curr:
                            same_count += 1
                            if same_count is 2 and curr != 0:
                                if curr == current_player:
                                    current_score += 10
                                else:
                                    current_score -= 10
                            else:
                                same_count = 1
                                curr = b[k][m]
                        k += 1
                        m += 1

        boards = [
            board.board,
            [row[::-1] for row in copy.deepcopy(board.board)]
        ]
        for b in boards:
            for i in range(board.width - 3 + 1):
                for j in range(board.height - 3 + 1):
                    if i > 0 and j > 0:
                        continue

                    same_count = 1
                    curr = b[j][i]
                    k, m = j + 1, i + 1
                    while k < board.height and m < board.width:
                        if b[k][m] == curr:
                            same_count += 1
                            if same_count is 3 and curr != 0:
                                if curr == current_player:
                                    current_score += 100
                                else:
                                    current_score -= 100
                            else:
                                same_count = 1
                                curr = b[k][m]
                        k += 1
                        m += 1


        boards = [
            board.board,
            [row[::-1] for row in copy.deepcopy(board.board)]
        ]
        for b in boards:
            for i in range(board.width - 4 + 1):
                for j in range(board.height - 4 + 1):
                    if i > 0 and j > 0:
                        continue

                    same_count = 1
                    curr = b[j][i]
                    k, m = j + 1, i + 1
                    while k < board.height and m < board.width:
                        if b[k][m] == curr:
                            same_count += 1
                            if same_count is 4 and curr != 0:
                                if curr == current_player:
                                    current_score += 1000
                                else:
                                    current_score -= 1000
                            else:
                                same_count = 1
                                curr = b[k][m]
                        k += 1
                        m += 1

        return current_score