import asterisk.manager
from asterisk.manager import ManagerAuthException, ManagerSocketException

port = "5038"
login = ""
password = ""


def connect(command,server):
    manager = asterisk.manager.Manager()
    try:
        manager.connect(server,port)
        manager.login(login,password)
        response = manager.command(command)
        return response.data
    except ManagerAuthException:
        return ['error 1',101]
    except ManagerSocketException:
        return ['error 2',102]
    except:
        return ['error 3',103]

def connect_calls(command,server):
    manager = asterisk.manager.Manager()
    try:
        manager.connect(server,port)
        manager.login(login,password)
        response = manager.command(command)
        return response.data
    except:
        return -1

