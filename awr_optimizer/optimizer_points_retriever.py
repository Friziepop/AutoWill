# MATERIALS_DB_CSV_PATH = "materials/materials_db.csv"
from typing import List, Tuple

import numpy as np

from materials.material import Material


class OptimizerPointsRetriever:
    def __init__(self, material: Material):
        # TODO:change to mat
        self._permutations = self._create_permutations(freq_start=2, freq_end=4, freq_points=5,
                                                       er_start=material.er - 0.3,
                                                       er_end=material.er + 0.3, er_points=5,
                                                       tanl_start=material.tanl - 0.001,
                                                       tanl_end=material.tanl + 0.001, tanl_points=2)

    def _create_permutations(self, freq_start, freq_end, freq_points: int, er_start, er_end, er_points: int, tanl_start,
                             tanl_end, tanl_points: int) -> List[Tuple[float, float, float]]:
        freq_ls = list(np.linspace(start=freq_start, stop=freq_end, num=freq_points))
        tanl_ls = list(np.linspace(start=tanl_start, stop=tanl_end, num=tanl_points))
        er_ls = list(np.linspace(start=er_start, stop=er_end, num=er_points))
        return [(i, j, k) for i in freq_ls for j in er_ls for k in tanl_ls]

    def get_points(self):
        return self._permutations
