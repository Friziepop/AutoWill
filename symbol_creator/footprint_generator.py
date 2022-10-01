import math
import os
import subprocess
import uuid
from pathlib import Path

from jinja2 import Template

from symbol_creator.symbol_params import FootprintParams


class FootprintGenerator:
    def __init__(self, params: FootprintParams):
        self._params = params

    def generate(self):
        with open(self._params.macro_path, "r") as f:
            macro_content = f.read()
        template = Template(macro_content)
        template.globals["cos"] = math.cos
        template.globals["sin"] = math.sin
        template.globals["radians"] = math.radians

        compiled_macro = template.render(DXF_FILE=self._params.dxf_file,
                                         DXF_MAPPING_FILE=self._params.dxf_mapping_file,
                                         MATERIAL_NAME_LOWER=
                                                        f"{self._params.material_name[0]}"
                                                        f"{self._params.material_name.lower()[1:]}",
                                         MATERIAL_NAME_UPPER=self._params.material_name.upper(),
                                         MATERIAL_ER=self._params.material_er,
                                         MATERIAL_TAN_L=self._params.material_tanl,
                                         MATERIAL_HEIGHT=self._params.material_height,
                                         PAD_NAME=self._params.pad_name,
                                         WIDTH=self._params.width,
                                         QUARTER=self._params.quarter,
                                         ROOTWIDTH=self._params.rootwidth,
                                         INPUT_PADDING=self._params.input_padding,
                                         UPPER_MID_POINT=self._params.upper_mid_point,
                                         PADSTACK_MID_PADDING=0.2,
                                         ANGLE=9.0000,
                                         PAD_B=self._params.pad_b)
        tmp_name = Path(os.getcwd()) / f"{uuid.uuid4()}__tmp.scr"
        with open(tmp_name, "w") as f:
            f.write(compiled_macro)
        subprocess.run(f"{self._params.allegro_exe_path} -orcad -s {tmp_name} {self._params.draw_path}".split())
