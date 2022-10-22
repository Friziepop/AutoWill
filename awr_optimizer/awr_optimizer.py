import math
import pickle
import shutil
import time
from typing import List, Dict

import json
import numpy as np
from tqdm import tqdm

from awr_optimizer.awr_connector import AwrConnector
from awr_optimizer.awr_equation_manager import AwrEquationManager
from awr_optimizer.optimization_constraint import OptimizationConstraint
from materials.material import Material
from microstip_freq_calc.copied_calc import MicroStripCopiedCalc

MATERIALS_DB_CSV_PATH = "materials/materials_db.csv"
Z0 = 50


class AwrOptimizer(AwrConnector):
    def __init__(self) -> None:
        super(AwrOptimizer, self).__init__()
        self._material = None
        self._width_calc = MicroStripCopiedCalc()
        self._eq_manager = AwrEquationManager()

    def connect(self):
        super(AwrOptimizer, self).connect()
        self._eq_manager.connect()

    def setup(self, max_iter: int, optimization_type: str,
              optimization_properties: Dict,
              constraints: List[OptimizationConstraint],
              material: Material):

        self._eq_manager.disable_opt_all()
        self._proj.optimization_max_iterations = max_iter
        self._proj.optimization_type = optimization_type
        self._material = material

        for key, val in self._proj.optimization_type_properties.items():
            self._proj.optimization_type_properties[key] = optimization_properties[key]
        self._proj.optimization_update_type_properties()

        for con in constraints:
            self._eq_manager.set_constraint(con=con)

        params = self._proj.circuit_schematics_dict['WilkinsonPowerDivider'].elements_dict[
            'MSUB.SUBSTRATE'].parameters_dict

        params['T'].value = self._material.thickness / 1000  # convert between units
        params['Rho'].value = self._material.rho
        params['ErNom'].value = self._material.er

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
        self._eq_manager.set_equation_value(eq_name="WIDTH", eq_val=str(
            self._width_calc.calc(er=self._material.er, thickness=self._material.thickness, z0=Z0,
                                  height=self._material.height, freq=freq)))

    def cleanup(self):
        shutil.rmtree("../DATA_SETS")
        shutil.rmtree("../TEMP")
