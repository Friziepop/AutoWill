from awr_connector import AwrConnector
from optimization_constraint import OptimizationConstraint


class AwrEquationManager(AwrConnector):
    def __init__(self):
        super(AwrEquationManager, self).__init__()

    def connect(self):
        super(AwrEquationManager, self).connect()

    def _eq_to_dict(self):
        return {eq.equation_name: eq for key, eq in
                self._proj.circuit_schematics_dict['WilkinsonPowerDivider'].equations_dict.items()}

    def set_equation_value(self, eq_name, eq_val):
        self._eq_to_dict()[eq_name].equation_value = eq_val

    def get_equation_by_name(self, name: str):
        return self._eq_to_dict()[name]

    def set_constraint(self, con: OptimizationConstraint):
        eq = self._eq_to_dict()[con.name]
        eq.optimize_enabled = con.should_optimize
        eq.lower_constraint = con.min if con.min else 0
        eq.upper_constraint = con.max if con.max else 10 ^ 6
        eq.constrain = con.constrain
        eq.equation_value = str(con.start)

    def disable_opt_all(self):
        for key, eq in self._eq_to_dict().items():
            eq.optimize_enabled = False
