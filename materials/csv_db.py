from abc import ABC

import pandas as pd


class CSVDb(ABC):
    def __init__(self, csv_path: str):
        materials_csv = pd.read_csv(csv_path)
        self._inner_materials_mapping = {}
        for config_dict in materials_csv.to_dict('records'):
            mat = self.create(config_dict)
            self._inner_materials_mapping[mat.id] = mat

    def create(self, config_dict):
        pass

    def get_by_id(self, id: int):
        return self._inner_materials_mapping[id]

    def get_by_name(self, name: str):
        return [mat for mat in self._inner_materials_mapping.values() if mat.name == name]

    def update_local_by_id(self, id: int, update_dict: dict):
        item = self.get_by_id(id=id)
        for key, val in update_dict.items():
            setattr(item, key, val)
