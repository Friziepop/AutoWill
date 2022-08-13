from typing import Dict, List

from pyawr_utils import awrde_utils

from dataclasses import dataclass

from pyawr_utils.common_utils import _Element


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

    def extract_results(self) -> ExtractionResult:
        result = ExtractionResult()

        for key, value in self.proj.graph_dict['Match'].measurements_dict.items():
            result.s_param_to_measurements[value.measurement_name] = \
                [SParam(measurement[0], measurement[1]) for measurement in value.trace_data[0]]

        for key, value in self.proj.graph_dict['Transmission'].measurements_dict.items():
            result.s_param_to_measurements[value.measurement_name] = \
                [SParam(measurement[0], measurement[1]) for measurement in value.trace_data[0]]

        result.circuit_vars = self.proj.circuit_schematics_dict['WilkinsonPowerDivider'].elements_dict
        result.equation_vars = self.proj.circuit_schematics_dict['WilkinsonPowerDivider'].equations_dict

        return result
