"""
name: exceptions.py

purpose: a module for the exceptions of the battleship game

author: bis-hanich-8

changelog:
    created: 29/12/2020
"""


class BattleShipException(Exception):
    """
    A base class for all battle ship exceptions
    """
    pass


class ConnectionNotInitializedError(BattleShipException):
    """
    A class for trying to use a connection that hasn't been initialized
    """
    pass


class GameEnd(BattleShipException):
    """
    An exception for when the game is over
    """
    pass
