import math
import pickle
import shutil
import time
from typing import List, Dict

import json
import numpy as np
from dataclass_csv import DataclassReader
from pyawr_utils import awrde_utils
from tqdm import tqdm

from awr_optimizer.optimization_constraint import OptimizationConstraint
from materials.material import Material
from microstip_freq_calc.copied_calc import MicroStripCopiedCalc

MATERIALS_DB_CSV_PATH = "materials/materials_db.csv"
Z0 = 50


class AwrOptimizer:
    def __init__(self) -> None:
        self._awrde = None
        self._proj = None
        self._width_eq = None
        self._root_width_eq = None
        self._material = None
        self._width_calc = MicroStripCopiedCalc()

    def connect(self):
        self._awrde = awrde_utils.establish_link()
        self._proj = awrde_utils.Project(self._awrde)

    def get_sub_mapping(self, material_name: str):
        sub_dielectric_list = json.loads(
            self._proj.circuit_schematics_dict['WilkinsonPowerDivider'].elements_dict['STACKUP.SUB1'].parameters_dict[
                'MatName'].value_str.replace("{", "[").replace("}", "]"))
        sub_dielectric = {x: i for i, x in enumerate(sub_dielectric_list)}
        return "{" + f"{sub_dielectric['Air']},{sub_dielectric[material_name]}" + "}"

    def get_material_from_db(self, material_name: str) -> Material:
        material = None
        with open(MATERIALS_DB_CSV_PATH) as f:
            reader = DataclassReader(f, Material, validate_header=False)
            for row in reader:
                if row.name.strip() == material_name.strip():
                    material = row
        return material

    def setup(self, max_iter: int, optimization_type: str,
              optimization_properties: Dict,
              constraints: List[OptimizationConstraint],
              material_name: str):
        self._proj.optimization_max_iterations = max_iter
        self._proj.optimization_type = optimization_type
        self._material = self.get_material_from_db(material_name=material_name)

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

        params = self._proj.circuit_schematics_dict['WilkinsonPowerDivider'].elements_dict[
            'MSUB.SUBSTRATE'].parameters_dict

        params['Er'].value = self._material.er
        params['H'].value = self._material.height / 1000
        params['T'].value = self._material.thickness / 1000
        params['Rho'].value = self._material.rho
        params['Tand'].value = self._material.tanl
        params['ErNom'].value = self._material.er

        self._proj.circuit_schematics_dict['WilkinsonPowerDivider'].elements_dict['STACKUP.SUB1'].parameters_dict[
            'DieInd'].value_str = self.get_sub_mapping(material_name=material_name)

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
        self._width_eq.equation_value = str(
            self._width_calc.calc(er=self._material.er, thickness=self._material.thickness, z0=Z0,
                                  height=self._material.height, freq=freq))
        self._root_width_eq.equation_value = str(
            self._width_calc.calc(er=self._material.er, thickness=self._material.thickness, z0=Z0 * math.sqrt(2),
                                  height=self._material.height, freq=freq))

    def cleanup(self):
        shutil.rmtree("../DATA_SETS")
        shutil.rmtree("../TEMP")
