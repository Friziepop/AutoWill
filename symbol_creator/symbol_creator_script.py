import math
import os
from symbol_creator.dxf_generator import DxfAwrGenerator
from symbol_creator.predictors import ModelPredictor, CsvPredictor, WidthPredictor, ConstPredictor
from symbol_creator.symbol_params import SymbolParams, SymbolGenerationParams
from materials.materials_db import MaterialDB

MODELS_DIR = "../learning/models"


def create(params: SymbolParams):
    material_db = MaterialDB(csv_path="../materials/materials_db.csv")
    height_predictor = ModelPredictor(models_dir=MODELS_DIR, model_feature="HEIGHT")
    thickness_predictor = CsvPredictor(material_db=material_db)
    quarter_predictor = ModelPredictor(models_dir=MODELS_DIR, model_feature="QUARTER")
    width_predictor = WidthPredictor(height_predictor=height_predictor, thickness_predictor=thickness_predictor, z0=50,
                                     material_db=material_db)
    rootwidth_predictor = WidthPredictor(height_predictor=height_predictor, thickness_predictor=thickness_predictor,
                                         z0=50 * math.sqrt(2),
                                         material_db=material_db)
    res_predictor = ConstPredictor(value=100.0)
    radius_predictor = ConstPredictor(value=0.5)

    print(f"height_predictor:{height_predictor.predict(symbol_input_params=params)}")
    print(f"thickness_predictor:{thickness_predictor.predict(symbol_input_params=params)}")
    print(f"quarter_predictor:{quarter_predictor.predict(symbol_input_params=params)}")
    print(f"width_predictor:{width_predictor.predict(symbol_input_params=params)}")
    print(f"rootwidth_predictor:{rootwidth_predictor.predict(symbol_input_params=params)}")
    print(f"res_predictor:{res_predictor.predict(symbol_input_params=params)}")
    print(f"radius_predictor:{radius_predictor.predict(symbol_input_params=params)}")

    dxf_params = SymbolGenerationParams(
        height=height_predictor.predict(symbol_input_params=params),
        thickness=thickness_predictor.predict(symbol_input_params=params),
        quarter=thickness_predictor.predict(symbol_input_params=params),
        width=width_predictor.predict(symbol_input_params=params),
        rootwidth=width_predictor.predict(symbol_input_params=params),
        res=res_predictor.predict(symbol_input_params=params),
        radius=radius_predictor.predict(symbol_input_params=params)
    )
    out_path = os.path.join(os.getcwd(), "out.dxf")
    print(f"Generating dxf file out:{out_path}")
    DxfAwrGenerator().generate(params=dxf_params, out_path=out_path)
    print("generation dxf")


if __name__ == '__main__':
    params = SymbolParams(material_id=1, frequency=10.0, bandwidth=0.5)
    create(params=params)
