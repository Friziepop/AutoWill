from pathlib import Path
from typing import Dict, List

from pyawr_utils import awrde_utils

from dacite import from_dict

from pyawr_utils.common_utils import _Element

from dataclasses import dataclass

from dataclass_csv import DataclassWriter

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


@dataclass
class SParams:
    bandwidth: float
    frequency: float
    s_1_1: float
    s_2_2: float
    s_3_3: float
    s_3_1: float
    s_3_2: float
    s_2_1: float

    def __init__(self, bandwidth, frequency, s_1_1, s_2_2, s_3_3, s_3_1, s_3_2, s_2_1):
        self.bandwidth = bandwidth
        self.frequency = frequency
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
        self.equation_vars = {}


class Extractor:
    def __init__(self):
        self.awrde = None
        self.proj = None

    def connect(self):
        self.awrde = awrde_utils.establish_link()
        self.proj = awrde_utils.Project(self.awrde)

    def extract_results(self, frequency, bandwidth) -> ExtractionResult:
        result = ExtractionResult()

        for key, value in self.proj.graph_dict['Match'].measurements_dict.items():
            result.s_param_to_measurements[value.measurement_name] = \
                [SParam(measurement[0], measurement[1]) for measurement in value.trace_data[0]]

        for key, value in self.proj.graph_dict['Transmission'].measurements_dict.items():
            result.s_param_to_measurements[value.measurement_name] = \
                [SParam(measurement[0], measurement[1]) for measurement in value.trace_data[0]]

        result.circuit_vars = self.proj.circuit_schematics_dict['WilkinsonPowerDivider'].elements_dict
        result.equation_vars = self.proj.circuit_schematics_dict['WilkinsonPowerDivider'].equations_dict

        self.extract_s_params_to_csv(bandwidth, frequency, result)

        return result

    @staticmethod
    def extract_s_params_to_csv(bandwidth, frequency, result):
        s_params_dict = {"bandwidth": bandwidth, "frequency": frequency}
        for key, value in result.s_param_to_measurements.items():
            for s_param in value:
                if s_param.frequency == frequency:
                    s_params_dict[S_PARAM_FIELD_TO_CLASS_FIELD[key]] = s_param.db_value
                    break

        csv_file = Path(S_PARAMS_CSV_FILE)

        csv_already_exists = csv_file.exists()

        with open(S_PARAMS_CSV_FILE, "a", newline='', encoding='utf-8') as f:
            s_params = from_dict(data_class=SParams, data=s_params_dict)
            w = DataclassWriter(f, [s_params], SParams)
            for key, value in S_PARAM_FIELD_TO_CLASS_FIELD.items():
                w.map(value).to(key)

            w.write(skip_header=csv_already_exists)
