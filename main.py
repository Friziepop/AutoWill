# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np

from awr_optimizer.awr_equation_manager import AwrEquationManager
from awr_optimizer.awr_optimizer import AwrOptimizer
from awr_optimizer.extractor import Extractor
from awr_optimizer.optimization_constraint import OptimizationConstraint

from materials.materials_db import MaterialDB
from copy import deepcopy


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def run_simulations():
    extractor = Extractor()
    extractor.connect()
    optimizer = AwrOptimizer()
    optimizer.connect()
    ids = [1, 2, 3]
    bandwith = 0.25
    freqs = np.arange(1, 40, 0.5)

    for id in ids:
        for freq in freqs:
            set_meshing(freq)

            chosen_mat = deepcopy(MaterialDB().get_by_id(id))
            quarter_wavelength = extractor.extract_quarter_wavelength(frequency=freq)
            print(f"starting -- freq:{freq} , wavelength:{quarter_wavelength * 4}")
            constraints = [OptimizationConstraint(name='Res', max=100, min=20, start=100, should_optimize=False),
                           OptimizationConstraint(name='QUARTER', max=quarter_wavelength * 2,
                                                  min=quarter_wavelength / 2,
                                                  start=quarter_wavelength),
                           OptimizationConstraint(name='HEIGHT', max=10, min=0.01, start=chosen_mat.height,
                                                  should_optimize=False)]

            optimizer.setup(max_iter=300,
                            optimization_type="Gradient Optimization",
                            optimization_properties={"Converge Tolerance": 0.01,
                                                     "Step Size": 0.001
                                                     },
                            constraints=constraints,
                            material=chosen_mat)

            optimizer.run_optimizer(freq=freq, bandwidth=bandwith, num_points=3)

            constraints = [
                OptimizationConstraint(name='HEIGHT', max=10, min=0.01, start=chosen_mat.height)]

            optimizer.setup(max_iter=300,
                            optimization_type="Gradient Optimization",
                            optimization_properties={"Converge Tolerance": 0.01,
                                                     "Step Size": 0.001
                                                     },
                            constraints=constraints,
                            material=chosen_mat)

            optimizer.run_optimizer(freq=freq, bandwidth=bandwith, num_points=3)

            constraints = [
                OptimizationConstraint(name='WIDTH', max=10, min=0.1, start=5)]

            optimizer.setup(max_iter=300,
                            optimization_type="Gradient Optimization",
                            optimization_properties={"Converge Tolerance": 0.01,
                                                     "Step Size": 0.001
                                                     },
                            constraints=constraints,
                            material=chosen_mat)

            optimizer.run_optimizer(freq=freq, bandwidth=bandwith, num_points=3)

            extractor.extract_results(frequency=freq, bandwidth=bandwith, material=chosen_mat)


def set_meshing(freq):
    equation_manager = AwrEquationManager()
    equation_manager.connect()
    if 0 <= freq < 10:
        equation_manager.set_equation_value("MESHING", 0.1)
    if 10 <= freq < 20:
        equation_manager.set_equation_value("MESHING", 0.01)
    if 20 <= freq < 30:
        equation_manager.set_equation_value("MESHING", 0.005)
    if 30 <= freq < 40:
        equation_manager.set_equation_value("MESHING", 0.002)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    run_simulations()
    x = 5

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
