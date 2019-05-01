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

        #Values used for checking board evaluation
        #Horizontal Checks
        h_connected3_player1 = ['0111','1110','1101','1011']
        h_connected3_player2 = ['0222','2220','2202','2022']
        h_connected2_player1 = ['0011','1100','0110','1010','0101']
        h_connected2_player2 = ['0022','2200','0220','0202','2020']

        #Vertical Checks, Reversed due to how columns work
        v_connected3_player1 = "0111"
        v_connected3_player2 = "0222"
        v_connected2_player1 = "0011"
        v_connected2_player2 = "0022"

        #Positive slope diagonal
        positive_slopes = []
        #loop through board diagonally and append them as strings
        for line in range(1, (board.height + board.width)):
            slopeString = ""
            startingColumn = max(0, line - board.height)
            count = min(line, (board.width - startingColumn), board.height)
            for j in range(0, count):
                slopeString += str(board.board[min(board.height, line) - j - 1][startingColumn + j])
            #Append only necessary strings
            if len(slopeString) >= 4:
                positive_slopes.append(slopeString)

        #Negative Slop diagonal
        flippedBoard = [row[:] for row in board.board]
        count = 0
        for row in flippedBoard:
            if count == 6:
                count = 0
            row = list(reversed(row))
            #adding reversed values to flippedBoard itself
            for i in range(len(row)):
                flippedBoard[count][i] = row[i]
            count += 1

        negative_slopes = []
        #loop through board diagonally and append them as strings
        for line in range(1, (board.height + board.width)):
            slopeString = ""
            startingColumn = max(0, line - board.height)
            count = min(line, (board.width - startingColumn), board.height)
            for j in range(0, count):
                slopeString += str(flippedBoard[min(board.height, line) - j - 1][startingColumn + j])
            #Append only necessary strings
            if len(slopeString) >= 4:
               negative_slopes.append(slopeString)

        #Initial board evaluation 0
        board_evaluation = 0

        #Assign player ID's
        current_player = self.id
        opponent = PLAYER_1
        if current_player == PLAYER_1:
            opponent = PLAYER_2

        #HORIZONTAL CHECK
        #Loop through all rows of the board
        for row in board.board:
            #Concatenate row into a single string for easier evalutation
            rowString = ''.join(str(e) for e in row)
            
            #Assign horizontal evaluation based on PLAYER_1 playing
            if current_player == PLAYER_1:
                #Checking for a loss, this results in worst score -100
                if PLAYER_2_WIN in rowString:
                    board_evaluation -= 100
                #Checking for 4 connected, resulting in a win, add big number to evaluation
                elif PLAYER_1_WIN in rowString:
                    board_evaluation += 100
                #Checking for any open 3 connected, good chance at victory
                elif any(x in rowString for x in h_connected3_player1):
                    board_evaluation += 5
                #checking for opponent open 3 connected, defend if possible
                elif any(x in rowString for x in h_connected3_player2):
                    board_evaluation -= 4
                #Checking for possible open 2 in a row
                elif any(x in rowString for x in h_connected2_player1):
                    board_evaluation += 2
                #checking for opponent connect 2 in a row, less priority
                elif any(x in rowString for x in h_connected2_player2):
                    board_evaluation -= 1

            #Assign horizontal evaluation based on PLAYER_2 playing
            else:
                #Checking for a loss, this results in worst score -100
                if PLAYER_1_WIN in rowString:
                    board_evaluation -= 100
                #Checking for 4 connected, resulting in a win, add big number to evaluation
                elif PLAYER_2_WIN in rowString:
                    board_evaluation += 100
                #Checking for any open 3 connected, good chance at victory
                elif any(x in rowString for x in h_connected3_player2):
                    board_evaluation += 5
                #checking for opponent open 3 connected, defend if possible
                elif any(x in rowString for x in h_connected3_player1):
                    board_evaluation -= 4
                #Checking for possible open 2 in a row
                elif any(x in rowString for x in h_connected2_player2):
                    board_evaluation += 2
                #checking for opponent connect 2 in a row, less priority
                elif any(x in rowString for x in h_connected2_player1):
                    board_evaluation -= 1
        
        #VERTICAL CHECK
        #Loop through all columns
        for i in range(board.width):
            columnString = ''
            #Generating string so evaltion can be done to column
            for j in range(board.height):
                columnString += str(board.board[j][i])
            #Assign vertical evaluation based on PLAYER_1 playing
            if current_player == PLAYER_1:
                #Checking for a loss, this results in worst score -100
                if PLAYER_2_WIN in columnString:
                    board_evaluation -= 100
                #4 vertical connected, Win
                elif PLAYER_1_WIN in columnString:
                    board_evaluation += 100
                #Checking for any open 3 vertical connected
                elif v_connected3_player1 in columnString:
                    board_evaluation += 5
                #Checking for opponent vertical 3
                elif v_connected2_player2 in columnString:
                    board_evaluation -= 4
                #Checking for vertical 2 connections
                elif v_connected2_player1 in columnString:
                    board_evaluation += 2
                #Checking for opponent 2 connections
                elif v_connected2_player2 in columnString:
                    board_evaluation -= 1

            #Assign vertical evaluation based on PLAYER_2 playing
            else:
                #Checking for a loss, this results in worst score -100
                if PLAYER_1_WIN in columnString:
                    board_evaluation -= 100
                #4 vertical connected, Win
                elif PLAYER_2_WIN in columnString:
                    board_evaluation += 100
                #Checking for any open 3 vertical connected
                elif v_connected3_player2 in columnString:
                    board_evaluation += 5
                #Checking for opponent vertical 3
                elif v_connected2_player1 in columnString:
                    board_evaluation -= 4
                #Checking for vertical 2 connections
                elif v_connected2_player2 in columnString:
                    board_evaluation += 2
                #Checking for opponent 2 connections
                elif v_connected2_player1 in columnString:
                    board_evaluation -= 1

        #DIAGONAL CHECKS
        #POSITIVE SLOPE
        for checkString in positive_slopes:
            #Diagonal evaluation based on PLAYER_1 playing
            if current_player == PLAYER_1:
                #Checking for a loss, this results in worst score -100
                if PLAYER_2_WIN in checkString:
                    board_evaluation -= 100
                #Checking for 4 connected, resulting in a win, add big number to evaluation
                elif PLAYER_1_WIN in checkString:
                    board_evaluation += 100
                #USES H_CONNECTED as similar checks
                #Checking for any open 3 connected, good chance at victory
                elif any(x in checkString for x in h_connected3_player1):
                    board_evaluation += 5
                #checking for opponent open 3 connected, defend if possible
                elif any(x in checkString for x in h_connected3_player2):
                    board_evaluation -= 4
                #Checking for possible open 2 in a row
                elif any(x in checkString for x in h_connected2_player1):
                    board_evaluation += 2
                #checking for opponent connect 2 in a row, less priority
                elif any(x in checkString for x in h_connected2_player2):
                    board_evaluation -= 1

            #Diagonal evaluation based on PLAYER_2 playing
            else:
                #Checking for a loss, this results in worst score -100
                if PLAYER_1_WIN in checkString:
                    board_evaluation -= 100
                #Checking for 4 connected, resulting in a win, add big number to evaluation
                elif PLAYER_2_WIN in checkString:
                    board_evaluation += 100
                #USES H_CONNECTED as similar checks
                #Checking for any open 3 connected, good chance at victory
                elif any(x in checkString for x in h_connected3_player2):
                    board_evaluation += 5
                #checking for opponent open 3 connected, defend if possible
                elif any(x in checkString for x in h_connected3_player1):
                    board_evaluation -= 4
                #Checking for possible open 2 in a row
                elif any(x in checkString for x in h_connected2_player2):
                    board_evaluation += 2
                #checking for opponent connect 2 in a row, less priority
                elif any(x in checkString for x in h_connected2_player1):
                    board_evaluation -= 1

        #NEGATIVE SLOPE
        for checkString in negative_slopes:
            #Diagonal evaluation based on PLAYER_1 playing
            if current_player == PLAYER_1:
                #Checking for a loss, this results in worst score -100
                if PLAYER_2_WIN in checkString:
                    board_evaluation -= 100
                #Checking for 4 connected, resulting in a win, add big number to evaluation
                elif PLAYER_1_WIN in checkString:
                    board_evaluation += 100
                #USES H_CONNECTED as similar checks
                #Checking for any open 3 connected, good chance at victory
                elif any(x in checkString for x in h_connected3_player1):
                    board_evaluation += 5
                #checking for opponent open 3 connected, defend if possible
                elif any(x in checkString for x in h_connected3_player2):
                    board_evaluation -= 4
                #Checking for possible open 2 in a row
                elif any(x in checkString for x in h_connected2_player1):
                    board_evaluation += 2
                #checking for opponent connect 2 in a row, less priority
                elif any(x in checkString for x in h_connected2_player2):
                    board_evaluation -= 1

            #Diagonal evaluation based on PLAYER_2 playing
            else:
                #Checking for a loss, this results in worst score -100
                if PLAYER_1_WIN in checkString:
                    board_evaluation -= 100
                #Checking for 4 connected, resulting in a win, add big number to evaluation
                elif PLAYER_2_WIN in checkString:
                    board_evaluation += 100
                #USES H_CONNECTED as similar checks
                #Checking for any open 3 connected, good chance at victory
                elif any(x in checkString for x in h_connected3_player2):
                    board_evaluation += 5
                #checking for opponent open 3 connected, defend if possible
                elif any(x in checkString for x in h_connected3_player1):
                    board_evaluation -= 4
                #Checking for possible open 2 in a row
                elif any(x in checkString for x in h_connected2_player2):
                    board_evaluation += 2
                #checking for opponent connect 2 in a row, less priority
                elif any(x in checkString for x in h_connected2_player1):
                    board_evaluation -= 1

        return board_evaluation