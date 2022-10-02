import pickle
from abc import ABC, abstractmethod

import numpy
import numpy as np

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
    def __init__(self, material_db: MaterialDB):
        super(CsvPredictor, self).__init__()
        self._material_db = material_db

    def predict(self, symbol_input_params: SymbolParams) -> float:
        mat = self._material_db.get_by_id(symbol_input_params.material_id)
        return mat.thickness


class ModelPredictor(BasePredictor):
    def __init__(self, models_dir: str, model_feature: str):
        super(ModelPredictor, self).__init__()
        self._model_feature = model_feature
        self._models_dir = models_dir

    def load_model(self, symbol_input_params: SymbolParams):
        model_path = get_learning_model_name(models_dir=self._models_dir, material_id=symbol_input_params.material_id,
                                             input_name="frequency",
                                             output_name=self._model_feature)
        with open(model_path, "rb") as input_file:
            return pickle.load(input_file)

    def predict(self, symbol_input_params: SymbolParams) -> float:
        return self.load_model(symbol_input_params).predict(np.array([symbol_input_params.frequency]))[0]


class WidthPredictor(BasePredictor):
    def __init__(self, height_predictor: BasePredictor, thickness_predictor: BasePredictor, z0: float,
                 material_db: MaterialDB):
        super(WidthPredictor, self).__init__()
        self._material_db = material_db
        self._z0 = z0
        self._thickness_predictor = thickness_predictor
        self._height_predictor = height_predictor
        self._calculator = MicroStripCopiedCalc()

    def predict(self, symbol_input_params: SymbolParams) -> float:
        mat = self._material_db.get_by_id(id=symbol_input_params.material_id)
        return self._calculator.calc(er=mat.er, height=self._height_predictor.predict(symbol_input_params),
                                     thickness=self._thickness_predictor.predict(symbol_input_params), z0=self._z0,
                                     freq=symbol_input_params.frequency)
