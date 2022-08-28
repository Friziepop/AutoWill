from creator.predictors import ModelPredictor, CsvPredictor, WidthPredictor
from creator.symbol_params import SymbolParams


def create(param: SymbolParams):
    height_predictor = ModelPredictor(model_path="")
    thickness_predictor = CsvPredictor(model_path="")
    quarter_predictor = ModelPredictor(model_path="")
    width_predictor = WidthPredictor(model_path="")


if __name__ == '__main__':

    pass
