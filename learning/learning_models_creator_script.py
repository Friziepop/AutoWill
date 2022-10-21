from pathlib import Path
from typing import List

import pandas as pd
from matplotlib import pyplot as plt

from learning.learners import InverseLearner, PolyLearner

CSV_DIR = "../awr_optimizer"
MODELS_DIR = "models"

X_COLS = ["frequency", "er", "tanl"]


def get_vars_path(mode: str, csv_dir: str = CSV_DIR):
    if mode == 'a':
        return f"{csv_dir}/vars.csv"
    if mode == 'tr':
        return f"{csv_dir}/vars_train.csv"
    if mode == 'v':
        return f"{csv_dir}/vars_val.csv"
    raise Exception("incorrect mode")


def generate_test_validate():
    if not Path(get_vars_path(mode='tr')).exists():
        df_all = pd.read_csv(get_vars_path(mode='a'))
        shuffled = df_all.sample(n=len(df_all))
        start_val = int(len(shuffled) * 0.9)
        shuffled.iloc[:start_val].to_csv(get_vars_path(mode='tr'))
        shuffled.iloc[start_val + 1:].to_csv(get_vars_path(mode='v'))


def learn_poly(degree: int, material_id: int, feature, vars_path: str, models_dir: str, show_graph: bool = False,
               save_model=True):
    generate_test_validate()
    poly = PolyLearner(degree=degree, material_id=material_id, models_dir=models_dir)
    model = poly.train(vars_path, x_cols=X_COLS, y_col=feature, save_model=save_model)
    if show_graph:
        poly.draw_graph(csv_data_path=vars_path, title=feature, x_cols=X_COLS, y_col=feature,
                        coefficients=model.coef_)
    return poly


def get_best_model(start_deg: int, end_deg: int, material_id: int, feature, models_dir: str, show_graph: bool = False):
    generate_test_validate()
    best_model_deg = 0
    best_model_score = -1
    for deg in range(start=start_deg, stop=end_deg):
        current_model = learn_poly(degree=deg, material_id=material_id, feature=feature,
                                   vars_path=get_vars_path(mode='tr'), models_dir=models_dir, save_model=False,
                                   show_graph=False)
        current_score = current_model.score(csv_data_path=get_vars_path(mode='v'), x_cols=X_COLS)
        print(f"deg:{deg} score:{current_score}")
        if current_score > best_model_score:
            best_model_deg = deg
            best_model_score = current_score
    return learn_poly(degree=best_model_deg, material_id=material_id, feature=feature,
                      vars_path=get_vars_path(mode='a'), models_dir=models_dir, save_model=True,
                      show_graph=show_graph)


def learn_models(materials_ids: List[int], csv_dir: str = CSV_DIR, models_dir: str = MODELS_DIR,
                 show_graph: bool = False):
    for mat_id in materials_ids:
        print(f"learning models : [quarter,height,width] for material_id={mat_id}")
        quarter_learner = InverseLearner(material_id=mat_id, model_dir=models_dir)
        vars_path = get_vars_path(csv_dir)
        coeff_quarter = quarter_learner.train(vars_path, x_cols=X_COLS, y_col="quarter",
                                              save_model=True)
        if show_graph:
            quarter_learner.draw_graph(csv_data_path=vars_path, title="quarter", x_cols=X_COLS,
                                       y_col="quarter",
                                       coefficients=coeff_quarter)
        get_best_model(start_deg=0, end_deg=2, material_id=mat_id, feature="root_width", show_graph=False,
                       models_dir=models_dir)


def main():
    show_graph = True
    ids = [5]
    print("starting to learn models")
    learn_models(materials_ids=ids, show_graph=show_graph)
    if show_graph:
        plt.show()


if __name__ == '__main__':
    main()
