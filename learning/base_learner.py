import pickle
from abc import ABC
from typing import List

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from learning.learnings_util import get_learning_model_name


class BaseLearner(ABC):
    def __init__(self, material_id: int, model_dir: str = "models"):
        self._model_dir = model_dir
        self._material_id = material_id
        self._model = None

    def create_feature(self, x):
        return np.array([x]).T

    def get_calculated_y(self, x, coefficients: List[float]):
        calculated_features = self.create_feature(x)
        return [row @ coefficients for row in calculated_features]

    # TODO: not done how to interop
    def draw_graph(self, title: str, x, y, feature: str, x_label: str, block=False):
        max_x = np.max(x) * 1.1
        max_y = np.max(y) * 1.1
        inerop_x = np.arange(0.00001, max_x, max_x / (10 * len(x)))
        calculated_y = self.get_calculated_y(x=inerop_x, coefficients=self._model.coef_)
        # plot
        fig, ax = plt.subplots()
        ax.scatter(x, y, color='blue')
        ax.plot(inerop_x, calculated_y, color='red')

        ax.set(xlim=(0, max_x), xticks=np.arange(0, max_x, max_x / 10),
               ylim=(0, max_y), yticks=np.arange(0, max_y, max_y / 10))
        ax.set_ylabel(feature)
        ax.set_xlabel(x_label)
        ax.set_title(title)

        plt.show(block=block)

    def train(self, x, y):
        model = LinearRegression(fit_intercept=False)
        features = self.create_feature(x)
        model = model.fit(features, y)
        print(model.coef_)

        self._model = model
        return model

    def save_model(self, feature: str):
        path = get_learning_model_name(models_dir=self._model_dir, material_id=self._material_id,
                                       feature=feature)
        print(f"saving model: {path}")
        with open(path, 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def score(self, x, y):
        features = self.create_feature(x)
        return self._model.score(features, y)

    def predict(self, x):
        features = self.create_feature(x)
        return self._model.predict(features)
