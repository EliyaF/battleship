"""
name: board_io.py

purpose: a class for managing the io of the game

author: bis-hanich-8

changelog:
    created: 30/12/2020
"""

SHIPS_COUNT = 5


class BoardIO:
    """
    A class for the input-output of the battleship board
    """

    def get_board(self):
        """
        Get the board from the user
        :return: a list of tuples of points and if they are down or sideways
        """
        ships = [((int(input("enter row: ")), int(input("enter column: "))), input("is down: ") == 'y') for i in
                 range(SHIPS_COUNT)]
        return ships

    def get_attacked(self, position, answer):
        """
        Print an attack that happend
        :param position: the position of the attack
        :param answer: the answer of the attack
        :return: None
        """
        print(f"position {position} has been attacked!")
        print(f"hit: {answer[0]}, sink: {answer[1]}")
        if answer[2]:
            print("Game over! you lose...")

    def get_guess(self):
        """
        Get a guess of where to attack next from the user
        :return: a tuple of the position
        :rtype : None
        """
        return int(input("enter row to attack: ")), int(input("enter column to attack: "))

    def set_guess_answer(self, guess, answer):
        """
        show the user the answer to his guess
        :param guess: the guess he guessed
        :param answer: the answer to the guess
        :return: None
        """
        print(f"you guessed {guess}:")
        print(f"hit: {answer[0]}, sink: {answer[1]}")
        if answer[2]:
            print("Game over! you win...")
