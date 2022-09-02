import numpy as np

from awr_equation_manager import AwrEquationManager
from awr_optimizer import AwrOptimizer
from extractor import Extractor
from optimization_constraint import OptimizationConstraint

from materials.materials_db import MaterialDB
from copy import deepcopy


def run_simulations(ids, freqs, bandwidth):
    extractor = Extractor()
    extractor.connect()
    optimizer = AwrOptimizer()
    optimizer.connect()

    for id in ids:
        for freq in freqs:
            set_meshing(freq)

            chosen_mat = deepcopy(MaterialDB().get_by_id(id))
            quarter_wavelength = extractor.extract_quarter_wavelength(frequency=freq)
            print(f"starting -- freq:{freq} , wavelength:{quarter_wavelength * 4}")
            constraints = [OptimizationConstraint(name='Res', max=100, min=20, start=100, should_optimize=False),
                           OptimizationConstraint(name='QUARTER', max=quarter_wavelength * 2,
                                                  min=quarter_wavelength / 3,
                                                  start=quarter_wavelength),
                           OptimizationConstraint(name='HEIGHT', max=10, min=0.01, start=chosen_mat.height,
                                                  should_optimize=False)]

            optimizer.setup(max_iter=30,
                            optimization_type="Gradient Optimization",
                            optimization_properties={"Converge Tolerance": 0.01,
                                                     "Step Size": 0.001
                                                     },
                            constraints=constraints,
                            material=chosen_mat)

            optimizer.run_optimizer(freq=freq, bandwidth=bandwidth, num_points=5)

            constraints = [
                OptimizationConstraint(name='HEIGHT', max=10, min=0.01, start=chosen_mat.height)]

            optimizer.setup(max_iter=30,
                            optimization_type="Gradient Optimization",
                            optimization_properties={"Converge Tolerance": 0.01,
                                                     "Step Size": 0.001
                                                     },
                            constraints=constraints,
                            material=chosen_mat)

            optimizer.run_optimizer(freq=freq, bandwidth=bandwidth, num_points=5)

            constraints = [
                OptimizationConstraint(name='WIDTH', max=10, min=0.1, start=5)]

            optimizer.setup(max_iter=30,
                            optimization_type="Gradient Optimization",
                            optimization_properties={"Converge Tolerance": 0.01,
                                                     "Step Size": 0.001
                                                     },
                            constraints=constraints,
                            material=chosen_mat)

            optimizer.run_optimizer(freq=freq, bandwidth=bandwidth, num_points=5)

            extractor.extract_results(frequency=freq, bandwidth=bandwidth, material=chosen_mat)


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


if __name__ == '__main__':
    start_freq = 1
    end_freq = 20
    step_size = 1

    ids = [1, 2, 3]
    bandwidth = 0.5

    freqs = [float(freq) for freq in np.arange(start_freq, end_freq, step_size)]
    print("starting dataset generation using awr optimization")
    print(f"ids:{ids}")
    print(f"bandwidth:{bandwidth}")
    print(f"freqs from :{start_freq} , to :{end_freq} ,step :{step_size}")

    run_simulations(ids=ids, bandwidth=bandwidth, freqs=freqs)
    x = 5
