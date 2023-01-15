import argparse
from pathlib import Path
from typing import List

import pandas as pd
from matplotlib import pyplot as plt

from learning.learners import InverseLearner, PolyLearner

CSV_DIR = "awr_optimizer"
MODELS_DIR = "learning/models"

X_COLS = ["frequency", "er", "tanl"]


def get_vars_path(mode: str, csv_dir: str = CSV_DIR):
    if mode == 'a':
        return f"vars.csv"
    if mode == 'tr':
        return f"vars_train.csv"
    if mode == 'v':
        return f"vars_val.csv"
    raise Exception("incorrect mode")


def extract_xy(csv_data_path: str, x_cols: List[str], y_col: str, material_id: int):
    df = pd.read_csv(filepath_or_buffer=csv_data_path, dtype={y_col: float})
    df = df[df["id"] == material_id]
    x_ls = []
    y = df[y_col].to_numpy()
    for x_col in x_cols:
        x_ls.append(df[x_col].to_numpy())
    return x_ls, y


def generate_test_validate(force_override: bool = True):
    if not force_override and Path(get_vars_path(mode='tr')):
        return
    df_all = pd.read_csv(get_vars_path(mode='a'))
    shuffled = df_all.sample(n=len(df_all))
    start_val = int(len(shuffled) * 0.9)
    shuffled.iloc[:start_val - 1].to_csv(get_vars_path(mode='tr'), index=False)
    shuffled.iloc[start_val:].to_csv(get_vars_path(mode='v'), index=False)

    print("created shuffled validation and train")


def learn_poly(degree: int, material_id: int, feature, vars_path: str, models_dir: str, show_graph: bool = False,
               save_model=True):
    generate_test_validate()
    poly = PolyLearner(degree=degree, material_id=material_id, models_dir=models_dir)
    x, y = extract_xy(vars_path, x_cols=X_COLS, y_col=feature, material_id=material_id)
    model = poly.train(x, y)
    if save_model:
        poly.save_model(feature=feature)
    if show_graph:
        poly.draw_graph(title=feature, y=y, x=x, x_label="TODO", feature=feature)
    return poly


def get_best_model(start_deg: int, end_deg: int, material_id: int, feature, models_dir: str, show_graph: bool = False):
    best_model_deg = 0
    best_model_score = -1
    for deg in range(start_deg, end_deg + 1):
        current_model = learn_poly(degree=deg, material_id=material_id, feature=feature,
                                   vars_path=get_vars_path(mode='tr'), models_dir=models_dir, save_model=False,
                                   show_graph=False)
        x, y = extract_xy(csv_data_path=get_vars_path(mode='v'), x_cols=X_COLS, y_col=feature, material_id=material_id)
        current_score = current_model.score(x, y)
        print(f"deg:{deg} score:{current_score}")
        if current_score > best_model_score:
            best_model_deg = deg
            best_model_score = current_score
    return learn_poly(degree=best_model_deg, material_id=material_id, feature=feature,
                      vars_path=get_vars_path(mode='a'), models_dir=models_dir, save_model=True,
                      show_graph=show_graph)


def learn_models(materials_ids: List[int], models_dir: str = MODELS_DIR,
                 show_graph: bool = False):
    for mat_id in materials_ids:
        print(f"learning models : [quarter,root_width] for material_id={mat_id} with parametrs :{X_COLS}")
        quarter_learner = InverseLearner(material_id=mat_id, model_dir=models_dir)

        x, y = extract_xy(get_vars_path(mode='a'), x_cols=X_COLS, y_col="quarter",material_id=mat_id)
        coeff_quarter = quarter_learner.train(x, y)
        quarter_learner.save_model(feature="quarter")

        '''
        if show_graph:
            quarter_learner.draw_graph(csv_data_path=path, title="quarter", x_cols=X_COLS,
                                       y_col="quarter",
                                       coefficients=coeff_quarter)
        '''

        get_best_model(start_deg=0, end_deg=2, material_id=mat_id, feature="root_width", show_graph=False,
                       models_dir=models_dir)


def main():

    show_graph = False
    parser = argparse.ArgumentParser()

    # -db DATABSE -u USERNAME -p PASSWORD -size 20
    parser.add_argument("-id", "--id", help="id of material", type=int)

    args = parser.parse_args()
    ids = [args.id] if args.id else [1]

    print("starting to learn models")
    learn_models(materials_ids=ids, show_graph=show_graph)
    if show_graph:
        plt.show()


if __name__ == '__main__':
    main()
