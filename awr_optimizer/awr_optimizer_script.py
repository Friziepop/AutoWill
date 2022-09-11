import math

import numpy as np

from awr_equation_manager import AwrEquationManager
from awr_optimizer import AwrOptimizer
from extractor import Extractor
from optimization_constraint import OptimizationConstraint

from materials.materials_db import MaterialDB
from copy import deepcopy


def run_simulations(ids, freqs):
    extractor = Extractor()
    extractor.connect()
    optimizer = AwrOptimizer()
    optimizer.connect()

    prev_quarter = None

    eq_manager = AwrEquationManager()
    eq_manager.connect()

    for id in [2, 1, 3]:
        for freq in freqs[9:]:
            set_meshing(freq)
            bandwidth = 0.5

            chosen_mat = deepcopy(MaterialDB().get_by_id(id))
            quarter_wavelength = prev_quarter if prev_quarter else extractor.extract_quarter_wavelength(frequency=freq)
            print(f"starting -- freq:{freq} , wavelength:{quarter_wavelength * 4}")

            # if needed add half wavelength to add room for padding
            number_of_quarters_to_add = math.floor(chosen_mat.padding_length / quarter_wavelength)
            number_of_quarters_to_add = number_of_quarters_to_add + 1 if number_of_quarters_to_add % 2 \
                else number_of_quarters_to_add

            quarter_wavelength = quarter_wavelength + number_of_quarters_to_add * quarter_wavelength

            quarter_wavelength = quarter_wavelength - chosen_mat.padding_length / 2

            constraints = [OptimizationConstraint(name='Res', max=100, min=20, start=100, should_optimize=False),
                           OptimizationConstraint(name='QUARTER', max=quarter_wavelength * 2,
                                                  min=quarter_wavelength / 3,
                                                  start=quarter_wavelength),
                           OptimizationConstraint(name='HEIGHT', max=10, min=0.01, start=chosen_mat.height,
                                                  should_optimize=False),
                           OptimizationConstraint(name='PAD_A', max=10, min=0,
                                                  start=chosen_mat.pad_a,
                                                  should_optimize=False),
                           OptimizationConstraint(name='PAD_B', max=10, min=0,
                                                  start=chosen_mat.pad_b,
                                                  should_optimize=False),
                           OptimizationConstraint(name='PAD_C', max=10, min=0,
                                                  start=chosen_mat.pad_c,
                                                  should_optimize=False)
                           ]

            optimizer.setup(max_iter=15,
                            optimization_type="Gradient Optimization",
                            optimization_properties={"Converge Tolerance": 0.01,
                                                     "Step Size": 0.001
                                                     },
                            constraints=constraints,
                            material=chosen_mat)

            optimizer.run_optimizer(freq=freq, bandwidth=bandwidth, num_points=3)

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
                eq_manager.get_equation_by_name("QUARTER").equation_value) + chosen_mat.padding_length / 2


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
    end_freq = 40
    step_size = 1

    ids = [1, 2, 3]

    freqs = [float(freq) for freq in np.arange(start_freq, end_freq, step_size)]
    print("starting dataset generation using awr optimization")
    print(f"ids:{ids}")
    print(f"freqs from :{start_freq} , to :{end_freq} ,step :{step_size}")

    run_simulations(ids=ids, freqs=freqs)
    x = 5
