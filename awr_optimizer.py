from pyawr_utils import awrde_utils
import os
import win32com.client as win32
import time;

class AwrOptimizer:
    def __init__(self) -> None:
        pass
    def connect(self):
        #self.awrde = awrde_utils.establish_link()#clsid_str='5BF3163E-6734-4FB4-891E-FD9E3D4A2CFA')
        self.awr = win32.DispatchEx("MWOApp.MWOffice")
        path = f"{os.getcwd()}\\WilkingsonPowerDivider.emp"
        print (f"opening path :{path}")
        self.awr.Open(path)
    def run_optimizer(self):
        self.awr.Project.Optimizer.MaxIterations = 500
        self.awr.Project.Optimizer.Type = "Gradient Optimization"
        self.awr.Project.Optimizer.NewWindow()
        self.awr.Project.Optimizer.Start()
        while self.awr.Project.Optimizer.Running == True:
            print ("hi 22")
            time.sleep(0.5)
