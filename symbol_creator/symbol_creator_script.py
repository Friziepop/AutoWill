import math
import os
from time import sleep

from materials.materials_db import MaterialDB
from symbol_creator.dxf_generator import DxfAwrGenerator
from symbol_creator.footprint_generator import FootprintGenerator
from symbol_creator.predictors import ModelPredictor, CsvPredictor, WidthPredictor, ConstPredictor, PaddingPredictor, \
    InputPaddingPredictor
from symbol_creator.symbol_params import SymbolParams, FootprintParams, DxfGenerationParams
from symbol_creator.wil_dxf_extractor import WilDxfExtractor

MODELS_DIR = "../learning/models"
MATERIALS_DB = "../materials/materials_db.csv"


def create(params: SymbolParams, models_dir: str = MODELS_DIR, materials_db: str = MATERIALS_DB):
    print(
        f"creating symbol for material_id:{params.material_id} , frequency:{params.frequency}, bandwidth:{params.bandwidth}")
    material_db = MaterialDB(csv_path=materials_db)

    material = material_db.get_by_id(params.material_id)

    height_predictor = CsvPredictor(material_db=material_db, field="height")
    thickness_predictor = CsvPredictor(material_db=material_db, field="thickness")
    quarter_predictor = ModelPredictor(models_dir=models_dir, model_feature="QUARTER")
    width_predictor = WidthPredictor(height_predictor=height_predictor, thickness_predictor=thickness_predictor, z0=50,
                                     material_db=material_db)
    calculated_rootwidth_predictor = WidthPredictor(height_predictor=height_predictor,
                                                    thickness_predictor=thickness_predictor,
                                                    z0=50 * math.sqrt(2),
                                                    material_db=material_db)

    rootwidth_predictor = ModelPredictor(models_dir=models_dir, model_feature="root_width")

    res_predictor = ConstPredictor(value=100.0)
    angle_predictor = ConstPredictor(value=9.0)

    port_1_padding_predictor = PaddingPredictor(coefficient=0.1, material_db=material_db)
    output_padding_predictor = PaddingPredictor(coefficient=0.5, material_db=material_db)
    input_padding_predictor = InputPaddingPredictor(rootwidth_predictor=calculated_rootwidth_predictor,
                                                    width_predictor=width_predictor, material_db=material_db)

    print(f"height_predictor:{height_predictor.predict(symbol_input_params=params)}")
    print(f"thickness_predictor:{thickness_predictor.predict(symbol_input_params=params)}")
    print(f"quarter_predictor:{quarter_predictor.predict(symbol_input_params=params)}")
    print(f"width_predictor:{width_predictor.predict(symbol_input_params=params)}")
    print(f"rootwidth_predictor:{rootwidth_predictor.predict(symbol_input_params=params)}")
    print(f"res_predictor:{res_predictor.predict(symbol_input_params=params)}")
    print(f"angle_predictor:{angle_predictor.predict(symbol_input_params=params)}")
    print(f"port_1_padding_predictor:{port_1_padding_predictor.predict(symbol_input_params=params)}")
    print(f"output_padding_predictor:{output_padding_predictor.predict(symbol_input_params=params)}")
    print(f"input_padding_predictor:{input_padding_predictor.predict(symbol_input_params=params)}")

    out_path = os.getcwd()

    dxf_params = DxfGenerationParams(
        height=height_predictor.predict(params),
        thickness=thickness_predictor.predict(params),
        quarter=quarter_predictor.predict(params),
        width=width_predictor.predict(params),
        rootwidth=rootwidth_predictor.predict(params),
        input_padding=input_padding_predictor.predict(params),
        port_1_padding=port_1_padding_predictor.predict(params),
        output_padding=output_padding_predictor.predict(params),
        res=res_predictor.predict(params),
        pad_a=material.resistor.pad_a,
        pad_b=material.resistor.pad_b,
        pad_c=material.resistor.pad_c,
        out_path=out_path,
        symbol_params=params,
    )

    print(f"Generating dxf file out:{out_path}")
    DxfAwrGenerator(params=dxf_params).generate()
    print("generated dxf")
    sleep(1)
    dxf_extractor = WilDxfExtractor(os.path.join(out_path, "out.dxf"))
    upper_mid_point = dxf_extractor.extract_layout_angle_mid()
    footprint_params = FootprintParams(
        macro_path="C:\\Users\\shvmo\\PycharmProjects\\AutoWill\\orcad\\pcb_automation\\wil_symbol_macro.scr",
        dxf_file=os.path.join(out_path, "out.dxf"),
        dxf_mapping_file="C:\\Users\\shvmo\\PycharmProjects\\AutoWill\\orcad\\pcb_automation\\resources\\mapping_setup.cnv",
        material_name=f"{material.name}-USER",
        pad_name=material.resistor.pad_name,  # "s_r28t30m38_40p28_30",
        material_er=material.er,
        material_tanl=material.tanl,
        draw_path="C:\\Users\\shvmo\\PycharmProjects\\AutoWill\\orcad\\package\\wil_sym.dra",
        allegro_exe_path="C:\\Cadence\\SPB_17.4\\tools\\bin\\allegro.exe",
        material_height=material.height,
        quarter=dxf_params.quarter,
        width=dxf_params.width,
        rootwidth=dxf_params.rootwidth,
        input_padding=dxf_params.input_padding,
        port_1_padding=dxf_params.port_1_padding,
        output_padding=dxf_params.output_padding,
        upper_mid_point=upper_mid_point,
        pad_b=material.resistor.pad_b,
        pad_a=material.resistor.pad_a,
        padstack_padding=material.resistor.padstack_padding,
        angle=angle_predictor.predict(params),
    )
    print(f"Generating symbol footprint")
    FootprintGenerator(params=footprint_params).generate()
    print("generated footprint")


if __name__ == '__main__':
    material_id = 2
    frequency = 20
    bandwidth = 1
    params = SymbolParams(material_id=material_id, frequency=frequency, bandwidth=bandwidth)
    create(params=params)
