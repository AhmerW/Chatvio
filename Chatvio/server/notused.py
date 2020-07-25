import threading
import socket 

## change to server file

class ClientConnection(threading.Thread):
    def __init__(self, conn, addr):
        super(ClientConnection, self).__init__()
        
        #variables
        self.con, self.adr = conn, addr
        

        #client variables
        self.connected = True
        
        self.name = ""
        self.logged_in = False 
        
    def handleLogin(self):
        pass
    
    def processRequest(self, req, *args):
        if args:
            args = args[0]
        if req.endswith('meeting'):
            req = req.split('_')[0].lower()
            if req == 'create':
                print(f"Creating meeting with {args}")
            elif req == 'join':
                pass 
            elif req == 'leave':
                pass 
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