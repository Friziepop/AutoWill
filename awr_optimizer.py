import math
import pickle
from typing import List, Dict

import numpy as np
from pyawr_utils import awrde_utils
import time
import shutil
from tqdm import tqdm

from optimization_constraint import OptimizationConstraint


class AwrOptimizer:
    def __init__(self) -> None:
        self._awrde = None
        self._proj = None
        self._width_eq = None
        self._root_width_eq = None

    def connect(self):
        self._awrde = awrde_utils.establish_link()
        self._proj = awrde_utils.Project(self._awrde)

    def setup(self, max_iter: int, optimization_type: str,
              optimization_properties: Dict,
              constraints: List[OptimizationConstraint]):
        self._proj.optimization_max_iterations = max_iter
        self._proj.optimization_type = optimization_type

        for key, value in self._proj.circuit_schematics_dict['WilkinsonPowerDivider'].equations_dict.items():
            if value.equation_name == 'WIDTH':
                self._width_eq = value
            if value.equation_name == 'ROOTWIDTH':
                self._root_width_eq = value

        for key, val in self._proj.optimization_type_properties.items():
            self._proj.optimization_type_properties[key] = optimization_properties[key]
        self._proj.optimization_update_type_properties()

        equations_dict = self._proj.circuit_schematics_dict['WilkinsonPowerDivider'].equations_dict

        for key, ele in equations_dict.items():
            ele.optimize_enabled = False

        for con in constraints:
            equation_opt = [eq for key, eq in equations_dict.items() if
                            eq.equation_name == con.name]
            if len(equation_opt) == 1:
                first = equation_opt[0]
                first.optimize_enabled = con.should_optimize
                first.lower_constraint = con.min if con.min else 0
                first.upper_constraint = con.max if con.max else 10 ^ 6
                first.constrain = con.constrain
                first.equation_value = str(con.start)
            else:
                print(f"error:{con.name} not optimized")

    def run_optimizer(self, freq: float, bandwidth: float, num_points: int, ):
        self.set_proj_params(bandwidth, freq, num_points)

        max_iter = self._proj.optimization_max_iterations
        self._proj.optimization_start = True  # Start the optimization
        old = 0
        with tqdm(total=max_iter, desc=f"{freq} Ghz") as pbar:
            while self._proj.optimization_start:
                time.sleep(0.1)
                new = self._awrde.Project.Optimizer.Iteration
                pbar.update(new - old)
                old = new

    def set_proj_params(self, bandwidth, freq, num_points):
        freq_array = np.linspace(freq - bandwidth / 2, freq + bandwidth / 2, num_points)
        self._proj.set_project_frequencies(project_freq_ay=freq_array, units_str='GHz')
        with open("microstip_freq/freq2width_dict.pickle", "rb") as file:
            freq_to_width = pickle.load(file)
            self._width_eq.equation_value = str(freq_to_width[str(freq)])
            self._root_width_eq.equation_value = str(math.sqrt(freq_to_width[str(freq)]))



    def cleanup(self):
        shutil.rmtree("DATA_SETS")
        shutil.rmtree("TEMP")
