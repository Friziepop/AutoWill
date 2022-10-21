from typing import List


def get_learning_model_name(models_dir: str, material_id: int, input_name: List[str], output_name: str):
    return f"{models_dir}/{material_id}__{input_name[0]}__{output_name}.pickle"
