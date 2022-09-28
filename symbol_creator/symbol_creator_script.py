import os

from materials.materials_db import MaterialDB
from symbol_creator.dxf_generator import DxfAwrGenerator
from symbol_creator.footprint_generator import FootprintGenerator
from symbol_creator.symbol_params import SymbolParams, FootprintParams, DxfGenerationParams

MODELS_DIR = "../learning/models"
MATERIALS_DB = "../materials/materials_db.csv"


def create(params: SymbolParams, models_dir: str = MODELS_DIR, materials_db: str = MATERIALS_DB):
    print(
        f"creating symbol for material_id:{params.material_id} , frequency:{params.frequency}, bandwidth:{params.bandwidth}")
    material_db = MaterialDB(csv_path=materials_db)

    material = material_db.get_by_id(params.material_id)

    '''
    height_predictor = ModelPredictor(models_dir=models_dir, model_feature="HEIGHT")
    thickness_predictor = CsvPredictor(material_db=material_db)
    quarter_predictor = ModelPredictor(models_dir=models_dir, model_feature="QUARTER")
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
    
    '''

    out_path = os.getcwd()

    dxf_params = DxfGenerationParams(
        height=0.1,
        thickness=0.01,
        quarter= 3.1176007026386072,
        width= 0.20863645369886577,
        rootwidth= 0.10838520376208859,
        res=100,
        out_path=out_path,
    )

    footprint_params = FootprintParams(
        macro_path="C:\\Users\\shvmo\\PycharmProjects\\AutoWill\\orcad\\pcb_automation\\wil_symbol_macro.scr",
        dxf_file=os.path.join(out_path, "out.dxf"),
        dxf_mapping_file="C:\\Users\\shvmo\\PycharmProjects\\AutoWill\\orcad\\pcb_automation\\resources\\mapping_setup.cnv",
        material_name=material.name,
        pad_name="s_r28t30m38_40p28_30",
        material_er=material.er,
        material_tanl=material.tanl,
        draw_path="C:\\Users\\shvmo\\PycharmProjects\\AutoWill\\orcad\\package\\wil_sym.dra",
        allegro_exe_path="C:\\Cadence\\SPB_17.4\\tools\\bin\\allegro.exe",
        material_height=material.height
    )
    print(f"Generating dxf file out:{out_path}")
    DxfAwrGenerator(params=dxf_params).generate()
    print("generated dxf")
    print(f"Generating symbol footprint")
    FootprintGenerator(params=footprint_params).generate()
    print("generated footprint")


if __name__ == '__main__':
    material_id = 1
    frequency = 10.0
    bandwidth = 0.5
    params = SymbolParams(material_id=material_id, frequency=frequency, bandwidth=bandwidth)
    create(params=params)
