from copy import copy
from typing import Optional

from materials.csv_db import CSVDb
from materials.material import Material
from materials.resistors_db import ResistorDB

DEFAULT_DB_PATH = '../materials/materials_db.csv'


class MaterialDB(CSVDb):
    def __init__(self, csv_path: Optional[str] = None):
        csv_path = csv_path if csv_path else DEFAULT_DB_PATH
        super().__init__(csv_path=csv_path)

    def create(self, config_dict):
        resistor = ResistorDB().get_by_id(id=config_dict["resistor_id"])
        new_dict = copy(config_dict)
        new_dict["resistor"] = resistor
        del new_dict["resistor_id"]
        return Material(**new_dict)
