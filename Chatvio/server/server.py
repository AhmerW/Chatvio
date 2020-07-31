import os
import socket 
import random
import threading
from string import ascii_lowercase

if __name__ == "__main__":
    from database import db 
else:
    from .database import db


CHOICES : list = list(ascii_lowercase)

class Holder(object):
    clients : list = [] # all the connected clients
    meetings : dict = {
        'meeting_id': {
            'participants': [],
            'participantNames': [],
            'canJoin': True
        }
    } 

    @classmethod
    def generateId(cls, length = 6) -> str:
        _id = ''.join(
            random.choice(CHOICES) for _ in range(length)
        )
        if _id not in cls.meetings:
            return _id
        cls.generateId()
        
class Server(object):
    def __init__(self, ip : str = "localhost", port : int = 8998) -> None:
        self.ip, self.port = ip, port
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        
        self.server_running = True
        
        #Database instance
        self.db = db.db()
        
        #Total clients
        self.total_clients = 0

      
        
    def start(self) -> None:
        print("Server is now listening on ({0.ip}, {0.port})! Clients are able to connect!".format(self))
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
            except ConnectionError:
                if conn in Holder.clients:
                    Holder.clients.remove(conn)
                    self.total_clients -= 1
            except Exception as e:
                print("error: ", e)
                
                
class ClientConnection(threading.Thread):
    def __init__(self, conn, addr):
        super(ClientConnection, self).__init__()
        
        #variables
        self.con, self.adr = conn, addr
        self.command_seperator = '/c/'
        
        #client variables
        self.connected = True
        self.streaming = False
        
        self.name = ""
        self.logged_in = False 
        self.meeting_id = 0
        
        
    def sendToAll(self, _id, msg):
        for client in Holder.meetings[_id]['participants'][1::]:
            print("sending to someone")
            client.send(bytes(msg, 'utf-8'))
        
    def handleLogin(self):
        pass
    
    def processRequest(self, req, *args):
        if args: args = args[0]
        if req == 'validateid':
            status = 'true' if args[0] in Holder.meetings else 'false'
            self.con.send(bytes(status, 'utf-8'))
            return
        if req.endswith('meeting'):
            req = req.split('_')[0].lower()
            if req == 'create':
                self.meeting_id = Holder.generateId()

                Holder.meetings[self.meeting_id] = {'participants' : [self.con], 
                                                    'participantNames': [self.name],
                                                    'canJoin': True
                                                   }
                
                print(f"Created meeting with id {self.meeting_id}")
                self.con.send(bytes(f'true,{self.meeting_id}', 'utf-8'))
            elif req == 'join':
                try:
                    _id = args[0]
                    Holder.meetings[_id]['participants'].append(self.con)
                    Holder.meetings[_id]['participantNames'].append(self.name)
                    
                    self.con.send(bytes('true', 'utf-8'))
                    print(f"joined meeting with id {_id}")
                except Exception as e:
                    print(e)
                    self.con.send(bytes('false', 'utf-8'))
            elif req == 'leave':
                try:
                    _id = args[0]
                    Holder.meetings[_id]['participants'].remove(self.con)
                    Holder.meetings[_id]['participantNames'].remove(self.name) 
                    
                    self.con.send(bytes('true', 'utf-8'))
                    print(f"Left meeting with id {_id}")
                except Exception as e:
                    print(e)
                    self.con.send(bytes('false', 'utf-8'))
            
            elif req == 'end':
                try:
                    print("Meeting ended")
                    _id = args[0]
                   #  self.sendToAll(_id, f"{self.command_seperator}meeting_ended")
                    self.con.send(bytes('true', 'utf-8'))
                    if ',' in _id:
                        _id = _id.split(',')[-1]
                    del Holder.meetings[_id]
                except Exception as e:
                    print(e)
        
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
            if self.streaming:
                stream = self.con.recv(2080)
                self.sendToAll(self.meeting_id, stream)
                status = self.con.recv(500)
                if status == "false":
                    self.streaming = False 
                    self.sendToAll(self.meeting_id, "stream_ended")
            else:
                request = self.con.recv(1080).decode('utf-8')
                args = self.con.recv(2080).decode('utf-8')
                if request.startswith(self.command_seperator):
                    request = request[3::]
                    if request == 'stream':
                        self.streaming = True
                        return
                if args.startswith(self.command_seperator):
                    args = args[3::]
                self.processRequest(request, args.split('|'))
        except ConnectionError:
            self.connected = False 
            return
        
    def run(self):
        try:
            status = self.con.recv(2080).decode('utf-8').split('/')
            for value in status:
                if value.startswith('username'):
                    self.name = value.split(':')[-1]
                elif value.startswith('logged_in'):
                    _status = value.split(':')[-1]
                    self.logged_in = True if _status.lower() == 'true' else False
            while self.connected:
                self.receiveRequest()
        except ConnectionError:
            self.connected = False
            return