#from connectfour.agents.computer_player import RandomAgent
from connectfour.agents.agent import Agent
import random
import copy

PLAYER_1 = 1
PLAYER_2 = 2
PLAYER_1_WIN = "1111"
PLAYER_2_WIN = "2222"

class StudentAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        #Game over, no need for moves

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
            #Not starting first, determine best move using MiniMax
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

        #Arrays used for checking substrings of connections
        connected3_player1 = ['0111','1110','1101','1011']
        connected3_player2 = ['0222','2220','2202','2022']
        connected2_player1 = ['0011','1100','0110','1010','0101']
        connected2_player2 = ['0022','2200','0220','0202','2020']

        board_evaluation = 0
        current_player = self.id
        opponent = PLAYER_1
        if current_player == PLAYER_1:
            opponent = PLAYER_2

        #HORIZONTAL CHECK
        #Loop through all rows of the board
        for row in board.board:
            connected = 1
            #Concatenate row into a single string for easier evalutation
            rowString = ''.join(str(e) for e in row)
            #Scan row for connections
            #Assign board evaluation based on PLAYER_1 playing
            if current_player == PLAYER_1:
                #Checking for a loss, this results in worst score -100
                if PLAYER_2_WIN in rowString:
                    board_evaluation -= 100
                #Checking for 4 connected, resulting in a win, add big number to evaluation
                elif PLAYER_1_WIN in rowString:
                    board_evaluation += 100
                #Checking for any open 3 connected, good chance at victory
                elif any(x in rowString for x in connected3_player1):
                    board_evaluation += 5
                #checking for opponent open 3 connected, defend if possible
                elif any(x in rowString for x in connected3_player2):
                    board_evaluation -= 8
                #Checking for possible open 2 in a row
                elif any(x in rowString for x in connected2_player1):
                    board_evaluation += 2
                #checking for opponent connect 2 in a row, less priority
                elif any(x in rowString for x in connected2_player2):
                    board_evaluation -= 1

            #Assign board evaluation based on PLAYER_2 playing
            else:
                #Checking for a loss, this results in worst score -100
                if PLAYER_1_WIN in rowString:
                    board_evaluation -= 100
                #Checking for 4 connected, resulting in a win, add big number to evaluation
                elif PLAYER_2_WIN in rowString:
                    board_evaluation += 100
                #Checking for any open 3 connected, good chance at victory
                elif any(x in rowString for x in connected3_player2):
                    board_evaluation += 5
                #checking for opponent open 3 connected, defend if possible
                elif any(x in rowString for x in connected3_player1):
                    board_evaluation -= 8
                #Checking for possible open 2 in a row
                elif any(x in rowString for x in connected2_player2):
                    board_evaluation += 2
                #checking for opponent connect 2 in a row, less priority
                elif any(x in rowString for x in connected2_player1):
                    board_evaluation -= 1
        
        #VERTICAL CHECK
        #WORKING ON IT

        return board_evaluation