# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np

from awr_optimizer.awr_optimizer import AwrOptimizer
from awr_optimizer.extractor import Extractor
from awr_optimizer.optimization_constraint import OptimizationConstraint
import os

from materials.material import Material


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

    bandwith = 0.25
    freqs = np.linspace(1, 50, 99)
    for freq in [5.0]:
        quarter_wavelength = extractor.extract_quarter_wavelength(frequency=freq)
        print(f"starting -- freq:{freq} , wavelength:{quarter_wavelength * 4}")
        constraints = [OptimizationConstraint(name='Res', max=100, min=20, start=100, should_optimize=False)
            , OptimizationConstraint(name='QUARTER', max=quarter_wavelength * 2, min=quarter_wavelength / 2,
                                     start=quarter_wavelength),
                       OptimizationConstraint(name='HALF', max=None, min=None, start=quarter_wavelength * 2,
                                              should_optimize=False)]

        optimizer.setup(max_iter=300,
                        optimization_type="Gradient Optimization",
                        optimization_properties={"Converge Tolerance": 0.01,
                                                 "Step Size": 0.001
                                                 },
                        constraints=constraints,
                        material_name='fr4')
        optimizer.run_optimizer(freq=freq, bandwidth=bandwith, num_points=3)
        # optimizer.cleanup()
        extractor.extract_results(frequency=freq, bandwidth=bandwith)
        x = 5
    x = 5

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
