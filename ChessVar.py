# Author: Vanja Ninkovic
# GitHub username: VanjaNinkovic
# Date: 5/27/2024
# Description: Created Atomic Chess Woohoo!

class ChessVar:
    """
    Atomic Chess class which will house the game state, moving the pieces, and printing the board.
    """

    def __init__(self):
        self._game_state = "UNFINISHED"
        self._active_player = "WHITE"

        self._dict_board = {
            "a8" : Rook("BLACK"), "b8": Knight("BLACK"), "c8": Bishop("BLACK"), "d8": Queen("BLACK"), "e8": King("BLACK"),
            "f8" : Bishop("BLACK"), "g8": Knight("BLACK"), "h8": Rook("BLACK"), "a7": Pawn("BLACK"), "b7": Pawn("BLACK"),
            "c7": Pawn("BLACK"), "d7": Pawn("BLACK"), "e7": Pawn("BLACK"), "f7": Pawn("BLACK"), "g7": Pawn("BLACK"),
            "h7": Pawn("BLACK"), "a6": "--", "b6": "--", "c6": "--", "d6": "--", "e6": "--", "f6": "--", "g6": "--",
            "h6": "--", "a5": "--", "b5": "--", "c5": "--", "d5": "--", "e5": "--", "f5": "--", "g5": "--",
            "h5": "--", "a4": "--", "b4": "--", "c4": "--", "d4": "--", "e4": "--", "f4": "--", "g4": "--",
            "h4": "--", "a3": "--", "b3": "--", "c3": "--", "d3": "--", "e3": "--", "f3": "--", "g3": "--",
            "h3": "--", "a2": Pawn("WHITE"), "b2": Pawn("WHITE"), "c2": Pawn("WHITE"), "d2": Pawn("WHITE"),
            "e2": Pawn("WHITE"), "f2": Pawn("WHITE"), "g2": Pawn("WHITE"), "h2": Pawn("WHITE"),
            "a1": Rook("WHITE"), "b1": Knight("WHITE"), "c1": Bishop("WHITE"), "d1": Queen("WHITE"), "e1": King("WHITE"),
            "f1": Bishop("WHITE"), "g1": Knight("WHITE"), "h1": Rook("WHITE"),
        }

    def print_board(self):
        """
        Prints out the board which is housed as a dictionary with objects are the values and keys as the board
        spaces
        """
        board = self._dict_board
        count = 0
        initial_num = 8
        for key in board:
            if count == 8:
                print("")
                count = 0
            if count == 0:
                print(initial_num, end=" ")
                initial_num -= 1
            if not isinstance(board[key], str):
                print(board[key].get_symbol(), end=" ")
            else:
                print(board[key], end=" ")
            count += 1

        print("\n   a  b  c  d  e  f  g  h")

    def get_game_state(self):
        """Returns the current state of the game"""
        return self._game_state

    def get_dict_board(self):
        """Method to return the dict"""
        return self._dict_board

    def make_move(self, start_pos, end_pos):
        """ Method that will move pieces to different sections of the board"""

        # First check if the game has not been won already
        if self._game_state != "UNFINISHED":
            return False

        # Check if trying to move an empty space
        if self._dict_board[start_pos] == "--":
            return False

        # Next check if the selected piece is the same color as the active player
        if self._dict_board[start_pos].get_color() != self._active_player:
            return False

        # Next check if the end position is actually a playable location
        if end_pos not in self._dict_board:
            return False

        # Next check if the end_pos has a piece with the same color as the active player
        # This will also make sure you aren't moving to from one spot to the exact same spot
        if not isinstance(self._dict_board[end_pos], str):
            if self._dict_board[end_pos].get_color() == self._active_player:
                return False

        # If above conditional pass we will then attempt to move the piece
        # If the piece cannot be moved due to being blocked or being unable to capture it will return False
        is_valid_move = self._dict_board[start_pos].move(start_pos, end_pos, self)

        if not is_valid_move:
            return False

        # If the piece can move to the end_pos then it will return true and the make_move will handle adjusting the
        # dictionary and capturing/exploding pieces
        if is_valid_move:

            # First we will determine if a piece has been captured by seeing if the end_pos is empty
            if self._dict_board[end_pos] != "--":

                # Check if two kings would die in the explosion if they will then return False
                if self.check_for_two_kings(end_pos) is True:
                    return False

                # Changing active player since move is confirmed to be possible
                if self._active_player == "WHITE":
                    self._active_player = "BLACK"
                else:
                    self._active_player = "WHITE"

                # Both the start and end points will now be empty as the captured piece explodes which also kills the
                # capturing piece
                self._dict_board[end_pos] = "--"
                self._dict_board[start_pos] = "--"

                # Calls for the explosion at the end_pos
                self.explode(end_pos)

                # Now we will check if either side still has their king
                white_king = None
                black_king = None

                for key in self._dict_board:
                    if not isinstance(self._dict_board[key], str):
                        if self._dict_board[key].get_symbol() == "wK":
                            white_king = "alive"
                        if self._dict_board[key].get_symbol() == "bK":
                            black_king = "alive"

                if black_king == "alive" and white_king == "alive":
                    # self.print_board()
                    return True

                else:
                    # if black_king is None and white_king is None:
                    #     self._game_state = "DRAW"
                    #     self.print_dict_board()
                    #     return True
                    if black_king is None:
                        self._game_state = "WHITE_WON"
                        # self.print_board()
                        return True
                    if white_king is None:
                        self._game_state = "BLACK_WON"
                        # self.print_board()
                        return True

            else:
                # Changing active player since move is confirmed to be possible
                if self._active_player == "WHITE":
                    self._active_player = "BLACK"
                else:
                    self._active_player = "WHITE"

                self._dict_board[end_pos] = self._dict_board[start_pos]
                self._dict_board[start_pos] = "--"
                # self.print_board()
                return True

    def explode(self, end_pos):
        """Method which will explode every piece around the captured piece besides the pawns"""
        orig_letter = ord(end_pos[0])
        orig_number = ord(end_pos[1])

        letter = orig_letter
        number = orig_number

        # first delete the places above and below the end_pos
        number += 1
        temp_pos = chr(letter) + chr(number)
        if temp_pos in self._dict_board:
            if not isinstance(self._dict_board[temp_pos], str):
                if self._dict_board[temp_pos].get_symbol() == "wp" or self._dict_board[temp_pos].get_symbol() == "bp":
                    pass
                else:
                    self._dict_board[temp_pos] = "--"

        number -= 2
        temp_pos = chr(letter) + chr(number)
        if temp_pos in self._dict_board:
            if not isinstance(self._dict_board[temp_pos], str):
                if self._dict_board[temp_pos].get_symbol() == "wp" or self._dict_board[temp_pos].get_symbol() == "bp":
                    pass
                else:
                    self._dict_board[temp_pos] = "--"

        # Next we move to get the three places to the left of the end_pos
        letter -= 1
        for place in range(3):
            temp_pos = chr(letter) + chr(number)

            if temp_pos in self._dict_board:
                if not isinstance(self._dict_board[temp_pos], str):
                    if self._dict_board[temp_pos].get_symbol() == "wp" or self._dict_board[temp_pos].get_symbol() == "bp":
                        pass
                    else:
                        self._dict_board[temp_pos] = "--"
            number += 1

        # Finally we go to the three places to the right of the end pos
        letter = orig_letter + 1
        number = orig_number - 1
        for place in range(3):
            temp_pos = chr(letter) + chr(number)

            if temp_pos in self._dict_board:
                if not isinstance(self._dict_board[temp_pos], str):
                    if self._dict_board[temp_pos].get_symbol() == "wp" or self._dict_board[temp_pos].get_symbol() == "bp":
                        pass
                    else:
                        self._dict_board[temp_pos] = "--"
            number += 1

    def check_for_two_kings(self, end_pos):
        """
         A function which will check the area around the captured piece for two kings if both kings are present then
         the move will return false
        """
        orig_letter = ord(end_pos[0])
        orig_number = ord(end_pos[1])

        letter = orig_letter
        number = orig_number
        check_white_king = False
        check_black_king = False
        # Check if end_pos is a king
        if end_pos in self._dict_board:
            if not isinstance(self._dict_board[end_pos], str):
                if self._dict_board[end_pos].get_symbol() == "wK":
                    check_white_king = True
                if self._dict_board[end_pos].get_symbol() == "bK":
                    check_black_king = True

        # first check the places above and below the end_pos
        number += 1
        temp_pos = chr(letter) + chr(number)
        if temp_pos in self._dict_board:
            if not isinstance(self._dict_board[temp_pos], str):
                if self._dict_board[temp_pos].get_symbol() == "wK":
                    check_white_king = True
                if self._dict_board[temp_pos].get_symbol() == "bK":
                    check_black_king = True
        number -= 2

        temp_pos = chr(letter) + chr(number)
        if temp_pos in self._dict_board:
            if not isinstance(self._dict_board[temp_pos], str):
                if self._dict_board[temp_pos].get_symbol() == "wK":
                    check_white_king = True
                if self._dict_board[temp_pos].get_symbol() == "bK":
                    check_black_king = True

        # Next we move to get the three places to the left of the end_pos
        letter -= 1
        for place in range(3):
            temp_pos = chr(letter) + chr(number)

            if temp_pos in self._dict_board:
                if not isinstance(self._dict_board[temp_pos], str):
                    if self._dict_board[temp_pos].get_symbol() == "wK":
                        check_white_king = True
                    if self._dict_board[temp_pos].get_symbol() == "bK":
                        check_black_king = True
            number += 1

        # Finally we go to the three places to the right of the end pos
        letter = orig_letter + 1
        number = orig_number - 1
        for place in range(3):
            temp_pos = chr(letter) + chr(number)

            if temp_pos in self._dict_board:
                if not isinstance(self._dict_board[temp_pos], str):
                    if self._dict_board[temp_pos].get_symbol() == "wK":
                        check_white_king = True
                    if self._dict_board[temp_pos].get_symbol() == "bK":
                        check_black_king = True
            number += 1

        if check_black_king is True and check_white_king is True:
            return True
        else:
            return False


class Rook:
    """The Rook chess piece and its properties"""
    def __init__(self, color):
        self._color = color
        self._first_turn = True
        if color == "WHITE":
            self._symbol = "wr"
        if color == "BLACK":
            self._symbol = "br"

    def get_symbol(self):
        """Method to return the symbol of the piece"""
        return self._symbol

    def get_color(self):
        """Method to return the color of the piece"""
        return self._color

    def move(self, start_pos, end_pos, chess):
        """Method for a Rook to move. Will return True if it can reach the end_pos otherwise, it will return false"""
        start_letter = start_pos[0]
        start_number = start_pos[1]
        end_letter = end_pos[0]
        end_number = end_pos[1]
        temp_pos = None
        valid_move = True
        board = chess.get_dict_board()

        # First checks if the start_pos and end_pos are a straight line apart this is done by checking if either
        # the NUMBER or LETTER are the same for both points
        if start_letter == end_letter or start_number == end_number:
            # Logic for if the letters are equal
            if start_letter == end_letter:
                number_dif = abs(ord(end_number) - ord(start_number))

                # Logic if the piece is going UP as in a1 to a5 for example
                if ord(start_number) < ord(end_number):
                    number_place = ord(start_number) + 1

                    # Logic for if we are move only one space will always be true due to early conditionals
                    # accounting for moving on your own piece or off the map
                    if number_dif == 1:
                        return True

                    for move in range(number_dif):
                        temp_pos = start_letter + chr(number_place)
                        if move != number_dif - 1 and board[temp_pos] == "--":
                            pass
                        if move != number_dif - 1 and board[temp_pos] != "--":
                            valid_move = False

                        number_place += 1

                    if valid_move is True:
                        return True
                    if valid_move is False:
                        return False

                # Logic if the piece is going DOWN as in a5 to a1 for example
                if ord(start_number) > ord(end_number):
                    number_place = ord(start_number) - 1

                    # Logic for if we are move only one space will always be true due to early conditionals
                    # accounting for moving on your own piece or off the map
                    if number_dif == 1:
                        return True

                    for move in range(number_dif):
                        temp_pos = start_letter + chr(number_place)
                        if move != number_dif - 1 and board[temp_pos] == "--":
                            pass
                        if move != number_dif - 1 and board[temp_pos] != "--":
                            valid_move = False

                        number_place -= 1

                    if valid_move is True:
                        return True
                    if valid_move is False:
                        return False

            # Next is the same logic but if the numbers are equal and letters are changing up/down
            if start_number == end_number:
                letter_dif = abs(ord(end_letter) - ord(start_letter))

                # Logic if the piece is going RIGHT as in a1 to d1 for example
                if ord(start_letter) < ord(end_letter):
                    letter_place = ord(start_letter) + 1

                    # Logic for if we are move only one space will always be true due to early conditionals
                    # accounting for moving on your own piece or off the map
                    if letter_dif == 1:
                        return True

                    for move in range(letter_dif):
                        temp_pos = chr(letter_place) + start_number
                        if move != letter_dif - 1 and board[temp_pos] == "--":
                            pass
                        if move != letter_dif - 1 and board[temp_pos] != "--":
                            valid_move = False

                        letter_place += 1

                    if valid_move is True:
                        return True
                    if valid_move is False:
                        return False

                # Logic if the piece is going LEFT as in d5 to a5 for example
                if ord(start_letter) > ord(end_letter):
                    letter_place = ord(start_letter) - 1

                    # Logic for if we are move only one space will always be true due to early conditionals
                    # accounting for moving on your own piece or off the map
                    if letter_dif == 1:
                        return True

                    for move in range(letter_dif):
                        temp_pos = chr(letter_place) + start_number
                        if move != letter_dif - 1 and board[temp_pos] == "--":
                            pass
                        if move != letter_dif - 1 and board[temp_pos] != "--":
                            valid_move = False

                        letter_place -= 1

                    if valid_move is True:
                        return True
                    if valid_move is False:
                        return False

        else:
            return False


class Knight:
    """The Knight chess piece and its properties"""

    def __init__(self, color):
        self._color = color
        self._first_turn = True
        if color == "WHITE":
            self._symbol = "wk"
        if color == "BLACK":
            self._symbol = "bk"

    def get_symbol(self):
        """Method to return the symbol of the piece"""
        return self._symbol

    def get_color(self):
        """Method to return the color of the piece"""
        return self._color

    def move(self, start_pos, end_pos, chess):
        """ Move function for the Knight"""
        start_letter = start_pos[0]
        start_number = start_pos[1]
        end_letter = end_pos[0]
        end_number = end_pos[1]
        board = chess.get_dict_board()
        number_dif = abs(ord(end_number) - ord(start_number))
        letter_dif = abs(ord(end_letter) - ord(start_letter))

        # A knight must move either 2 vert 1 horizontal or 2 horizontal 1 vert to be a valid move
        # These conditionals will check if the movement is valid and if it ends on the board.
        if number_dif == 2 and letter_dif == 1:
            if end_pos in board:
                return True

        if letter_dif == 2 and number_dif == 1:
            if end_pos in board:
                return True

        # If the knight is not making a valid move return False
        return False


class Bishop:
    """The Bishop chess piece and its properties"""

    def __init__(self, color):
        self._color = color
        self._first_turn = True
        if color == "WHITE":
            self._symbol = "wb"
        if color == "BLACK":
            self._symbol = "bb"

    def get_symbol(self):
        """Method to return the symbol of the piece"""
        return self._symbol

    def get_color(self):
        """Method to return the color of the piece"""
        return self._color

    def move(self, start_pos, end_pos, chess):
        """ Movement method for the Bishop piece"""
        start_letter = start_pos[0]
        start_number = start_pos[1]
        end_letter = end_pos[0]
        end_number = end_pos[1]
        board = chess.get_dict_board()
        temp_pos = None
        number_dif = abs(ord(end_number) - ord(start_number))
        letter_dif = abs(ord(end_letter) - ord(start_letter))
        valid_move = True

        # Conditional that checks if the Bishop is moving in a diagonal line
        if number_dif == letter_dif:
            # Logic to check every space to make sure it is empty
            ord_number_place = ord(start_number)
            ord_letter_place = ord(start_letter)
            for move in range(number_dif + 1):
                temp_pos = chr(ord_letter_place) + chr(ord_number_place)
                if move == 0:
                    if ord(start_letter) < ord(end_letter) and ord(start_number) < ord(end_number):
                        ord_number_place += 1
                        ord_letter_place += 1

                    # If the bishop is moving towards the top left of the board
                    if ord(start_letter) > ord(end_letter) and ord(start_number) < ord(end_number):
                        ord_number_place += 1
                        ord_letter_place -= 1

                    # If the bishop is moving towards the bottom left of the board
                    if ord(start_letter) > ord(end_letter) and ord(start_number) > ord(end_number):
                        ord_number_place -= 1
                        ord_letter_place -= 1

                    # If the bishop is moving towards the bottom right of the board
                    if ord(start_letter) < ord(end_letter) and ord(start_number) > ord(end_number):
                        ord_number_place -= 1
                        ord_letter_place += 1
                else:
                    # if it is not the last move and the board space is empty pass
                    if move != number_dif and board[temp_pos] == "--":
                        pass
                    # if it is not the last move and the board space is filled then return invalid move
                    if move != number_dif and board[temp_pos] != "--":
                        valid_move = False

                    # Logic for determining next temp_pos for the next loop
                    # If the bishop is moving towards the top right of the board
                    if ord(start_letter) < ord(end_letter) and ord(start_number) < ord(end_number):
                        ord_number_place += 1
                        ord_letter_place += 1

                    # If the bishop is moving towards the top left of the board
                    if ord(start_letter) > ord(end_letter) and ord(start_number) < ord(end_number):
                        ord_number_place += 1
                        ord_letter_place -= 1

                    # If the bishop is moving towards the bottom left of the board
                    if ord(start_letter) > ord(end_letter) and ord(start_number) > ord(end_number):
                        ord_number_place -= 1
                        ord_letter_place -= 1

                    # If the bishop is moving towards the bottom right of the board
                    if ord(start_letter) < ord(end_letter) and ord(start_number) > ord(end_number):
                        ord_number_place -= 1
                        ord_letter_place += 1

            if valid_move is True:
                return True
            if valid_move is not True:
                return False
        else:
            return False


class Queen:
    """The Queen chess piece and its properties"""

    def __init__(self, color):
        self._color = color
        self._first_turn = True
        if color == "WHITE":
            self._symbol = "wQ"
        if color == "BLACK":
            self._symbol = "bQ"

    def get_symbol(self):
        """Method to return the symbol of the piece"""
        return self._symbol

    def get_color(self):
        """Method to return the color of the piece"""
        return self._color

    def move(self, start_pos, end_pos, chess):
        """ Move Function for the Queen """
        start_letter = start_pos[0]
        start_number = start_pos[1]
        end_letter = end_pos[0]
        end_number = end_pos[1]
        temp_pos = None
        valid_move = True
        board = chess.get_dict_board()
        number_dif = abs(ord(end_number) - ord(start_number))
        letter_dif = abs(ord(end_letter) - ord(start_letter))

        # Logic for Rook Movement copied to queen
        if start_letter == end_letter or start_number == end_number:
            # Logic for if the letters are equal
            if start_letter == end_letter:
                number_dif = abs(ord(end_number) - ord(start_number))

                # Logic if the piece is going UP as in a1 to a5 for example
                if ord(start_number) < ord(end_number):
                    number_place = ord(start_number) + 1

                    # Logic for if we are move only one space will always be true due to early conditionals
                    # accounting for moving on your own piece or off the map
                    if number_dif == 1:
                        return True

                    for move in range(number_dif):
                        temp_pos = start_letter + chr(number_place)
                        if move != number_dif - 1 and board[temp_pos] == "--":
                            pass
                        if move != number_dif - 1 and board[temp_pos] != "--":
                            valid_move = False

                        number_place += 1

                    if valid_move is True:
                        return True
                    if valid_move is False:
                        return False

                # Logic if the piece is going DOWN as in a5 to a1 for example
                if ord(start_number) > ord(end_number):
                    number_place = ord(start_number) - 1

                    # Logic for if we are move only one space will always be true due to early conditionals
                    # accounting for moving on your own piece or off the map
                    if number_dif == 1:
                        return True

                    for move in range(number_dif):
                        temp_pos = start_letter + chr(number_place)
                        if move != number_dif - 1 and board[temp_pos] == "--":
                            pass
                        if move != number_dif - 1 and board[temp_pos] != "--":
                            valid_move = False

                        number_place -= 1

                    if valid_move is True:
                        return True
                    if valid_move is False:
                        return False

            # Next is the same logic but if the numbers are equal and letters are changing up/down
            if start_number == end_number:
                letter_dif = abs(ord(end_letter) - ord(start_letter))

                # Logic if the piece is going RIGHT as in a1 to d1 for example
                if ord(start_letter) < ord(end_letter):
                    letter_place = ord(start_letter) + 1

                    # Logic for if we are move only one space will always be true due to early conditionals
                    # accounting for moving on your own piece or off the map
                    if letter_dif == 1:
                        return True

                    for move in range(letter_dif):
                        temp_pos = chr(letter_place) + start_number
                        if move != letter_dif - 1 and board[temp_pos] == "--":
                            pass
                        if move != letter_dif - 1 and board[temp_pos] != "--":
                            valid_move = False

                        letter_place += 1

                    if valid_move is True:
                        return True
                    if valid_move is False:
                        return False

                # Logic if the piece is going LEFT as in d5 to a5 for example
                if ord(start_letter) > ord(end_letter):
                    letter_place = ord(start_letter) - 1

                    # Logic for if we are move only one space will always be true due to early conditionals
                    # accounting for moving on your own piece or off the map
                    if letter_dif == 1:
                        return True

                    for move in range(letter_dif):
                        temp_pos = chr(letter_place) + start_number
                        if move != letter_dif - 1 and board[temp_pos] == "--":
                            pass
                        if move != letter_dif - 1 and board[temp_pos] != "--":
                            valid_move = False

                        letter_place -= 1

                    if valid_move is True:
                        return True
                    if valid_move is False:
                        return False

        # Bishop Movement Logic
        if number_dif == letter_dif:
            # Logic to check every space to make sure it is empty
            ord_number_place = ord(start_number)
            ord_letter_place = ord(start_letter)
            for move in range(number_dif + 1):
                temp_pos = chr(ord_letter_place) + chr(ord_number_place)
                if move == 0:
                    if ord(start_letter) < ord(end_letter) and ord(start_number) < ord(end_number):
                        ord_number_place += 1
                        ord_letter_place += 1

                    # If the bishop is moving towards the top left of the board
                    if ord(start_letter) > ord(end_letter) and ord(start_number) < ord(end_number):
                        ord_number_place += 1
                        ord_letter_place -= 1

                    # If the bishop is moving towards the bottom left of the board
                    if ord(start_letter) > ord(end_letter) and ord(start_number) > ord(end_number):
                        ord_number_place -= 1
                        ord_letter_place -= 1

                    # If the bishop is moving towards the bottom right of the board
                    if ord(start_letter) < ord(end_letter) and ord(start_number) > ord(end_number):
                        ord_number_place -= 1
                        ord_letter_place += 1
                else:
                    # if it is not the last move and the board space is empty pass
                    if move != number_dif and board[temp_pos] == "--":
                        pass
                    # if it is not the last move and the board space is filled then return invalid move
                    if move != number_dif and board[temp_pos] != "--":
                        valid_move = False

                    # Logic for determining next temp_pos for the next loop
                    # If the bishop is moving towards the top right of the board
                    if ord(start_letter) < ord(end_letter) and ord(start_number) < ord(end_number):
                        ord_number_place += 1
                        ord_letter_place += 1

                    # If the bishop is moving towards the top left of the board
                    if ord(start_letter) > ord(end_letter) and ord(start_number) < ord(end_number):
                        ord_number_place += 1
                        ord_letter_place -= 1

                    # If the bishop is moving towards the bottom left of the board
                    if ord(start_letter) > ord(end_letter) and ord(start_number) > ord(end_number):
                        ord_number_place -= 1
                        ord_letter_place -= 1

                    # If the bishop is moving towards the bottom right of the board
                    if ord(start_letter) < ord(end_letter) and ord(start_number) > ord(end_number):
                        ord_number_place -= 1
                        ord_letter_place += 1

            if valid_move is True:
                return True
            if valid_move is not True:
                return False
        else:
            return False


class King:
    """The King chess piece and its properties"""

    def __init__(self, color):
        self._color = color
        self._first_turn = True
        if color == "WHITE":
            self._symbol = "wK"
        if color == "BLACK":
            self._symbol = "bK"

    def get_symbol(self):
        """Method to return the symbol of the piece"""
        return self._symbol

    def get_color(self):
        """Method to return the color of the piece"""
        return self._color

    def move(self, start_pos, end_pos, chess):
        """ Move function for the King"""
        start_letter = start_pos[0]
        start_number = start_pos[1]
        end_letter = end_pos[0]
        end_number = end_pos[1]
        board = chess.get_dict_board()
        number_dif = abs(ord(end_number) - ord(start_number))
        letter_dif = abs(ord(end_letter) - ord(start_letter))

        # If the king is trying to move more than one spot
        if number_dif > 1 or letter_dif > 1:
            return False

        # The king cannot capture any targets
        if board[end_pos] != "--":
            return False

        if board[end_pos] == "--":
            return True


class Pawn:
    """The Pawn chess piece and its properties"""

    def __init__(self, color):
        self._color = color
        self._first_turn = True
        if color == "WHITE":
            self._symbol = "wp"
        if color == "BLACK":
            self._symbol = "bp"

    def get_symbol(self):
        """Method to return the symbol of the piece"""
        return self._symbol

    def get_color(self):
        """Method to return the color of the piece"""
        return self._color

    def move(self, start_pos, end_pos, chess):
        """ Move function for the Pawn"""
        start_letter = start_pos[0]
        start_number = start_pos[1]
        end_letter = end_pos[0]
        end_number = end_pos[1]
        temp_pos = None
        valid_move = True
        board = chess.get_dict_board()
        two_kings_in_explosions = chess.check_for_two_kings(end_pos)

        # First check if the Pawn is going straight
        if start_letter == end_letter:
            number_dif = abs(ord(end_number) - ord(start_number))

            # Next we will determine if the pawn is going in the correct direction based on its color
            # This conditional will check if the pawn is white and going upwards
            if board[start_pos].get_color() == "WHITE" and ord(start_number) < ord(end_number):
                # if pawn tries to move more than two spots ever return false
                if number_dif > 2:
                    return False

                # If the pawn tries to move two spaces, but it is not its first turn return false
                if number_dif == 2 and self._first_turn is not True:
                    return False

                # If the pawn moves two spaces, but it also is its first turn
                if number_dif == 2 and self._first_turn is True:
                    number_place = ord(start_number) + 1
                    for move in range(number_dif):
                        temp_pos = start_letter + chr(number_place)
                        if board[temp_pos] == "--":
                            pass
                        else:
                            valid_move = False
                        number_place += 1

                # If the pawn moves only 1 space check the forward space. If it is empty do nothing otherwise
                # invalidate the move
                if number_dif == 1:
                    number_place = ord(start_number) + 1
                    temp_pos = start_letter + chr(number_place)
                    if board[temp_pos] == "--":
                        pass
                    else:
                        valid_move = False

            # If the pawn tries to move backwards
            if board[start_pos].get_color() == "WHITE" and ord(start_number) > ord(end_number):
                return False

            # This conditional will check if the pawn is black and going downwards
            if board[start_pos].get_color() == "BLACK" and ord(start_number) > ord(end_number):
                # if pawn tries to move more than two spots ever return false
                if number_dif > 2:
                    return False

                # If the pawn tries to move two spaces, but it is not its first turn return false
                if number_dif == 2 and self._first_turn is not True:
                    return False

                # If the pawn moves two spaces, but it also is its first turn
                if number_dif == 2 and self._first_turn is True:
                    number_place = ord(start_number) - 1
                    for move in range(number_dif):
                        temp_pos = start_letter + chr(number_place)
                        if board[temp_pos] == "--":
                            pass
                        else:
                            valid_move = False
                        number_place -= 1

                # If the pawn moves only 1 space check the forward space. If it is empty do nothing otherwise
                # invalidate the move
                if number_dif == 1:
                    number_place = ord(start_number) - 1
                    temp_pos = start_letter + chr(number_place)
                    if board[temp_pos] == "--":
                        pass
                    else:
                        valid_move = False

            # If the Pawn tries to move backwards
            if board[start_pos].get_color() == "BLACK" and ord(start_number) < ord(end_number):
                return False

            # Final return on straight line movement
            if valid_move is True:
                if two_kings_in_explosions is True and board[end_pos] != "--":
                    return False
                else:
                    self._first_turn = False
                    return True

            if valid_move is False:
                return False

        # Logic for if the pawn is moving at a diagonal not straight up or down
        else:
            number_dif = abs(ord(end_number) - ord(start_number))
            letter_dif = abs(ord(end_letter) - ord(start_letter))

            if board[start_pos].get_color() == "WHITE" and ord(start_number) < ord(end_number):
                # Logic to check for an even diagonal that is only a length of one
                if number_dif == letter_dif and number_dif == 1:
                    # If the end_pos is not empty then the move is a valid capture
                    if board[end_pos] != "--" and two_kings_in_explosions is False:
                        self._first_turn = False
                        return True

                    if board[end_pos] == "--":
                        return False

            if board[start_pos].get_color() == "BLACK" and ord(start_number) > ord(end_number):
                # Logic to check for an even diagonal that is only a length of one
                if number_dif == letter_dif and number_dif == 1:
                    # If the end_pos is not empty then the move is a valid capture
                    if board[end_pos] != "--" and two_kings_in_explosions is False:
                        self._first_turn = False
                        return True

                    if board[end_pos] == "--":
                        return False

            return False


# def main():
#     game = ChessVar()
#     print(game.make_move('d2', 'd4'))  # output True
#     print(game.make_move('g7', 'g5'))  # output True
#     print(game.make_move('c1', 'g5'))  # output True
#     game.print_board()
#     print(game.get_game_state())  # output UNFINISHED
#
#
# if __name__=="__main__":
#     main()