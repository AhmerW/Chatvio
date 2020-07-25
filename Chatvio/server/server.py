import os
import socket 
import random
import logging 
import threading
from string import ascii_lowercase
try:
    from .database import db
except ImportError:
    # This server is meant to be started from the __main__.py file
    # if it's started correctly then the importerror will  not get raised,
    # unless if someone decide to directly start it from server.py
    # which in that case the above imports will not work.
    from database import db

## set up some basic logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
_format = \
"""
%(levelname)s at %(asctime)s, in %(filename)s - %(module)s, %(funcName)s (%(lineno)d)
: %(message)s \n
"""
handler.setFormatter(logging.Formatter(_format, datefmt="%d-%b-%y %H:%M:%S"))
handler.setLevel(logging.DEBUG)
logging.root.setLevel(logging.DEBUG)
logger.addHandler(handler)

CHOICES : list = list(ascii_lowercase)

class Holder(object):
    clients : list = [] # all the connected clients
    meetings : dict = {} #current meetings. all values are list and first index is host.

    
    @staticmethod 
    def generateId(length = 6):
        _id = ''.join([
            random.choice(CHOICES) for _ in range(length)
        ])
        if not _id in Holder.meetings:
            return _id
        Holder.generateId()
        
class Server(object):
    def __init__(self, ip : str = "localhost", port : int = 8998):
        self.ip, self.port = ip, port
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        
        self.server_running = True
        
        #instances 
        self.db = db.db()
        
        #dynamic vars
        self.total_clients = 0

      
        
    def start(self):
        logger.warning("Server is now listening on ({0.ip}, {0.port})! Clients are able to connect!".format(self))
        self.server.listen()
        while self.server_running:
            try:
                conn, addr = self.server.accept()
                if conn not in Holder.clients:
                    Holder.clients.append(conn)
                    self.total_clients += 1
                    
                self.db.add_connection(conn)
                connection = ClientConnection(conn, addr)
                connection.start()
            except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
                if conn in Holder.clients:
                    Holder.clients.remove(conn)
                    self.total_clients -= 1
            except Exception as e:
                print("error: ", e)
                logger.debug(e)
                
                
class ClientConnection(threading.Thread):
    def __init__(self, conn, addr):
        super(ClientConnection, self).__init__()
        
        #variables
        self.con, self.adr = conn, addr
        

        #client variables
        self.connected = True
        
        self.name = ""
        self.logged_in = False 
        self.host_id = 0
        
        
    def sendToAll(self, aclient, _id, msg):
        for client in Holder.meetings[_id]:
            if client != aclient:
                client.send(bytes(msg, 'utf-8'))
        
    def handleLogin(self):
        pass
    
    def processRequest(self, req, *args):
        if args:
            args = args[0]
        if req == 'validateid':
            status = 'true' if args[0] in Holder.meetings else 'false'
            self.con.send(bytes(status, 'utf-8'))
            return
        if req.endswith('meeting'):
            req = req.split('_')[0].lower()
            if req == 'create':
                meeting_id = Holder.generateId()
                Holder.meetings[meeting_id] = [self.con] 
                print(f"Created meeting with {args}")
                
            elif req == 'join':
                try:
                    _id = args[0]
                    self.con.send(bytes('true', 'utf-8'))
                    Holder.meetings[_id].append(self.con)
                    print(f"joined meeting with id {_id}")
                except Exception as e:
                    print(e)
                    self.con.send(bytes('false', 'utf-8'))
            
            elif req == 'leave':
                try:
                    _id = args[0]
                    Holder.meetings[_id].remove(self.con) 
                    self.con.send(bytes('true', 'utf-8'))
                    print(f"Left meeting with id {_id}")
                except Exception as e:
                    print(e)
                    self.con.send(bytes('false', 'utf-8'))
            
            elif req == 'end':
                pass
        
        elif req.endswith('member'):
            pass
    
    def receiveRequest(self):
        """
        Receives a request from the client and
        processes that request
        valid requests are:
            (
                create_meeting,
                join_meeting,
                leave_meeting,
                end_meeting,
                kick_member,
                invite_member,
                ...
            )
        """
        try:
            request = self.con.recv(4080).decode('utf-8')
            status = self.con.recv(4080).decode('utf-8')
            if request.startswith('/c/'):
                request = request[3::]
            if status.startswith('/c/'):
                status = status[3::]
            print(f'Received: {request} and {status}')
            self.processRequest(request, status.split('|'))
        except ConnectionError:
            self.connected = False 
            return
        
    def run(self):
        status = self.con.recv(4080).decode('utf-8').split('/')
        for value in status:
            if value.startswith('username'):
                self.name = value.split(':')[-1]
            elif value.startswith('logged_in'):
                _status = value.split(':')[-1]
                self.logged_in = True if _status.lower() == 'true' else False
        while self.connected:
            self.receiveRequest()