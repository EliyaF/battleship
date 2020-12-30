"""
name: game_manager.py

purpose: a class for managing the battle-ship game

author: bis-hanich-8

changelog:
    created: 30/12/2020
"""

from board_io import BoardIO

SHIP_SIZES = (2, 3, 3, 4, 5)
BOARD_SIDE_SIZE = 10


class GameManager:
    """
    A class to manage the game
    """

    def __init__(self, board_io: BoardIO):
        self._board_io = board_io
        self._ships = None

    def initialize_board(self):
        """
        Get the user to initialize the board
        :return: None
        """
        board = self._board_io.get_board()
        self._ships = []
        for i in range(len(SHIP_SIZES)):
            ship = []
            for j in range(SHIP_SIZES[i]):
                new_point = list(board[i][0])
                if board[i][1]:
                    new_point[0] += j
                else:
                    new_point[1] += j
                ship.append([tuple(new_point), True])
            self._ships.append(ship)

    def get_next_guess(self):
        """
        Get the next guess from the user
        :return: A tuple of the point
        :rtype: tuple
        """
        return self._board_io.get_guess()

    def set_answer(self, guess: tuple, answer: tuple):
        """
        set the answer to the user's guess
        :param guess: the previous user's guess
        :param answer: the answer recived
        :return: None
        """
        self._board_io.set_guess_answer(guess, answer)

    def attack(self, guess: tuple):
        """
        Attack the player's battleship
        :param guess: the other player's guess
        :return: the answer
        :rtype: tuple
        """
        for ship in self._ships:
            for place in ship:
                if guess == place[0]:
                    place[1] = False
                    answer = (True, self._is_ship_sunk(ship), self._is_game_over())
                    self._board_io.get_attacked(guess, answer)
                    return answer

        answer = (False, False, False)
        self._board_io.get_attacked(guess, answer)
        return answer

    def _is_ship_sunk(self, ship):
        """
        Check if a ship is sunk
        :param ship: the ship to check
        :return: True if it is sunk
        :rtype : bool
        """
        for place in ship:
            if place[1]:
                return False
        return True


    def _is_game_over(self):
        """
        Check if the game is over (all of the ships are sunk)
        :return: True if the game is over
        :rtype : bool
        """
        for ship in self._ships:
            for place in ship:
                if place[1]:
                    return False
        return True
