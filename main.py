# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from cgi import print_arguments
import os
import win32com.client as win32

from pyawr_utils import awrde_utils

from awr_optimizer import AwrOptimizer
from extractor import Extractor
from optimization_constraint import OptimizationConstraint


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # output Res,Quarter,HALF,RADIUS wavelength
    extractor = Extractor()
    extractor.connect()
    optimizer = AwrOptimizer()
    optimizer.connect()

    constraints = [OptimizationConstraint(name='Res', max=120, min=80, start=100),
                   OptimizationConstraint(name='QUARTER', max=None, min=None, start=10)]
    optimizer.setup(freq=4.5, bandwidth=0.5, num_points=3, max_iter=10, optimization_type="Gradient Optimization",
                    constraints=constraints)
    optimizer.run_optimizer()
    res = extractor.extract_results()
    x=5

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
