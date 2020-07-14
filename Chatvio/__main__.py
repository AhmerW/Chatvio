import os 

from server.server import server


## make sure this server doesnt start twice..
started = os.environ.get("CHATVIO_STARTED")
if not started:
    os.environ["CHATVIO_STARTED"] = "1"
    
    
    
    mainServer = server()
    mainServer.start()
else:
    raise ValueError("Program has already launched. Running two instances can create trouble..")