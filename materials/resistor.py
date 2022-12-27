from dataclasses import dataclass


@dataclass
class Resistor:
    id: int
    name: str
    pad_name: str
    pad_a: float
    pad_b: float
    pad_c: float
    padstack_padding: float
    actual_res_pad: float
    description: str
