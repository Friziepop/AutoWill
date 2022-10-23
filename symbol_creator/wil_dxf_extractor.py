from typing import Tuple

import ezdxf


class WilDxfExtractor:
    def __init__(self, wil_layout_file_path: str):
        self._doc = ezdxf.readfile(wil_layout_file_path)

    def extract_layout_angle_mid(self, extract_top=True) -> Tuple[float, float]:
        angle_ent = [ent for ent in list(self._doc.entities) if len(ent.vertices) ==5]
        if extract_top:
            chosen_ent = [ent for ent in angle_ent if ent.vertices[0].dxf.location.y > 0][0]
        else:
            chosen_ent = [ent for ent in angle_ent if ent.vertices[0].dxf.location.y < 0][0]

        return (chosen_ent.vertices[1].dxf.location.x + chosen_ent.vertices[2].dxf.location.x) / 2, (
                chosen_ent.vertices[1].dxf.location.y + chosen_ent.vertices[2].dxf.location.y) / 2
