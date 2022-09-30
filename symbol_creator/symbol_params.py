from dataclasses import dataclass
from typing import Tuple


@dataclass
class SymbolParams:
    material_id: int
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
    out_path: str


@dataclass
class FootprintParams:
    macro_path: str
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
    upper_mid_point: Tuple[float, float]
