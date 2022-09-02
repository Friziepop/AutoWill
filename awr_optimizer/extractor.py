import math
from pathlib import Path
from typing import Dict, List

from pyawr_utils import awrde_utils

from dacite import from_dict

from pyawr_utils.common_utils import _Element

from dataclasses import dataclass

from dataclass_csv import DataclassWriter
from scipy.constants import constants

from awr_optimizer.awr_connector import AwrConnector
from awr_optimizer.awr_equation_manager import AwrEquationManager
from materials.material import Material

S_PARAMS_CSV_FILE = "sparams.csv"
VARS_CSV_FILE = "vars.csv"

S_PARAM_FIELD_TO_CLASS_FIELD = {
    "WilkinsonPowerDivider:DB(|S(1,1)|)": "s_1_1",
    "WilkinsonPowerDivider:DB(|S(2,2)|)": "s_2_2",
    "WilkinsonPowerDivider:DB(|S(3,3)|)": "s_3_3",
    "WilkinsonPowerDivider:DB(|S(3,1)|)": "s_3_1",
    "WilkinsonPowerDivider:DB(|S(3,2)|)": "s_3_2",
    "WilkinsonPowerDivider:DB(|S(2,1)|)": "s_2_1"
}

CLASS_FIELD_TO_VARS = {
    "res": "Res",
    "quarter": "QUARTER",
    "radius": "RADIUS",
    "height": "HEIGHT",
    "root_width": "ROOTWIDTH",
    "width": "WIDTH"
}

SPARAM_ZERO_THRESHOLD = -30

SPARAMS_TO_CHECK_ZERO_THRESHOLD = [
    "WilkinsonPowerDivider:DB(|S(1,1)|)",
    "WilkinsonPowerDivider:DB(|S(2,2)|)",
    "WilkinsonPowerDivider:DB(|S(3,3)|)",
    "WilkinsonPowerDivider:DB(|S(3,2)|)"
]

SPARAM_3_DB_THRESHOLD = 1000

SPARAMS_TO_CHECK_3_DB_THRESHOLD = [
    "WilkinsonPowerDivider:DB(|S(2,1)|)",
    "WilkinsonPowerDivider:DB(|S(3,1)|)"
]


@dataclass
class Vars:
    name: str
    id: int
    frequency: float
    radius: float
    quarter: float
    res: float
    height: float
    root_width: float
    width: float

    def __init__(self, name, id, frequency, radius, quarter, res, height, root_width, width):
        self.name = name
        self.id = id
        self.frequency = frequency
        self.radius = radius
        self.quarter = quarter
        self.res = res
        self.height = height
        self.root_width = root_width
        self.width = width


@dataclass
class SParams:
    id: int
    name: str
    bandwidth: float
    frequency: float
    left_freq: float
    right_freq: float
    s_1_1: float
    s_2_2: float
    s_3_3: float
    s_3_1: float
    s_3_2: float
    s_2_1: float

    def __init__(self, id, name, bandwidth, frequency, left_freq, right_freq,
                 s_1_1, s_2_2, s_3_3, s_3_1, s_3_2, s_2_1):
        self.id = id
        self.name = name
        self.bandwidth = bandwidth
        self.frequency = frequency
        self.left_freq = left_freq
        self.right_freq = right_freq
        self.s_1_1 = s_1_1
        self.s_2_2 = s_2_2
        self.s_3_3 = s_3_3
        self.s_3_1 = s_3_1
        self.s_3_2 = s_3_2
        self.s_2_1 = s_2_1


@dataclass
class SParam:
    frequency: float
    db_value: float

    def __init__(self, frequency, db_value):
        self.frequency = frequency
        self.db_value = db_value


@dataclass
class ExtractionResult:
    s_param_to_measurements: Dict[str, List[SParam]]
    circuit_vars: Dict[str, _Element]

    def __init__(self):
        self.s_param_to_measurements = {}
        self.circuit_vars = {}


class Extractor(AwrConnector):
    def __init__(self):
        super(Extractor, self).__init__()
        self._eq_manager = AwrEquationManager()

    def connect(self):
        super(Extractor, self).connect()
        self._eq_manager.connect()

    def extract_quarter_wavelength(self, frequency) -> float:
        eps_r = \
            self._proj.circuit_schematics_dict['WilkinsonPowerDivider'].elements_dict["MSUB.SUBSTRATE"].parameters_dict[
                'Er'].value
        qua_meter = (constants.speed_of_light / (frequency * 10 ** 9 * math.sqrt(eps_r))) / 4
        return qua_meter * 10 ** 3

    def extract_results(self, frequency: float, bandwidth: float, material: Material,
                        save_csv=True) -> ExtractionResult:
        result = ExtractionResult()

        for key, value in self._proj.graph_dict['Match'].measurements_dict.items():
            result.s_param_to_measurements[value.measurement_name] = \
                [SParam(measurement[0], measurement[1]) for measurement in value.trace_data[0]]

        for key, value in self._proj.graph_dict['Transmission'].measurements_dict.items():
            result.s_param_to_measurements[value.measurement_name] = \
                [SParam(measurement[0], measurement[1]) for measurement in value.trace_data[0]]

        result.circuit_vars = self._proj.circuit_schematics_dict['WilkinsonPowerDivider'].elements_dict

        if save_csv:
            self.extract_s_params_to_csv(material.id, bandwidth, material.name, frequency, result)
            self.extract_vars_to_csv(frequency, material.id, material.name)

        return result

    def extract_vars_to_csv(self, frequency: float, id: int, name: str):
        vars_dict = {"frequency": frequency, "id": id, "name": name}
        for field, eq_name in CLASS_FIELD_TO_VARS.items():
            vars_dict[field] = float(self._eq_manager.get_equation_by_name(eq_name).equation_value)

        vars = from_dict(data_class=Vars, data=vars_dict)
        csv_file = Path(VARS_CSV_FILE)
        csv_already_exists = csv_file.exists()

        with open(VARS_CSV_FILE, "a", newline='', encoding='utf-8') as f:
            w = DataclassWriter(f, [vars], Vars)
            for key, value in CLASS_FIELD_TO_VARS.items():
                w.map(value).to(key)

            w.write(skip_header=csv_already_exists)

    @staticmethod
    def extract_s_params_to_csv(material_id: int, bandwidth: float, material_name: str, frequency: float,
                                result: ExtractionResult):
        s_params_dict = {"id": material_id, "name": material_name, "frequency": frequency}

        for key, value in result.s_param_to_measurements.items():
            for s_param in value:
                if round(s_param.frequency, 2) == round(frequency, 2):
                    s_params_dict[S_PARAM_FIELD_TO_CLASS_FIELD[key]] = s_param.db_value
                    break

        left_frequency = 0
        right_frequency = frequency + bandwidth

        for key, value in result.s_param_to_measurements.items():
            if key in SPARAMS_TO_CHECK_ZERO_THRESHOLD:
                frequencies_below_zero = [s_param.frequency for s_param in value if
                                          s_param.db_value <= SPARAM_ZERO_THRESHOLD]

                left_frequency = max(left_frequency,
                                     min(frequencies_below_zero)) if frequencies_below_zero else frequency
                right_frequency = min(left_frequency,
                                      max(frequencies_below_zero)) if frequencies_below_zero else frequency

            if key in SPARAMS_TO_CHECK_3_DB_THRESHOLD:
                frequencies_around_3db = [s_param.frequency for s_param in value if
                                          -3 + SPARAM_3_DB_THRESHOLD <= s_param.db_value <= -3 - SPARAM_3_DB_THRESHOLD]

                left_frequency = max(left_frequency,
                                     min(frequencies_around_3db)) if frequencies_around_3db else frequency
                right_frequency = min(left_frequency,
                                      max(frequencies_around_3db)) if frequencies_around_3db else frequency

        s_params_dict["bandwidth"] = right_frequency - left_frequency
        s_params_dict["left_freq"] = left_frequency
        s_params_dict["right_freq"] = right_frequency

        s_params = from_dict(data_class=SParams, data=s_params_dict)

        csv_file = Path(S_PARAMS_CSV_FILE)
        csv_already_exists = csv_file.exists()

        with open(S_PARAMS_CSV_FILE, "a", newline='', encoding='utf-8') as f:
            w = DataclassWriter(f, [s_params], SParams)
            for key, value in S_PARAM_FIELD_TO_CLASS_FIELD.items():
                w.map(value).to(key)

            w.write(skip_header=csv_already_exists)
