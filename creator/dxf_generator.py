from awr_optimizer.awr_connector import AwrConnector
from awr_optimizer.awr_equation_manager import AwrEquationManager


class DxfAwrGenerator(AwrConnector):
    def __init__(self):
        super(DxfAwrGenerator, self).__init__()
        self._eq_manager = AwrEquationManager()

    def connect(self):
        super(DxfAwrGenerator, self).connect()
        self._eq_manager.connect()

    def generate(self, out_path: str):
        self.connect()
        self._eq_manager.set_equation_value("EXPORT_PATH", out_path)
        self._awrde.GlobalScripts('Import_Load_Pull_Files').Routines('Import_Load_Pull_Files').Run()

