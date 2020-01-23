from datetime import datetime
from WTP import WtpClient

def on_data(dt: datetime, data):
    print(dt, data)

if __name__ == '__main__':
    ip_address = '192.168.91.102'
    wtp = WtpClient(tcp_address=ip_address)
    wtp.datastore.set_on_data_callback(on_data)
    wtp.start()

    running = True
    while running:
        pass
