"""
name: protocol_manager.py

purpose: a class for managing the battle-ship protocol

author: bis-hanich-8

changelog:
    created: 29/12/2020
"""

from tcp_connection import TcpConnection
import struct
from collections import namedtuple

BYTES_LEN = 9

BytesDataTuple = namedtuple("BytesDataTuple",
                            "game_begin, finished_putting_ships, is_attack, attack_row, attack_column, is_attack_answer, attack_answer, game_end, error",
                            defaults=[0] * BYTES_LEN)


class ERRORS:
    MORE_THAN_ONE_EXISTS = 1
    INVALID_POSITION = 2
    DID_HIT_BIGGER_THAN_2 = 3
    GAME_BEGIN_BAD_TIME = 4
    FINISHED_PUTTING_BOATS_BAD_TIME = 5
    ATTACK_NOT_AT_TURN = 6
    REPLY_TO_ATTACK_NOT_AT_TURN = 7


class ProtocolManager:
    """
    A class for managing the battle-ship protocol
    """

    def __init__(self, tcp_connection: TcpConnection):
        """
        Initilize the class
        :param tcp_connection: a TcpConnection that has been initialized
        """
        self._tcp_connection = tcp_connection

    def send_guess(self, guess: tuple):
        """
        Send a guess to attack the other player's battleships
        :param guess: the guess of where to attack
        :return: None
        """
        self._tcp_connection.send(
            self._pack_messgae(BytesDataTuple(is_attack=True, attack_row=guess[0], attack_column=guess[1])))

    def get_guess_reply(self):
        """
        get the status of the guess
        :return: the group of hit/sink/won
        :rtype: tuple
        """
        guess_reply = self.unpack_message(self._tcp_connection.recv(BYTES_LEN))
        return guess_reply.attack_answer >= 1, guess_reply.attack_answer == 2, guess_reply.game_end

    def get_guess(self):
        """
        get the other player's guess
        :return: the other player's guess
        :rtype: the coordination of the guess
        :rtype: tuple
        """
        guess = self.unpack_message(self._tcp_connection.recv(BYTES_LEN))
        return guess[3], guess[4]

    def send_guess_reply(self, reply: tuple):
        """
        send the other player a guess reply
        :param reply: the reply to send
        :return: None
        """
        self._tcp_connection.send(
            self._pack_messgae(
                BytesDataTuple(is_attack_answer=True, attack_answer=reply[0] + reply[1], game_end=reply[2])))

    def ready_to_start(self):
        """
        synchronize with the other player that we are ready to start
        :return: True if it is our turn
        :rtype : bool
        """
        if not self._tcp_connection.is_server():
            start_request = self._tcp_connection.recv(BYTES_LEN)
        self._tcp_connection.send(self._pack_messgae(BytesDataTuple(finished_putting_ships=True)))
        if self._tcp_connection.is_server():
            start_reply = self._tcp_connection.recv(BYTES_LEN)
            return False
        return True

    def play_game(self):
        """
        start the game
        :return: None
        """
        if self._tcp_connection.is_server():
            self._get_start_request()
        self._tcp_connection.send(self._pack_messgae(BytesDataTuple(game_begin=True)))
        if not self._tcp_connection.is_server():
            self._get_start_request()

    def send_error(self, error_num: int):
        """
        send an error
        :param error_num: the number of the error to send
        :return: None
        """
        self._tcp_connection.send(self._pack_messgae(BytesDataTuple(error=error_num)))

    def _pack_messgae(self, bytes_tuple: BytesDataTuple):
        """
        pack a messgae according to the protocol, with the default args of 0
        :param bytes_tuple: the tuple of bytes to send
        :return: the packed message in bytes
        :rtype : bytes
        """
        return struct.pack("b" * BYTES_LEN, *bytes_tuple)

    def unpack_message(self, message: bytes):
        """
        get the tuple of values from the message
        :param message: the message in bytes
        :return: the tuple of values
        :rtype : BytesDataTuple
        """
        return BytesDataTuple(*struct.unpack("b" * BYTES_LEN, message))

    def _get_start_request(self):
        start_request = self._tcp_connection.recv(BYTES_LEN)
        while not self._check_legal_reply(self.unpack_message(start_request)):
            start_request = self._tcp_connection.recv(BYTES_LEN)

    def _check_legal_reply(self, answer: BytesDataTuple):
        count = 0
        count += answer.game_begin != 0
        count += answer.finished_putting_ships != 0
        count += answer.is_attack != 0
        count += answer.is_attack_answer != 0
        if count != 1:
            self._tcp_connection.send(self._pack_messgae(BytesDataTuple(error=ERRORS.MORE_THAN_ONE_EXISTS)))
            return False
        return True
