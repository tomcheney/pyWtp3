import struct
from enum import Enum


class MessageType(Enum):
    UNKNOWN = 0
    HEARTBEAT = 1
    VARIABLE_MAP = 20
    VARIABLE_DATA = 30
    MOB_EVENT = 40
    MOB_DATA = 50


class Message():
    def __init__(self, msg_type: MessageType):
        self.msg_type = msg_type


class VariableMapMessage(Message):
    def __init__(self, data):
        super().__init__(MessageType.VARIABLE_MAP)
        self._data = data
        i = 0
        size = 12
        length = len(data)
        self.vars = {}
        while i < (length-size):
            var_data = data[i:i+1+size]
            var_id = struct.unpack('>H', var_data[0:2])[0]
            var_name  = var_data[2:11].decode("utf-8")
            self.vars[var_id] = var_name
            i = i + size


class DataMessage(Message):
    def __init__(self, data):
        super().__init__(MessageType.VARIABLE_DATA)
        self._data = data
        length = len(data)

        i = 0
        size = 6
        self.vars = {}
        while i < (length - size - 8):
            var_data = data[i:i+1+size]
            var_id = struct.unpack('>H', var_data[0:2])[0]
            var_value = struct.unpack('>f', var_data[2:6])[0]
            self.vars[var_id] = var_value
            i = i + size


class MessageHeader():
    valid = False

    def __init__(self, data):
        self.valid = data[0] == 0x55 and data[1] == 0xAA
        try:
            self.msg_type = MessageType(data[2])
        except ValueError as e:
            print(e)
            self.msg_type = MessageType.UNKNOWN

        ts_bytes = data[3:7]
        self.timestamp = struct.unpack('>I', ts_bytes)[0]
        self.msg_length = struct.unpack('>H', data[7:9])[0]
