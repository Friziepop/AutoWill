from typing import List, Optional

from materials.material import Material


class MaterialDB:
    def __init__(self, csv_path: Optional[str] = None):
        pass

    def get_by_id(self) -> Material:
        pass

    def get_by_name(self) -> List[Material]:
        pass
