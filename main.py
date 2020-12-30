"""
name: main.py

purpose: the main module to connect all of the classes and run the game

author: bis-hanich-8

changelog:
    created: 29/12/2020
"""

from tcp_connection import TcpConnection
from protocol_manager import ProtocolManager
from board_io import BoardIO
from game_manager import GameManager
from battle_ship import BattleShip


def get_tcp_connection():
    """
    Get the tcp connection. decide if to be the server according to the user
    :return: the tcp connection
    :rtype: TcpConnection
    """
    if input("Are you the server?") == 'y':
        return TcpConnection()
    else:
        return TcpConnection(input("Enter IP: "))


def main():
    """
    Run the main logic of connecting the classes
    :return: None
    """
    tcp_connection = get_tcp_connection()
    protocol_manager = ProtocolManager(tcp_connection)
    board_io = BoardIO()
    game_manager = GameManager(board_io)
    battle_ship = BattleShip(protocol_manager, game_manager)
    battle_ship.play_game()


if __name__ == '__main__':
    main()
