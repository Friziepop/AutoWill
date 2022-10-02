from typing import List

from matplotlib import pyplot as plt

from learning.learners import InverseLearner, PolyLearner

CSV_DIR = "../awr_optimizer"
MODELS_DIR = "models"


def get_vars_path(csv_dir: str):
    return f"{csv_dir}/vars.csv"


def learn_poly(degree: int, material_id: int, feature, vars_path: str, models_dir: str, show_graph: bool = False):
    poly = PolyLearner(degree=degree, material_id=material_id, models_dir=models_dir)
    coeff = poly.train(vars_path, x_col="frequency", y_col=feature, save_model=True)
    if show_graph:
        poly.draw_graph(csv_data_path=vars_path, title=feature, x_col="frequency", y_col=feature,
                        coefficients=coeff)


def learn_models(materials_ids: List[int], csv_dir: str = CSV_DIR, models_dir: str = MODELS_DIR,
                 show_graph: bool = False):
    for mat_id in materials_ids:
        print(f"learning models : [quarter,height,width] for material_id={mat_id}")
        quarter_learner = InverseLearner(material_id=mat_id, model_dir=models_dir)
        vars_path = get_vars_path(csv_dir)
        coeff_quarter = quarter_learner.train(vars_path, x_col="frequency", y_col="quarter",
                                              save_model=True)
        if show_graph:
            quarter_learner.draw_graph(csv_data_path=vars_path, title="quarter", x_col="frequency",
                                       y_col="quarter",
                                       coefficients=coeff_quarter)
        learn_poly(degree=0, material_id=mat_id, feature="root_width", vars_path=vars_path, models_dir=models_dir,
                   show_graph=show_graph)


def main():
    show_graph = True
    ids = [2]
    print("starting to learn models")
    learn_models(materials_ids=ids, show_graph=show_graph)
    if show_graph:
        plt.show()


if __name__ == '__main__':
    main()
