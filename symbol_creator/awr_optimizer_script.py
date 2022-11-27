import math

import numpy as np
from scipy.constants import speed_of_light

from awr_optimizer.awr_equation_manager import AwrEquationManager
from awr_optimizer.awr_optimizer import AwrOptimizer
from awr_optimizer.extractor import Extractor
from awr_optimizer.optimization_constraint import OptimizationConstraint
from awr_optimizer.optimizer_points_retriever import OptimizerPointsRetriever
from microstip_freq_calc.copied_calc import MicroStripCopiedCalc

from materials.materials_db import MaterialDB
from copy import deepcopy


def run_simulations(ids, step_size):
    extractor = Extractor()
    extractor.connect()
    optimizer = AwrOptimizer()
    optimizer.connect()

    prev_quarter = None
    prev_rootwidth = None
    eq_manager = AwrEquationManager()
    eq_manager.connect()

    for id in ids:
        chosen_mat = deepcopy(MaterialDB().get_by_id(id))

        simulation_points = OptimizerPointsRetriever(material=chosen_mat).get_points()
        print(f"freqs from :{simulation_points[0][0]} , to :{simulation_points[-1][0]}")

        for freq, er, tanl in simulation_points:
            chosen_mat.er = er
            chosen_mat.tanl = tanl
            set_meshing(freq)
            bandwidth = freq / 15

            quarter_wavelength = 10 ** 3 * ((speed_of_light / (freq * 10 ** 9 * math.sqrt(er))) / 4)

            print(f"starting -- freq:{freq} , wavelength:{extractor.extract_quarter_wavelength(frequency=freq)}")

            micro_strip_calc = MicroStripCopiedCalc()
            start_width = micro_strip_calc.calc(er=chosen_mat.er, height=chosen_mat.height,
                                                thickness=chosen_mat.thickness, z0=50, freq=freq)

            root_width = micro_strip_calc.calc(er=chosen_mat.er, height=chosen_mat.height,
                                               thickness=chosen_mat.thickness, z0=70.7,
                                               freq=freq) if not prev_rootwidth else prev_rootwidth

            input_padding = \
                (2 * chosen_mat.resistor.pad_b + chosen_mat.resistor.pad_c - start_width) / 2

            quarter_wavelength = quarter_wavelength - input_padding

            constraints = [OptimizationConstraint(name='Res', max=100, min=20, start=100, should_optimize=False),
                           OptimizationConstraint(name='QUARTER', max=quarter_wavelength * 2,
                                                  min=quarter_wavelength / 3,
                                                  start=quarter_wavelength, should_optimize=True),
                           OptimizationConstraint(name='INPUT_PADDING', max=input_padding,
                                                  min=input_padding,
                                                  start=input_padding, should_optimize=False),
                           OptimizationConstraint(name='HEIGHT', max=10, min=0.01, start=chosen_mat.height,
                                                  should_optimize=False),
                           OptimizationConstraint(name='PAD_A', max=10, min=0,
                                                  start=chosen_mat.resistor.pad_a,
                                                  should_optimize=False),
                           OptimizationConstraint(name='PAD_B', max=chosen_mat.resistor.pad_b, min=0,
                                                  start=chosen_mat.resistor.pad_b,
                                                  should_optimize=False),
                           OptimizationConstraint(name='PAD_C', max=chosen_mat.resistor.pad_c, min=0,
                                                  start=chosen_mat.resistor.pad_c,
                                                  should_optimize=False),
                           OptimizationConstraint(name='ROOTWIDTH', max=5, min=0,
                                                  start=root_width,
                                                  should_optimize=False),
                           OptimizationConstraint(name='OUTPUT_PADDING', max=quarter_wavelength * 2,
                                                  min=quarter_wavelength / 100,
                                                  start=quarter_wavelength / 10,
                                                  should_optimize=False),
                           OptimizationConstraint(name='PORT_1_PADDING', max=quarter_wavelength,
                                                  min=quarter_wavelength / 100,
                                                  start=quarter_wavelength / 10,
                                                  should_optimize=False),
                           OptimizationConstraint(name='Er', max=chosen_mat.er,
                                                  min=chosen_mat.er,
                                                  start=chosen_mat.er,
                                                  should_optimize=False),
                           OptimizationConstraint(name='Tanl', max=chosen_mat.tanl,
                                                  min=chosen_mat.tanl,
                                                  start=chosen_mat.tanl,
                                                  should_optimize=False),
                           ]

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

            optimizer.setup(max_iter=15,
                            optimization_type="Simplex Optimizer",
                            optimization_properties={"Converge Tolerance": 0.01,
                                                     "Step Size": 0.001
                                                     },
                            constraints=constraints,
                            material=chosen_mat)

            optimizer.run_optimizer(freq=freq, bandwidth=bandwidth, num_points=3)

            constraints = [OptimizationConstraint(name='ROOTWIDTH', max=root_width * 1.2, min=root_width / 1.2,
                                                  start=root_width,
                                                  should_optimize=True)
                           ]

            optimizer.setup(max_iter=15,
                            optimization_type="Simplex Optimizer",
                            optimization_properties={"Converge Tolerance": 0.01,
                                                     "Step Size": 0.001
                                                     },
                            constraints=constraints,
                            material=chosen_mat)

            optimizer.run_optimizer(freq=freq, bandwidth=bandwidth, num_points=3)

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
    step_size = 0.5

    ids = [5]

    print("starting dataset generation using awr optimization")
    print(f"ids:{ids}")

    run_simulations(ids=ids, step_size=step_size)
    x = 5
