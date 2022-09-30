import math

import numpy as np

from awr_optimizer.awr_equation_manager import AwrEquationManager
from awr_optimizer.awr_optimizer import AwrOptimizer
from awr_optimizer.extractor import Extractor
from awr_optimizer.optimization_constraint import OptimizationConstraint
from microstip_freq_calc.copied_calc import MicroStripCopiedCalc


from materials.materials_db import MaterialDB
from copy import deepcopy


def run_simulations(ids, step_size):
    extractor = Extractor()
    extractor.connect()
    optimizer = AwrOptimizer()
    optimizer.connect()

    prev_quarter = None

    eq_manager = AwrEquationManager()
    eq_manager.connect()

    for id in [2, 1, 3]:
        chosen_mat = deepcopy(MaterialDB().get_by_id(id))
        freqs = [float(freq) for freq in np.arange(chosen_mat.start_freq, chosen_mat.end_freq, step_size)]
        print(f"freqs from :{freqs[0]} , to :{freqs[-1]} ,step :{step_size}")

        for freq in [10.0]:
            set_meshing(freq)
            bandwidth = freq / 10

            quarter_wavelength = prev_quarter if prev_quarter else extractor.extract_quarter_wavelength(frequency=freq)
            print(f"starting -- freq:{freq} , wavelength:{extractor.extract_quarter_wavelength(frequency=freq)}")

            start_width = MicroStripCopiedCalc().calc(er=chosen_mat.er, height=chosen_mat.height,
                                                      thickness=chosen_mat.thickness, z0=50, freq=freq)

            root_width = MicroStripCopiedCalc().calc(er=chosen_mat.er, height=chosen_mat.height,
                                                     thickness=chosen_mat.thickness, z0=70.7, freq=freq)

            input_padding = (2 * chosen_mat.pad_b + chosen_mat.pad_c + 2 * root_width - start_width) / 2

            quarter_wavelength = quarter_wavelength - input_padding

            constraints = [OptimizationConstraint(name='Res', max=100, min=20, start=100, should_optimize=False),
                           OptimizationConstraint(name='QUARTER', max=quarter_wavelength * 2,
                                                  min=quarter_wavelength / 3,
                                                  start=quarter_wavelength),
                           OptimizationConstraint(name='HEIGHT', max=10, min=0.01, start=chosen_mat.height,
                                                  should_optimize=False),
                           OptimizationConstraint(name='PAD_A', max=10, min=0,
                                                  start=chosen_mat.pad_a,
                                                  should_optimize=False),
                           OptimizationConstraint(name='PAD_B', max=chosen_mat.pad_b, min=0,
                                                  start=chosen_mat.pad_b,
                                                  should_optimize=False),
                           OptimizationConstraint(name='PAD_C', max=chosen_mat.pad_c, min=0,
                                                  start=chosen_mat.pad_c,
                                                  should_optimize=False),
                           OptimizationConstraint(name='INPUT_PADDING', max=input_padding, min=0,
                                                  start=input_padding,
                                                  should_optimize=False)
                           ]

            optimizer.setup(max_iter=15,
                            optimization_type="Gradient Optimization",
                            optimization_properties={"Converge Tolerance": 0.01,
                                                     "Step Size": 0.001
                                                     },
                            constraints=constraints,
                            material=chosen_mat)

            optimizer.run_optimizer(freq=freq, bandwidth=bandwidth, num_points=5)

            # constraints = [
            #     OptimizationConstraint(name='HEIGHT', max=10, min=0.01, start=chosen_mat.height)]
            #
            # optimizer.setup(max_iter=15,
            #                 optimization_type="Gradient Optimization",
            #                 optimization_properties={"Converge Tolerance": 0.01,
            #                                          "Step Size": 0.001
            #                                          },
            #                 constraints=constraints,
            #                 material=chosen_mat)
            #
            # optimizer.run_optimizer(freq=freq, bandwidth=bandwidth, num_points=3)

            extractor.extract_results(frequency=freq, bandwidth=bandwidth, material=chosen_mat)

            prev_quarter = float(
                eq_manager.get_equation_by_name("QUARTER").equation_value) + input_padding / 2


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
    step_size = 0.5

    ids = [1, 2, 3]

    print("starting dataset generation using awr optimization")
    print(f"ids:{ids}")

    run_simulations(ids=ids, step_size=step_size)
    x = 5
