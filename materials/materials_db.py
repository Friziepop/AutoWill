from typing import List, Optional

import pandas as pd

from materials.material import Material

DEFAULT_DB_PATH = '../materials/materials_db.csv'


class MaterialDB:
    def __init__(self, csv_path: Optional[str] = None):
        csv_path = csv_path if csv_path else DEFAULT_DB_PATH
        materials_csv = pd.read_csv(csv_path)
        self._inner_materials_mapping = {}
        for config_dict in materials_csv.to_dict('records'):
            mat = Material(**config_dict)
            self._inner_materials_mapping[mat.id] = mat

    def get_by_id(self, material_id: int) -> Material:
        return self._inner_materials_mapping[material_id]

    def get_by_name(self, name: str) -> List[Material]:
        return [mat for mat in self._inner_materials_mapping.values() if mat.name == name]
