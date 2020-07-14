import socket 
import os
import logging 
from threading import active_count

try:
    from .database import db
    from .clientHandling import clientConnection
except ImportError:
    # This server is meant to be started from the __main__.py file
    # if it's started correctly then the importerror will  not get raised,
    # unless if someone decide to directly start it from server.py
    # which in that case the above imports will not work.
    from database import db
    from clientHandling import clientConnection

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
logger.addHandler(handler)

class server(object):
    def __init__(self, ip : str = "localhost", port : int = 8998):
        self.ip, self.port = ip, port
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        
        self.serverRunning = True
        
        #instances 
        self.db = db.db()
        
    def start(self):
        logger.warning("Server is now listening on ({0.ip}, {0.port})! Clients are able to connect!".format(self))
        self.server.listen()
        while self.serverRunning:
            conn, addr = self.server.accept()
            print(f"[{addr}] Connected")
            print(f"{active_count()} threads running!")
            connection = clientConnection(conn, addr)
            self.db.add_connection(conn)
            connection.start()