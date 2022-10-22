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

    def extract_xy(self, csv_data_path: str, x_cols: List[str], y_col: str):
        df = pd.read_csv(filepath_or_buffer=csv_data_path, dtype={y_col: float})
        df = df[df["id"] == self._material_id]
        x_ls = []
        y = df[y_col].to_numpy()
        for x_col in x_cols:
            x_ls.append(df[x_col].to_numpy())
        return x_ls, y

    def get_calculated_y(self, x, coefficients: List[float]):
        calculated_features = self.create_feature(x)
        return [row @ coefficients for row in calculated_features]

    def draw_graph(self, csv_data_path: str, title: str, x_cols: List[str], y_col: str, coefficients: List[float],
                   block=False):
        x, y = self.extract_xy(csv_data_path, x_cols, y_col)
        max_x = np.max(x) * 1.1
        max_y = np.max(y) * 1.1
        inerop_x = np.arange(0.00001, max_x, max_x / (10 * len(x)))
        calculated_y = self.get_calculated_y(x=inerop_x, coefficients=coefficients)
        # plot
        fig, ax = plt.subplots()
        ax.scatter(x, y, color='blue')
        ax.plot(inerop_x, calculated_y, color='red')

        ax.set(xlim=(0, max_x), xticks=np.arange(0, max_x, max_x / 10),
               ylim=(0, max_y), yticks=np.arange(0, max_y, max_y / 10))
        ax.set_ylabel(y_col)
        ax.set_xlabel(x_cols)
        ax.set_title(title)

        plt.show(block=block)

    def train(self, csv_data_path: str, x_cols: List[str], y_col: str, save_model: bool = False):
        # model = Pipeline([('poly', PolynomialFeatures(degree=self.degree)),
        #                   ('linear', LinearRegression(fit_intercept=False))])

        model = LinearRegression(fit_intercept=False)
        x, y = self.extract_xy(csv_data_path, x_cols, y_col)
        features = self.create_feature(x)
        model = model.fit(features, y)
        print(model.coef_)

        self._model = model

        if save_model:
            path = get_learning_model_name(models_dir=self._model_dir, material_id=self._material_id, input_name=x_cols,
                                           output_name=y_col)
            print(f"saving model: {path}")
            with open(path, 'wb') as handle:
                pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)


        return model

    def score(self, csv_data_path: str, x_cols: List[str], y_col: str):
        x, y = self.extract_xy(csv_data_path, x_cols, y_col)
        features = self.create_feature(x)
        return self._model.score(features, y)

    def predict(self, x):
        features = self.create_feature(x)
        return self._model.predict(features)
