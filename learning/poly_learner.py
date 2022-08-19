from typing import List

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class LinearLearner:

    def __init__(self):
        self.degree = 1

    def extract_xy(self, csv_data_path: str, x_col: str, y_col: str):
        df = pd.read_csv(filepath_or_buffer=csv_data_path, dtype={x_col: float, y_col: float})
        x = df[x_col].to_numpy()
        y = df[y_col].to_numpy()
        return x, y

    def create_feature(self, x):
        bias_ones = np.ones(len(x))
        tmp = np.array([bias_ones, 1 / x])
        return tmp.T

    def get_calculated_y(self, x, coefficients: List[float]):
        calculated_features = self.create_feature(x)
        return [row @ coefficients for row in calculated_features]

    def draw_graph(self, csv_data_path: str, x_col: str, y_col: str, coefficients: List[float]):
        x, y = self.extract_xy(csv_data_path, x_col, y_col)
        calculated_y = self.get_calculated_y(x=x, coefficients=coefficients)
        # plot
        fig, ax = plt.subplots()
        ax.scatter(x, y,color='blue')
        ax.plot(x, calculated_y,color='red')

        ax.set(xlim=(0, 20), xticks=np.arange(1, 30),
               ylim=(0, 20), yticks=np.arange(1, 50))
        ax.set_ylabel(y_col)
        ax.set_xlabel(x_col)

        plt.show()

    def train(self, csv_data_path: str, x_col: str, y_col: str):
        # model = Pipeline([('poly', PolynomialFeatures(degree=self.degree)),
        #                   ('linear', LinearRegression(fit_intercept=False))])

        model = LinearRegression(fit_intercept=False)
        x, y = self.extract_xy(csv_data_path, x_col, y_col)
        features = self.create_feature(x)
        model = model.fit(features, y)
        print(model.coef_)

        return model.coef_


learner = LinearLearner()
coeff = learner.train("../vars.csv", x_col="frequency", y_col="QUARTER")
learner.draw_graph("../vars.csv", x_col="frequency", y_col="QUARTER", coefficients=coeff)
