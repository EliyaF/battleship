"""
name: tcp_connection.py

purpose: a class for the tcp connection of the battleship game

author: bis-hanich-8

changelog:
    created: 29/12/2020
"""

import socket

from excpetions import ConnectionNotInitializedError

MY_IP = ''
PORT = 12346


class TcpConnection:
    """
    A class for the tcp connections
    """

    def __init__(self):
        self._socket = None

    def wait_for_connection(self):
        """
        Wait for another player to start the connection
        :return: None
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
            listening_socket.bind((MY_IP, PORT))
            listening_socket.listen(1)
            self._socket, _ = listening_socket.accept()

    def start_connection(self, ip: str):
        """
        Start a connection with a waiting server
        :param ip: the ip of the waiting server
        :return: None
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip, PORT))

    def recv(self, bytes_len: int):
        """
        receive bytes from the internet
        :param bytes_len: the length of the bytes to recv
        :return: the bytes received
        :rtype : list
        """
        if self._socket is None:
            raise ConnectionNotInitializedError("Tried to receive from non initialized socket")
        else:
            return self.recv(bytes_len)

    def send(self, bytes_to_send: list):
        """
        send bytes through the connections
        :param bytes_to_send: the bytes to send
        :return: None
        """
        if self._socket is None:
            raise ConnectionNotInitializedError("Tried to send to non initialized socket")
        else:
            self._socket.sendall(bytes_to_send)
