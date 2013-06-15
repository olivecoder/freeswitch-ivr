import inspect
from modivr import in_freeswitch

def log(msg="CheckPoint", level="info"):
    global in_freeswitch
    line=inspect.currentframe().f_back.f_lineno
    msg = "IVR: %i: %s" % (line, msg)
    if in_freeswitch:
        consoleLog(level, msg + "\n")
    else:
        print msg
    
