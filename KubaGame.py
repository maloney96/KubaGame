# Author: Liam Maloney
# Date June 9th, 2021
# Description: *Kuba Board Game*
#     Takes 2 players as a tuple, with winning player being the first one to capture 7 red marbles or eliminate all of oppent's marbles.
#     Either player may start, with turns alternating after a successful move.
#     Balls may be pushed left, right, backward, or forward, but must have an empty space in opposite direction of
#     the push direction. Cannot revert an opponent's turn.

import copy

class KubaGame():
    '''
    Class for playing the Kuba Board Game.
    Takes 2 players as a tuple, with winning player being the first one to capture 7 red marbles or eliminate all of oponnent's marbles.
    Either player may start, with turns alternating after a successful move.
    Balls may be pushed left, right, backward, or forward, but must have an empty space in opposite direction of
    the push direction. Cannot revert an opponent's turn.
    '''
    def __init__(self, p1, p2):
        '''
        Initializes private data members of both players, red marbles (as a player), the board,
        current turn, winner, dictionary of marbles to initialize the board,  both player's captured red marbles, and previous iterations of the board by player
        '''
        self._p1 = p1
        self._p2 = p2
        self._red_m = ("Board","R")
        self._board = [[" " for i in range(7)] for j in range(7)]
        self._turn = None       # initialize player turn to None, update once a move is made
        self._winner = None     # updated once a player has 7 red marbles captured or opponent has run out of marbles
        self._marbles = {}
        self._p1_red_captured = 0
        self._p2_red_captured = 0
        self._previous_p1_board = None
        self._previous_p2_board = None

        # Create default dictionaries for each player
        self._marbles.setdefault(self._p1[0],[])
        self._marbles.setdefault(self._p2[0],[])
        self._marbles.setdefault(self._red_m[0],[])

        # Add marbles of appropriate color to each player's dictionary
        for marble in range(0,8):
            self._marbles[self._p1[0]].append(self._p1[1])
            self._marbles[self._p2[0]].append(self._p2[1])

        for marble in range(0,12):
            self._marbles[self._red_m[0]].append(self._red_m[1])

        #Append each player's marbles to the board
        for player in self._marbles:
            for marble in self._marbles[player]:
                #P1 Marbles
                if player is self._p1[0]:
                    for i in range(0,2):
                        self._board[0][i] = marble
                        self._board[1][i] = marble
                    for i in range(5,7):
                        self._board[5][i] = marble
                        self._board[6][i] = marble
                #P2 Marbles
                if player is self._p2[0]:
                    for i in range(5,7):
                        self._board[0][i] = marble
                        self._board[1][i] = marble
                    for i in range(0,2):
                        self._board[5][i] = marble
                        self._board[6][i] = marble
                #Red Marbles
                if player is self._red_m[0]:
                    self._board[1][3] = marble
                    self._board[5][3] = marble
                    for i in range(2,5):
                        self._board[2][i] = marble
                        self._board[4][i] = marble
                    for i in range(1,6):
                        self._board[3][i] = marble

    def display_board(self):
        '''Displays the current state of the board'''
        for row in self._board:
            print(row)

    def get_player_color(self, player_name):
        '''Returns the color associated with the current player'''
        if self._p1[0] == player_name:
            return self._p1[1]
        elif self._p2[0] == player_name:
            return self._p2[1]

    def get_player_name(self, color):
        '''Returns the name associated with player color'''
        if self._p1[1] == color:
            return self._p1[0]
        elif self._p2[1] == color:
            return self._p2[0]

    def player_score_plus_one(self,player_name):
        '''Updates the player's score after successful capture'''
        if self._p1[0] == player_name:
            self._p1_red_captured += 1
        elif self._p2[0] == player_name:
            self._p2_red_captured += 1

    def get_current_turn(self):
        '''Returns the player name of current player's turn'''
        return self._turn

    def make_move(self, player_name, coordinates, direction):
        '''
        Moves the marble of specified player name in a direction left, right, forward, or backward.
        Coordinates contain location of current marble being moved.
        After successful move, update the player's count of captured red marbles if red capture occurred,
        then calls update_game_status to check for a winner.
        Update player's turn to player name of person who didn't just complete the move.
        '''

        # Check to make sure it's correct player's turn
        if self._turn != None:
            if player_name == self._p1[0]:
                if player_name != self.get_current_turn():
                    return False
            if player_name == self._p2[0]:
                if player_name != self.get_current_turn():
                    return False

        # Board pre-move
        board_pre_move = copy.deepcopy(self._board)

        # Original board
        if self._turn is None:
            if player_name == self._p1[0]:
                self._previous_p1_board = copy.deepcopy(self._board)
            if player_name == self._p2[0]:
                self._previous_p2_board = copy.deepcopy(self._board)

        # Finds color of the marble trying to be pushed
        pushing_marble = self.get_marble(coordinates)

        # Prevents the player from pushing marbles that are not their own color, unless the marble was pushed as a result of
        # a previous marble push
        if self.get_player_color(player_name) != pushing_marble:
            return False

        # Stop move if there is already a winner
        if self._winner != None:
            return False

        # Sets baseline squares for front/back comparison
        backward_coordinates = (coordinates[0] + 1, coordinates[1])

        if backward_coordinates[0] == 7:
            backward_space = None
        else:
            backward_space = self.get_marble(backward_coordinates)

        forward_coordinates = (coordinates[0] - 1, coordinates[1])
        if forward_coordinates[0] == -1:
            forward_space = None
        else:
            forward_space = self.get_marble(forward_coordinates)

        # Sets baseline squares for right/left comparison

        right_coordinates = (coordinates[0], coordinates[1] + 1)

        if right_coordinates[1] == 7:
            right_space = None
        else:
            right_space = self.get_marble(right_coordinates)

        left_coordinates = (coordinates[0], coordinates[1] - 1)
        if left_coordinates[1] == -1:
            left_space = None
        else:
            left_space = self.get_marble(left_coordinates)

        # Left
        if direction == "L":

            # Baseline condition, must be empty space to the right of the pushing marble
            if right_space == "X" or right_space == None:

                if left_space != None:
                    # Iterate through everything to the left until blank space is hit
                    # make sure marbles stop at that point
                    current_row = self._board[coordinates[0]]
                    starting_col_range = coordinates[1] + 1

                    marble_shift_count = 0
                    moving_marbles_list = []
                    for marble in reversed(current_row[0:starting_col_range]):
                        if marble == " ":
                            break
                        else:
                            marble_shift_count += 1
                            moving_marbles_list.append(marble)

                    #Set pushing marbles coordinates to be empty again
                    self.set_marble(coordinates, " ")


                    for i in range(0,marble_shift_count):
                         new_left_coordinates = (coordinates[0],coordinates[1]-1-i)
                        #Check to see if we are off the board with the push
                         if new_left_coordinates[1] == -1:
                            if moving_marbles_list[i] == "R":
                                self.player_score_plus_one(player_name)
                         else:
                            self.set_marble(new_left_coordinates,moving_marbles_list[i])

                if left_space is None:
                        self.set_marble(coordinates, " ")

            else:
                return False

        # Right
        if direction == "R":

            # Baseline condition, must be empty space to the left of the pushing marble
            if left_space == "X" or left_space == None:

                if right_space != None:
                    # Iterate through everything to the right until blank space is hit
                    # make sure marbles stop at that point
                    current_row = self._board[coordinates[0]]
                    starting_col_range = coordinates[1]

                    marble_shift_count = 0
                    moving_marbles_list = []
                    for marble in current_row[starting_col_range:7]:
                        if marble == " ":
                            break
                        else:
                            marble_shift_count += 1
                            moving_marbles_list.append(marble)

                    #Set pushing marbles coordinates to be empty again
                    self.set_marble(coordinates, " ")

                    for i in range(0,marble_shift_count):
                         new_right_coordinates = (coordinates[0],coordinates[1]+1+i)
                        #Check to see if we are off the board with the push
                         if new_right_coordinates[1] == 7:
                            if moving_marbles_list[i] == "R":
                                self.player_score_plus_one(player_name)
                         else:
                            self.set_marble(new_right_coordinates,moving_marbles_list[i])

                if right_space is None:
                    self.set_marble(coordinates, " ")

            else:
                return False

        # Backward
        if direction == "B":

             # Baseline condition, must be empty space to the forward of the pushing marble
            if forward_space == "X" or forward_space == None:

                if backward_space != None:
                    # Iterate through everything to the back until blank space is hit
                    # make sure marbles stop at that point
                    marble_shift_count = 0
                    moving_marbles_list = []

                    for i in range(coordinates[0],7):
                        if self._board[i][coordinates[1]] == " ":
                            break
                        else:
                            marble_shift_count +=1
                            moving_marbles_list.append(self.get_marble((i,coordinates[1])))

                    # Set pushing marbles coordinates to be empty again
                    self.set_marble(coordinates, " ")

                    for i in range(0,marble_shift_count):
                         new_backward_coordinates = (coordinates[0]+1+i,coordinates[1])
                        #Check to see if we are off the board with the push
                         if new_backward_coordinates[0] == 7:
                            if moving_marbles_list[i] == "R":
                                self.player_score_plus_one(player_name)
                         else:
                            self.set_marble(new_backward_coordinates,moving_marbles_list[i])

                if backward_space is None:
                    self.set_marble(coordinates, " ")

            else:
                return False

        # Forward
        if direction == "F":

             # Baseline condition, must be empty space to the backward of the pushing marble
            if backward_space == "X" or backward_space == None:

                if forward_space != None:
                    marble_shift_count = 0
                    moving_marbles_list = []

                    for i in range(coordinates[0],-1, -1):
                        if self._board[i][coordinates[1]] == " ":
                            break
                        else:
                            marble_shift_count +=1
                            moving_marbles_list.append(self.get_marble((i,coordinates[1])))

                    # Set pushing marbles coordinates to be empty again
                    self.set_marble(coordinates, " ")

                    for i in range(0,marble_shift_count):
                         new_forward_coordinates = (coordinates[0]-1-i,coordinates[1])
                        #Check to see if we are off the board with the push
                         if new_forward_coordinates[0] == -1:
                            if moving_marbles_list[i] == "R":
                                self.player_score_plus_one(player_name)
                         else:
                            self.set_marble(new_forward_coordinates,moving_marbles_list[i])

                if forward_space is None:
                    self.set_marble(coordinates, " ")

            else:
                return False

        # Check to see if the board was just undone from previous move
        # If so revert the board and return false
        if self._board == self._previous_p1_board:
            self._board = board_pre_move
            return False
        if self._board == self._previous_p2_board:
            self._board = board_pre_move
            return False

        # Update player's previous board to the board that just made a successful move
        if self._p1[0] == player_name:
            self._previous_p1_board = copy.deepcopy(self._board)
        if self._p2[0] == player_name:
            self._previous_p2_board = copy.deepcopy(self._board)


        # Update player turn
        if self._p1[0] == player_name:
            self._turn = self._p2[0]
        if self._p2[0] == player_name:
            self._turn = self._p1[0]

        # After successful move check to see if there is a winner
        self.update_game_state(player_name)

        return True

    def update_game_state(self, player_name):
        '''
        Checks to see if a player has captured 7 red marbles.
        Check to see if either player has no marbles remaining on the board, if so.. the opposing player is declared the winner.
        Updates the current winner of the game if applicable.
        '''
        if self.get_captured(player_name) == 7:
            self._winner = player_name

        remaining_marbles = self.get_marble_count()

        loser = None

        for color in remaining_marbles:
            if color == 0:
                loser = self.get_player_name(color)

        if loser != None:
            if self._p1[0] == loser:
                self._winner = self._p2[0]
            if self._p2[0] == loser:
                self._winner = self._p1[0]

    def get_winner(self):
        '''Returns name of player who has won'''
        return self._winner

    def get_captured(self, player_name):
        '''Returns player's number of captured red marbles'''
        if player_name == self._p1[0]:
            return self._p1_red_captured
        elif player_name == self._p2[0]:
            return self._p2_red_captured

    def get_marble(self, coordinates):
        '''
        Returns the marble that is present at the coordinates location.
        If there is none, the coordinate location returned is 'X'.
        Will index the list at given position to find this marble.
        '''
        if self._board[coordinates[0]][coordinates[1]] != " ":
            return self._board[coordinates[0]][coordinates[1]]
        else:
            return "X"

    def set_marble(self, coordinates, marble):
        '''Sets the marble at specified coordinates'''
        self._board[coordinates[0]][coordinates[1]] = marble

    def get_marble_count(self):
        '''
        Returns the number of white, black, and red marbles on the board, in a tuple. In that order.
        Will iterate through boards list of lists, appending these to a tuple result that is then returned.
        '''
        white = 0
        black = 0
        red = 0

        for marbles in self._board:
            for marble in marbles:
                if marble == "W":
                    white += 1
                elif marble == "B":
                     black += 1
                elif marble == "R":
                     red +=1

        return (white,black,red)
