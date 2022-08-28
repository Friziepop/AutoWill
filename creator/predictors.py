import pickle
from abc import ABC, abstractmethod

from creator.symbol_params import SymbolParams
from materials.materials_db import MaterialDB
from microstip_freq_calc.copied_calc import MicroStripCopiedCalc


class BasePredictor(ABC):
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
    def __init__(self, model_path: str):
        super(ModelPredictor, self).__init__()
        with open(model_path, "rb") as input_file:
            self.model = pickle.load(input_file)

    def predict(self, symbol_input_params: SymbolParams) -> float:
        return self.model.predict([symbol_input_params.frequency])


class WidthPredictor(BasePredictor):
    def __init__(self, height_predictor: BasePredictor, thickness_predictor: BasePredictor, z0: float,
                 material_db: MaterialDB):
        super.__init__()
        self.material_db = material_db
        self.z0 = z0
        self.thickness_predictor = thickness_predictor
        self.height_predictor = height_predictor
        self.calculator = MicroStripCopiedCalc()

    @abstractmethod
    def predict(self, symbol_input_params: SymbolParams) -> float:
        mat = self.material_db.get_by_id(id=symbol_input_params.material_id)
        return self.calculator.calc(er=mat.er, height=self.height_predictor.predict(symbol_input_params),
                                    thickness=self.thickness_predictor.predict(symbol_input_params), z0=self.z0,
                                    freq=symbol_input_params.frequency)
