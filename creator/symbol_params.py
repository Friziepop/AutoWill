from dataclasses import dataclass


@dataclass
class SymbolParams:
    material_id: int
    frequency: float
    bandwidth: float


@dataclass
class SymbolGenerationParams:
    height: float
    thickness: float
    width: float
    rootwidth: float
    res: float
    radius: float
    quarter: float
