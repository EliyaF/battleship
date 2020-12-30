"""
name: battle_ship.py

purpose: the main class for connecting the game and the protocol

author: bis-hanich-8

changelog:
    created: 30/12/2020
"""

from protocol_manager import ProtocolManager
from game_manager import GameManager
from excpetions import GameEnd

class BattleShip:
    """
    A main class for connecting the game and the protocol
    """

    def __init__(self, protocol_manager: ProtocolManager, game_manager: GameManager):
        """
        Initialize the battle ship classes
        :param protocol_manager: the protocol manager
        :param game_manager: the game manager
        """
        self._protocol_manager = protocol_manager
        self._game_manager = game_manager

    def play_game(self):
        """
        Play the game
        :return: None
        """
        self._protocol_manager.play_game()
        self._game_manager.initialize_board()
        my_turn = self._protocol_manager.ready_to_start()
        game_over = False
        try:
            while True:
                if my_turn:
                    guess = self._game_manager.get_next_guess()
                    self._protocol_manager.send_guess(guess)
                    answer = self._protocol_manager.get_guess_reply()
                    self._game_manager.set_answer(guess, answer)
                else:
                    answer = self._game_manager.attack(self._protocol_manager.get_guess())
                    self._protocol_manager.send_guess_reply(answer)
                if not answer[0]:
                    my_turn = not my_turn
        except GameEnd:
            print("Game over!")
