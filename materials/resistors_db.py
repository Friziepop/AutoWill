from typing import Optional

from materials.csv_db import CSVDb
from materials.resistor import Resistor

DEFAULT_DB_PATH = '../materials/resistors_db.csv'


class ResistorDB(CSVDb):
    def __init__(self, csv_path: Optional[str] = None):
        csv_path = csv_path if csv_path else DEFAULT_DB_PATH
        super().__init__(csv_path=csv_path,dtypes={'name':str})

    def create(self, config_dict):
        return Resistor(**config_dict)
