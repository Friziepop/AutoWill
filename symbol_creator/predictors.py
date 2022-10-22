import pickle
from abc import ABC, abstractmethod

import numpy
import numpy as np

from microstip_freq_calc.utils import CalculationsUtils
from symbol_creator.symbol_params import SymbolParams
from learning.learnings_util import get_learning_model_name
from materials.materials_db import MaterialDB
from microstip_freq_calc.copied_calc import MicroStripCopiedCalc


class BasePredictor(ABC):
    def __init__(self):
        super(BasePredictor, self).__init__()

    @abstractmethod
    def predict(self, symbol_input_params: SymbolParams) -> float:
        pass


class ConstPredictor(BasePredictor):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def predict(self, symbol_input_params: SymbolParams) -> float:
        return self._value


class CsvPredictor(BasePredictor):
    def __init__(self, field: str):
        super(CsvPredictor, self).__init__()
        self._field = field

    def predict(self, symbol_input_params: SymbolParams) -> float:
        return getattr(symbol_input_params.material, self._field)


class WidthPredictor(BasePredictor):
    def __init__(self, height_predictor: BasePredictor, thickness_predictor: BasePredictor, z0: float):
        super(WidthPredictor, self).__init__()
        self._z0 = z0
        self._thickness_predictor = thickness_predictor
        self._height_predictor = height_predictor
        self._calculator = MicroStripCopiedCalc()

    def predict(self, symbol_input_params: SymbolParams) -> float:
        return self._calculator.calc(er=symbol_input_params.material.er,
                                     height=self._height_predictor.predict(symbol_input_params),
                                     thickness=self._thickness_predictor.predict(symbol_input_params), z0=self._z0,
                                     freq=symbol_input_params.frequency)


class ModelPredictor(BasePredictor):
    def __init__(self, models_dir: str, model_feature: str, material_db: MaterialDB):
        super(ModelPredictor, self).__init__()
        self._model_feature = model_feature
        self._models_dir = models_dir
        self._material_db = material_db

    def load_model(self, symbol_input_params: SymbolParams):
        model_path = get_learning_model_name(models_dir=self._models_dir, material_id=symbol_input_params.material.id,
                                             feature=self._model_feature)
        with open(model_path, "rb") as input_file:
            return pickle.load(input_file)

    def predict(self, symbol_input_params: SymbolParams) -> float:
        return self.load_model(symbol_input_params).predict(
            np.array([[symbol_input_params.frequency], [symbol_input_params.material.er],
                      [symbol_input_params.material.tanl]]))[0]


class InputPaddingPredictor(BasePredictor):
    def __init__(self, width_predictor: WidthPredictor, rootwidth_predictor: ModelPredictor):
        super(InputPaddingPredictor, self).__init__()
        self._width_predictor = width_predictor
        self._rootwidth_predictor = rootwidth_predictor

    def predict(self, symbol_input_params: SymbolParams) -> float:
        return CalculationsUtils.calculate_padding(resistor=symbol_input_params.material.resistor,
                                                   root_width=self._rootwidth_predictor.predict(symbol_input_params),
                                                   start_width=self._width_predictor.predict(symbol_input_params))


class PaddingPredictor(BasePredictor):
    def __init__(self, coefficient: float, input_padding_predictor: InputPaddingPredictor):
        super(PaddingPredictor, self).__init__()
        self._coefficient = coefficient
        self._input_padding_predictor = input_padding_predictor

    def predict(self, symbol_input_params: SymbolParams) -> float:
        return self._coefficient * (
                CalculationsUtils.extract_quarter_wavelength(frequency=symbol_input_params.frequency,
                                                             er=symbol_input_params.material.er) - self._input_padding_predictor.predict(
            symbol_input_params))
