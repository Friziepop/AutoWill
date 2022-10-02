import math
from scipy.constants import constants

from materials.resistor import Resistor


class CalculationsUtils:
    @staticmethod
    def extract_quarter_wavelength(frequency: float, er: float) -> float:
        qua_meter = (constants.speed_of_light / (frequency * 10 ** 9 * math.sqrt(er))) / 4
        return qua_meter * 10 ** 3

    @staticmethod
    def calculate_padding(resistor: Resistor, root_width: float, start_width: float):
        return (2 * resistor.pad_b + resistor.pad_c + 2 * root_width - start_width) / 2
