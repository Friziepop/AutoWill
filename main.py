# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
import os

import numpy as np
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

    bandwith = 0.5
    freqs = np.linspace(4, 6, 5)
    for freq in [10]:
        quarter_wavelength = extractor.extract_quarter_wavelength(frequency=freq)
        print(f"starting -- freq:{freq} , wavelength:{quarter_wavelength * 4}")
        constraints = [OptimizationConstraint(name='Res', max=100, min=20, start=50)
            , OptimizationConstraint(name='QUARTER', max=quarter_wavelength * 2, min=quarter_wavelength / 2,
                                     start=quarter_wavelength),
                       OptimizationConstraint(name='HALF', max=None, min=None, start=quarter_wavelength * 2,
                                              should_optimize=False)]

        optimizer.setup(max_iter=35,
                        optimization_type="Gradient Optimization",
                        optimization_properties={"Converge Tolerance": 0.01,
                                                 "Step Size": 0.001
                                                 },
                        constraints=constraints)
        optimizer.run_optimizer(freq=freq, bandwidth=bandwith, num_points=3)
        # optimizer.cleanup()
        extractor.extract_results(frequency=freq, bandwidth=bandwith)
        x = 5
    x = 5

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
