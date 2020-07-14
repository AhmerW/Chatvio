

class db(object):
    def __init__(self):
        self._total_connections = 0
        
        self.connections = set()
    
    @property 
    def total_connections(self):
        return self._total_connections
    
    @total_connections.setter 
    def total_connections(self, val):
        self._total_connections = val
        
    def add_connection(self, conn):
        self.connections.add(conn)
    
    def remove_connection(self, conn) -> bool:
        try:
            self.connections.remove(conn)
            return True
        except KeyError:
            return False