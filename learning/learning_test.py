from matplotlib import pyplot as plt

from learning.learners import InverseLearner, PolyLearner


def main():
    #learner = InverseLearner()
    #coeff_quarter = learner.train("../vars.csv", x_col="frequency", y_col="QUARTER")
    #learner.draw_graph(csv_data_path="../vars.csv", title="quarter", x_col="frequency", y_col="QUARTER",
    #                   coefficients=coeff_quarter)
    poly = PolyLearner(degree=5)
    coeff_half = poly.train("../vars.csv", x_col="frequency", y_col="HEIGHT")
    poly.draw_graph(csv_data_path="../vars.csv", title="half", x_col="frequency", y_col="HEIGHT",
                    coefficients=coeff_half)



if __name__ == '__main__':
    main()
    plt.show()
