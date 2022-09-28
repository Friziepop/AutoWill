import os

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
        path = os.path.join(self._params.out_path, "out.dxf")
        self._eq_manager.set_equation_value("EXPORT_PATH", f'"{path}"')
        # self._awrde.GlobalScripts('Import_Load_Pull_Files').Routines('Import_Load_Pull_Files').Run()
        self._awrde.Project.ProjectScripts("DXFExporter").Routines("Main").Run()
