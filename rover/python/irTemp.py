import subprocess
import string
class irTemp :
    def __init__ (self) :
        pass
    def measure(self) :
        measurment = subprocess.check_output("./mlxAvg10")
        (a,o)=measurment.split(",")
        amb=float(a)
        obj=float(o)
        return (amb,obj)
