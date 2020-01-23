from WTP import DataStore, TcpClient, MulticastClient

if __name__ == '__main__':
    datastore = DataStore()
    tcp_client = TcpClient(datastore)
    tcp_client.start()
    udp_client = MulticastClient(datastore)
    udp_client.start()
    udp_client.join()


class WtpClient():
    def __init__(self, tcp_address: str, tcp_port: int=5605, multicast_group: str='234.2.2.2', multicast_port: int=5604):
        self.datastore = DataStore()
        self.__tcp_client = TcpClient(self.datastore, tcp_address, tcp_port)
        self.__udp_client = MulticastClient(self.datastore, multicast_group, multicast_port)

    def start(self):
        self.__tcp_client.start()
        self.__udp_client.start()
        self.__udp_client.join()
