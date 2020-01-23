import socket
import struct
import binascii
import sys
from threading import Thread
from enum import Enum

from .message import MessageType, MessageHeader, DataMessage, VariableMapMessage
from .datastore import DataStore


class WtpClient(Thread):
    def __init__(self, datastore: DataStore):
            super().__init__()
            self.datastore = datastore


class MulticastClient(WtpClient):
    def __init__(self, datastore: DataStore, multicast_group: str, port: int):
        super().__init__(datastore)
        IS_ALL_GROUPS = True
        # Create the socket
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to the server address
        self.__sock.bind((multicast_group, port))

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('=4sl', group, socket.INADDR_ANY)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            data, address = self.__sock.recvfrom(10240)
            header = MessageHeader(data[0:9])
            if header.msg_type == MessageType.VARIABLE_DATA:
                message = DataMessage(data[9:10+header.msg_length])
                self.datastore.on_data_msg(message, header)
            

    def stop(self):
        self.running = False


class TcpClient(WtpClient):
    def __init__(self, datastore: DataStore, ip_address: str, port: int):
        super().__init__(datastore)
        # Create a TCP/IP socket
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        self.__sock.connect((ip_address, port))
        self.running = False

    def run(self):
        self.running = True
        count = 0
        while self.running:
            data = self.__sock.recv(10240)
            header = MessageHeader(data[0:9])
            if header.msg_type == MessageType.VARIABLE_MAP:
                message = VariableMapMessage(data[9:10+header.msg_length])
                self.datastore.on_map_msg(message)
