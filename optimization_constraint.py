from typing import Optional


class OptimizationConstraint:
    def __init__(self, name: str, max: Optional[float], min: Optional[float], start: float):
        self.name = name
        self.max = max
        self.min = min
        self.start = start
        self.constrain = False
        if max and min:
            self.constrain = True

