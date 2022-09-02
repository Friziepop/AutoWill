from awr_optimizer.awr_connector import AwrConnector
from awr_optimizer.awr_equation_manager import AwrEquationManager
from symbol_creator.symbol_params import SymbolGenerationParams


class DxfAwrGenerator(AwrConnector):
    def __init__(self):
        super(DxfAwrGenerator, self).__init__()
        self._eq_manager = AwrEquationManager()

    def connect(self):
        super(DxfAwrGenerator, self).connect()
        self._eq_manager.connect()

    def generate(self, out_path: str, params: SymbolGenerationParams):
        self.connect()
        self._eq_manager.set_equation_value("WIDTH", params.width)
        self._eq_manager.set_equation_value("ROOTWIDTH", params.rootwidth)
        self._eq_manager.set_equation_value("Res", params.res)
        self._eq_manager.set_equation_value("QUARTER", params.quarter)
        self._eq_manager.set_equation_value("RADIUS", params.radius)
        self._eq_manager.set_equation_value("HEIGHT", params.height)

        self._eq_manager.set_equation_value("EXPORT_PATH", f'"{out_path}"')
        #self._awrde.GlobalScripts('Import_Load_Pull_Files').Routines('Import_Load_Pull_Files').Run()
        self._awrde.Project.ProjectScripts("DXFExporter").Routines("Main").Run()
