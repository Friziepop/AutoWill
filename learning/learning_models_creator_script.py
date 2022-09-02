from matplotlib import pyplot as plt

from learning.learners import InverseLearner, PolyLearner


def main():
    learner = InverseLearner(material_id=1)
    coeff_quarter = learner.train("../vars.csv", x_col="frequency", y_col="QUARTER",save_model=True)
    learner.draw_graph(csv_data_path="../vars.csv", title="quarter", x_col="frequency", y_col="QUARTER",
                      coefficients=coeff_quarter)
    poly = PolyLearner(degree=1,material_id=1)
    coeff_half = poly.train("../vars.csv", x_col="frequency", y_col="HEIGHT",save_model=True)
    poly.draw_graph(csv_data_path="../vars.csv", title="height", x_col="frequency", y_col="HEIGHT",
                    coefficients=coeff_half)


if __name__ == '__main__':
    main()
    plt.show()
