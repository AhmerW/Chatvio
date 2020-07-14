#main client
import socket 
import threading

from time import sleep

class client(object):
    def __init__(self, ip : str = "localhost", port : int = 8998):
        self.ip, self.port = ip, port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.connected = False
        self.sent_first = False
        
        self.command_seperator = r'/c/'
    
    def get_command(self, cmd):
        return "{0.command_seperator}{1}".format(self, str(cmd).lower().strip())
        
    def send_command(self, cmd, *args):
        if not self.connected:
            return 
        self.connection.send(bytes(self.get_command(cmd), 'utf-8'))
        
    def attempt_connect(self):
        try:
            self.connection.connect((self.ip, self.port))
            return True
        except:
            return False
    
    def start(self):
        print("Trying to connect to server on {0.ip}, {0.port}".format(self))
        while not self.connected:
            if self.attempt_connect():
                break
            else:
                print("Failed to connect, retrying..")
                sleep(2)
        print("Successfully connected to the server on {0.ip}, {0.port}!".format(self))
        
if __name__ == "__main__":
    clientObj = client()
    clientObj.start()