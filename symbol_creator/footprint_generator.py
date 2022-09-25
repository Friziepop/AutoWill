import subprocess
import uuid

from symbol_creator.symbol_params import FootprintParams


class FootprintGenerator:
    def __init__(self, params: FootprintParams):
        self._params = params

    def generate(self):
        macro_content = None
        with open(self._params.macro_path, "r") as f:
            macro_content = f.read()
        compiled_macro = macro_content.format(DXF_FILE=self._params.dxf_file,
                                              DXF_MAPPING_FILE=self._params.dxf_mapping_file,
                                              MATERIAL_NAME_LOWER=self._params.material_name.lower(),
                                              MATERIAL_NAME_UPPER=self._params.material_name.upper(),
                                              MATERIAL_ER=self._params.material_er,
                                              MATERIAL_TAN_L=self._params.material_tanl, PAD_NAME=self._params.pad_name)
        tmp_name = f"{uuid.uuid4()}__tmp.scr"
        with open(tmp_name, "w") as f:
            f.write(compiled_macro)
        subprocess.run(f"allegro.exe -orcad -s {tmp_name} {self._params.draw_path}".split())
