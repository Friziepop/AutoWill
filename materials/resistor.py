from dataclasses import dataclass


@dataclass
class Resistor:
    id: int
    name: str
    pad_name: str
    pad_a: float
    pad_b: float
    pad_c: float
    padstck_padding: float
    description: str
