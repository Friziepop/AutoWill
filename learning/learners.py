import numpy as np

from learning.base_learner import BaseLearner
import itertools


class InverseLearner(BaseLearner):
    def create_feature(self, x):
        bias_ones = np.ones(len(x))
        tmp = np.array([bias_ones, 1 / x])
        return tmp.T


class PolyLearner(BaseLearner):
    def __init__(self, material_id: int, degree: int, models_dir):
        super().__init__(material_id, models_dir)
        self._degree = degree

    def create_feature(self, x):
        numer_of_params = len(x)
        bias_ones = np.ones(len(x[0]))
        tmp = np.array([bias_ones])
        ls = [list(range(0, self._degree + 1) for i in range(numer_of_params))]
        all_deg_permutations = itertools.product(*ls)
        for degs in all_deg_permutations:
            x_tmp = 1
            for i in range(len(degs)):
                x_tmp = x_tmp * np.power(x[i], degs[i])
            tmp = np.vstack((tmp, x_tmp))

        return tmp.T
