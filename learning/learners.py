import numpy as np

from learning.base_learner import BaseLearner


class InverseLearner(BaseLearner):
    def create_feature(self, x):
        bias_ones = np.ones(len(x))
        tmp = np.array([bias_ones, 1 / x])
        return tmp.T


class PolyLearner(BaseLearner):
    def __init__(self, material_id: int, degree: int):
        super().__init__(material_id)
        self._degree = degree

    def create_feature(self, x):
        bias_ones = np.ones(len(x))
        tmp = np.array([bias_ones])
        for deg in range(1, self._degree + 1):
            tmp = np.vstack((tmp, np.power(x, deg)))

        return tmp.T
