from dataclasses import dataclass
from typing import Tuple

from materials.material import Material


@dataclass
class SymbolParams:
    material: Material
    frequency: float
    bandwidth: float


@dataclass
class DxfGenerationParams:
    height: float
    thickness: float
    width: float
    rootwidth: float
    res: float
    quarter: float
    port_1_padding: float
    output_padding: float
    input_padding: float
    pad_a: float
    pad_b: float
    pad_c: float
    out_path: str
    symbol_params: SymbolParams


@dataclass
class FootprintParams:
    macro_path: str
    pad_stack_macro_path: str
    dxf_file: str
    dxf_mapping_file: str
    material_name: str
    pad_name: str
    material_er: float
    material_height: float
    material_tanl: float
    draw_path: str
    allegro_exe_path: str
    quarter: float
    rootwidth: float
    width: float
    input_padding: float
    port_1_padding: float
    output_padding: float
    upper_mid_point: Tuple[float, float]
    pad_a: float
    pad_b: float
    padstack_padding: float
    angle: float
