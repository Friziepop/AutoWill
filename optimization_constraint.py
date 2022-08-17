from typing import Optional


class OptimizationConstraint:
    def __init__(self, name: str, max: Optional[float], min: Optional[float], start: float, should_optimize=True):
        self.name = name
        self.max = max
        self.min = min
        self.start = start
        self.should_optimize = should_optimize
        self.constrain = False
        if max and min:
            self.constrain = True
