import threading
import socket 


class clientConnection(threading.Thread):
    def __init__(self, conn, addr):
        super(clientConnection, self).__init__()
        
        #variables
        self.addr, self.conn = addr, conn
        
        #temporary variables
        self.client_logged_in = False
        
    def handle_login(self):
        pass
        
    def run(self):
        status = self.conn.recv(4098).decode('utf-8')
        