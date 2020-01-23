from datetime import datetime, timedelta
from .message import DataMessage, VariableMapMessage, MessageHeader

class DataStore():
    def __init__(self):
        self.__var_names = {}
        self.__var_values = {}
        self.__on_data_cb = None
        self.__previous_timestamp = None
        self.__duplicate_count = 0

    def on_data_msg(self, msg: DataMessage, header: MessageHeader):
        for var_id, var_value in msg.vars.items():
            self.__var_values[var_id] = var_value

        dt = datetime.fromtimestamp(header.timestamp)
        data = {name: self.__var_values[var_id] for var_id, name in self.__var_names.items()}
        
        # This is a workaround for 5hz data arriving with a one second resolution timestamp
        if self.__previous_timestamp is not None:
            if self.__previous_timestamp == header.timestamp:
                self.__duplicate_count = self.__duplicate_count + 1
                dt = dt + timedelta(seconds=self.__duplicate_count*0.2)
            else:
               self.__duplicate_count = 0
        self.__previous_timestamp = header.timestamp
        
        if self.__on_data_cb:
            self.__on_data_cb(dt, data)

    def on_map_msg(self, msg: VariableMapMessage):
        for var_id, var_name in msg.vars.items():
            self.__var_names[var_id] = var_name

    def set_on_data_callback(self, cb_fun):
        self.__on_data_cb = cb_fun

    def var_names(self):
        return dict(self.__var_names)
