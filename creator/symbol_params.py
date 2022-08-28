from dataclasses import dataclass


@dataclass
class SymbolParams:
    material_id: int
    frequency: float
    bandwidth: float