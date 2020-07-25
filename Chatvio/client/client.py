#main client
import ssl
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
    
    def getCommand(self, cmd):
        return "{0.command_seperator}{1}".format(self, str(cmd).lower().strip())
        
    def sendCommand(self, cmd, *args):
        print(f"Sending command {cmd}, {args}")
        if not self.connected:
            return 
        self.connection.send(bytes(self.getCommand(cmd), 'utf-8'))
        if not args:
            args = ['none']
        else:
            args = args[0]
            args = [str(arg) for arg in args]
        self.connection.send(
            bytes(
                self.getCommand('|'.join(args)),
                'utf-8'
            )
        )
        
        result = self.connected.recv(4080).decode('utf-8')
        return result
        
    def attemptConnect(self):
        try:
            self.connection.connect((self.ip, self.port))
            return True
        except:
            return False
    
    def start(self):
        print("Trying to connect to server on {0.ip}, {0.port}".format(self))
        while not self.connected:
            if self.attemptConnect():
                break
            else:
                print("Failed to connect, retrying..")
                sleep(2)
        self.connected = True 
        print("Successfully connected to the server on {0.ip}, {0.port}!".format(self))
        
if __name__ == "__main__":
    clientObj = client()
    clientObj.start()