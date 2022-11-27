import math
import os
import subprocess
import uuid
from pathlib import Path

from jinja2 import Template

from symbol_params import FootprintParams


def format_float(val: float, num_digits: int):
    return f"{val:.{num_digits}}"


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
        template.globals["format"] = format_float

        tmp_pad_stack_macro_name = Path(os.getcwd()) / f"{uuid.uuid4()}__tmp.scr"
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
                                         PORT_1_PADDING=self._params.port_1_padding,
                                         OUTPUT_PADDING=self._params.output_padding,
                                         UPPER_MID_POINT=self._params.upper_mid_point,
                                         PADSTACK_MID_PADDING=self._params.padstack_padding,
                                         ANGLE=self._params.angle,
                                         PAD_A=self._params.pad_a,
                                         PAD_B=self._params.pad_b,
                                         PAD_STACK_SCRIPT=tmp_pad_stack_macro_name.name)
        tmp_name = Path(os.getcwd()) / f"{uuid.uuid4()}__tmp.scr"
        with open(tmp_name, "w") as f:
            f.write(compiled_macro)

        with open(self._params.pad_stack_macro_path, "r") as f:
            macro_content = f.read()

        template = Template(macro_content)
        compiled_macro = template.render(WIDTH=self._params.width)
        with open(tmp_pad_stack_macro_name, "w") as f:
            f.write(compiled_macro)

        subprocess.run(f"{self._params.allegro_exe_path} -orcad -s {tmp_name} {self._params.draw_path}".split())
