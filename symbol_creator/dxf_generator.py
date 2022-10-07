import os

import numpy as np

from awr_optimizer.awr_connector import AwrConnector
from awr_optimizer.awr_equation_manager import AwrEquationManager
from symbol_creator.symbol_params import DxfGenerationParams


class DxfAwrGenerator(AwrConnector):
    def __init__(self, params: DxfGenerationParams):
        super(DxfAwrGenerator, self).__init__()
        self._eq_manager = AwrEquationManager()
        self._params = params

    def connect(self):
        super(DxfAwrGenerator, self).connect()
        self._eq_manager.connect()

    def generate(self):
        self.connect()
        self._eq_manager.set_equation_value("WIDTH", self._params.width)
        self._eq_manager.set_equation_value("ROOTWIDTH", self._params.rootwidth)
        self._eq_manager.set_equation_value("Res", self._params.res)
        self._eq_manager.set_equation_value("QUARTER", self._params.quarter)
        self._eq_manager.set_equation_value("HEIGHT", self._params.height)
        self._eq_manager.set_equation_value("PAD_A", self._params.pad_a)
        self._eq_manager.set_equation_value("PAD_B", self._params.pad_b)
        self._eq_manager.set_equation_value("PAD_C", self._params.pad_c)
        self._eq_manager.set_equation_value("INPUT_PADDING", self._params.input_padding)
        self._eq_manager.set_equation_value("OUTPUT_PADDING", self._params.output_padding)
        self._eq_manager.set_equation_value("PORT_1_PADDING", self._params.port_1_padding)
        path = os.path.join(self._params.out_path, "out.dxf")
        self._eq_manager.set_equation_value("EXPORT_PATH", f'"{path}"')
        # self._awrde.GlobalScripts('Import_Load_Pull_Files').Routines('Import_Load_Pull_Files').Run()
        self._awrde.Project.ProjectScripts("DXFExporter").Routines("Main").Run()

        freq_array = np.linspace(self._params.symbol_params.frequency - self._params.symbol_params.bandwidth / 2,
                                 self._params.symbol_params.frequency + self._params.symbol_params.bandwidth / 2, 5)
        self._proj.set_project_frequencies(project_freq_ay=freq_array, units_str='GHz')
