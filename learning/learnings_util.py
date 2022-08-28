def get_learning_model_name(models_dir: str, material_id: int, input_name: str, output_name: str):
    return f"{models_dir}/{material_id}__{input_name}__{output_name}.pickle"
