from typing import List

from matplotlib import pyplot as plt

from learning.learners import InverseLearner, PolyLearner


def get_vars_path(csv_dir: str):
    return f"{csv_dir}/vars.csv"


def learn_poly(degree: int, material_id: int, feature, vars_path: str, show_graph: bool = False):
    poly = PolyLearner(degree=degree, material_id=material_id)
    coeff = poly.train(vars_path, x_col="frequency", y_col=feature, save_model=True)
    if show_graph:
        poly.draw_graph(csv_data_path=vars_path, title=feature, x_col="frequency", y_col=feature,
                        coefficients=coeff)


def learn_models(materials_ids: List[int], csv_dir: str, show_graph: bool = False):
    for mat_id in materials_ids:
        print(f"learning models : [QUARTER,HEIGHT,WIDTH] for material_id={mat_id}")
        quarter_learner = InverseLearner(material_id=1)
        vars_path = get_vars_path(csv_dir)
        coeff_quarter = quarter_learner.train(vars_path, x_col="frequency", y_col="QUARTER",
                                              save_model=True)
        if show_graph:
            quarter_learner.draw_graph(csv_data_path=vars_path, title="quarter", x_col="frequency",
                                       y_col="QUARTER",
                                       coefficients=coeff_quarter)
        learn_poly(degree=1, material_id=mat_id, feature="HEIGHT", vars_path=vars_path, show_graph=show_graph)
        learn_poly(degree=1, material_id=mat_id, feature="WIDTH", vars_path=vars_path, show_graph=show_graph)


def main():
    csv_dir = "../"
    show_graph = True
    ids = [1]
    print("starting to learn models")
    learn_models(materials_ids=ids, show_graph=show_graph, csv_dir=csv_dir)
    if show_graph:
        plt.show()


if __name__ == '__main__':
    main()

