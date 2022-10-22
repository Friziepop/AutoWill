from typing import List


def get_learning_model_name(models_dir: str, material_id: int, feature:str):
    return f"{models_dir}/{material_id}__{feature}.pickle"
