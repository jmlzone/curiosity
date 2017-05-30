import subprocess
import string
import os.path
class irTemp :
    def __init__ (self) :
        self.installPath = os.path.dirname(os.path.realpath(__file__))
        self.mlxPath = os.path.abspath(self.installPath + "/../c/mlxAvg10")
        pass
    def measure(self) :
        measurment = subprocess.check_output(self.mlxPath)
        (a,o)=measurment.split(",")
        amb=float(a)
        obj=float(o)
        return (amb,obj)
