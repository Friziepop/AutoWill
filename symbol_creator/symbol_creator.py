import os
from copy import deepcopy
from pathlib import Path
from time import sleep

from materials.materials_db import MaterialDB
from predictors import CsvPredictor, WidthPredictor, ModelPredictor, ConstPredictor, \
    InputPaddingPredictor, PaddingPredictor
from dxf_generator import DxfAwrGenerator
from footprint_generator import FootprintGenerator
from wil_dxf_extractor import WilDxfExtractor
from symbol_params import SymbolParams, DxfGenerationParams, FootprintParams

MODELS_DIR = "../learning/models"
MATERIALS_DB = "../materials/materials_db.csv"


class SymbolCreator:
    def __init__(self):
        pass

    def _create(self, params: SymbolParams, models_dir: str = MODELS_DIR):
        print(
            f"creating symbol for material_id:{params.material.id} , frequency:{params.frequency},er:{params.material.er} , tanl:{params.material.tanl} bandwidth:{params.bandwidth}")

        height_predictor = CsvPredictor(field="height")
        thickness_predictor = CsvPredictor(field="thickness")
        quarter_predictor = ModelPredictor(models_dir=models_dir, model_feature="quarter")
        width_predictor = WidthPredictor(height_predictor=height_predictor, thickness_predictor=thickness_predictor,
                                         z0=50)

        rootwidth_predictor = ModelPredictor(models_dir=models_dir, model_feature="root_width")

        res_predictor = ConstPredictor(value=100.0)
        angle_predictor = ConstPredictor(value=45)

        input_padding_predictor = InputPaddingPredictor(rootwidth_predictor=rootwidth_predictor,
                                                        width_predictor=width_predictor)
        port_1_padding_predictor = PaddingPredictor(coefficient=0.1, input_padding_predictor=input_padding_predictor)
        output_padding_predictor = PaddingPredictor(coefficient=0.1, input_padding_predictor=input_padding_predictor)

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
            er=params.material.er,
            tanl=params.material.tanl,
            height=height_predictor.predict(params),
            thickness=thickness_predictor.predict(params),
            quarter=quarter_predictor.predict(params),
            width=width_predictor.predict(params),
            rootwidth=rootwidth_predictor.predict(params),
            input_padding=input_padding_predictor.predict(params),
            port_1_padding=port_1_padding_predictor.predict(params),
            output_padding=output_padding_predictor.predict(params),
            res=res_predictor.predict(params),
            pad_a=params.material.resistor.pad_a,
            pad_b=params.material.resistor.pad_b,
            pad_c=params.material.resistor.pad_c,
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
            macro_path=str(Path(os.getcwd()).parent / "orcad/pcb_automation/wil_symbol_macro.scr"),
            pad_stack_macro_path=str(Path(os.getcwd()).parent / "orcad/pcb_automation/padstack_change.scr"),
            dxf_file=os.path.join(out_path, "out.dxf"),
            dxf_mapping_file=str(Path(os.getcwd()).parent / "orcad/pcb_automation/resources/mapping_setup.cnv"),
            material_name=f"{params.material.name}-USER",
            pad_name=params.material.resistor.pad_name,  # "s_r28t30m38_40p28_30",
            material_er=params.material.er,
            material_tanl=params.material.tanl,
            draw_path=str(Path(os.getcwd()).parent / "orcad/package/wil_sym.dra"),
            allegro_exe_path="C:\\Cadence\\SPB_17.4\\tools\\bin\\allegro.exe",
            material_height=params.material.height,
            quarter=dxf_params.quarter,
            width=dxf_params.width,
            rootwidth=dxf_params.rootwidth,
            input_padding=dxf_params.input_padding,
            port_1_padding=dxf_params.port_1_padding,
            output_padding=dxf_params.output_padding,
            upper_mid_point=upper_mid_point,
            pad_b=params.material.resistor.pad_b,
            pad_a=params.material.resistor.actual_res_pad,
            padstack_padding=params.material.resistor.padstack_padding,
            angle=angle_predictor.predict(params),
        )
        print(f"Generating symbol footprint")
        FootprintGenerator(params=footprint_params).generate()
        print("generated footprint")

    def create(self, material_id: int, frequency: float, er: float, tanl: float):
        material_db = MaterialDB(csv_path=MATERIALS_DB)

        mat = deepcopy(material_db.get_by_id(material_id))
        mat.er = er
        mat.tanl = tanl
        bandwidth = frequency / 15

        params = SymbolParams(material=mat, frequency=frequency, bandwidth=bandwidth)

        self._create(params=params)
