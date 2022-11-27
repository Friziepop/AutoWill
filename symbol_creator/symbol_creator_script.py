
from symbol_creator import SymbolCreator

MODELS_DIR = "../learning/models"
MATERIALS_DB = "../materials/materials_db.csv"

if __name__ == '__main__':
    material_id = 5
    frequency = 5
    er = 3.66
    tanl = 0.0037
    symbol_creator = SymbolCreator()

    symbol_creator.create(material_id, frequency, er, tanl)
