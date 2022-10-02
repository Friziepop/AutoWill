import math
from scipy.constants import constants


class CalculationsUtils:
    @staticmethod
    def extract_quarter_wavelength(frequency: float, er: float) -> float:
        qua_meter = (constants.speed_of_light / (frequency * 10 ** 9 * math.sqrt(er))) / 4
        return qua_meter * 10 ** 3
