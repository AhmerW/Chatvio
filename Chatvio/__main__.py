import os 

from server.server import Server


## make sure this server doesnt start twice..
started = os.environ.get("CHATVIO_STARTED")
if not started:
    os.environ["CHATVIO_STARTED"] = "1"
    
    
    
    mainServer = Server()
    mainServer.start()
else:
    raise ValueError("Program has already launched. Running two instances can create trouble..")