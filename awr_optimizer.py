from pyawr_utils import awrde_utils
import os
import win32com.client as win32
import time

from tqdm import tqdm


class AwrOptimizer:
    def __init__(self, type: str, max_iter: int) -> None:
        self.awrde = None
        self.max_iter = max_iter
        self.type = type
        self.proj = None

    def connect(self):
        # self.awrde = awrde_utils.establish_link()#clsid_str='5BF3163E-6734-4FB4-891E-FD9E3D4A2CFA')
        self.awrde = awrde_utils.establish_link()
        self.proj = awrde_utils.Project(self.awrde)

    def run_optimizer(self):
        self.proj.optimization_max_iterations = self.max_iter
        self.proj.optimization_type = self.type
        self.proj.optimization_start = True  # Start the optimization

        with tqdm(total=self.max_iter) as pbar:
            while self.proj.optimization_start:
                time.sleep(0.1)
                pbar.update(self.awrde.Project.Optimizer.Iteration)
        x = 5
