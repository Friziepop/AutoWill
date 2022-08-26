import math
import pickle
from time import sleep
from typing import Dict

import numpy as np
import pandas as pd
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

# fr4_params = {
#     "prefix":"fr4","er": 4.4, "tanl": 0.018, "rho": 0.7, "height": 60, "thickness": 1.377952755905512, "z0": 50
# }
# ro4350_params = {
#         "prefix": "ro4350","er": 3.66, "tanl": 0.0037, "rho": 0.7, "height": 3.93701, "thickness": 0.039370079, "z0": 50
# }
from materials.material import Material
from materials.materials_db import MaterialDB
from microstip_freq_calc.copied_calc import MicroStripCopiedCalc

Z0 = 50
MILLS_TO_MM = 0.0254
MM_TO_MILS = 1 / MILLS_TO_MM


def extract(material: Material, step_size):
    dict_ans = {}
    dict_ans_root = {}
    freqs = [round(x, 1) for x in np.arange(material.start_freq, material.end_freq + step_size, step_size)]
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.microwaves101.com/calculators/1201-microstrip-calculator")
    sleep(2)
    er = driver.find_element(value="edt_msEr")
    er.clear()
    er.send_keys(material.er)
    tanl = driver.find_element(value="edt_msTand")
    tanl.clear()
    tanl.send_keys(material.tanl)
    rho = driver.find_element(value="edt_msRho")
    rho.clear()
    rho.send_keys(material.rho)
    freq_form = driver.find_element(value="edt_msFreq")

    height = driver.find_element(value="edt_msHeight")
    height.clear()
    height.send_keys(material.height * MM_TO_MILS)
    thickness = driver.find_element(value="edt_msThickness")
    thickness.clear()
    thickness.send_keys(material.thickness * MM_TO_MILS)

    zo = driver.find_element(value="edt_msZo")
    zo.clear()
    zo.send_keys(Z0)
    angle = driver.find_element(value="edt_msAngle")
    angle.clear()
    angle.send_keys(90)

    btn_sy = driver.find_element(value="btn_ms_synthesize")
    width = driver.find_element(value="edt_msWidth")
    for freq in tqdm(freqs):
        freq_form.clear()
        freq_form.send_keys(freq)
        btn_sy.click()
        sleep(0.1)
        val = float(width.get_attribute("value")) * MILLS_TO_MM
        dict_ans[f"{freq}"] = val

    with open(f'{material.name}_freq2width_dict.pickle', 'wb') as handle:
        pickle.dump(dict_ans, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # root
    print("now root")
    zo.clear()
    zo.send_keys(Z0 * math.sqrt(2))
    angle.clear()
    angle.send_keys(180)

    for freq in tqdm(freqs):
        freq_form.clear()
        freq_form.send_keys(freq)
        btn_sy.click()
        sleep(0.1)
        val = float(width.get_attribute("value")) * MILLS_TO_MM
        dict_ans_root[f"{freq}"] = val

    with open(f'{material.name}_freq2width_root_dict.pickle', 'wb') as handle:
        pickle.dump(dict_ans_root, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    materials = MaterialDB('../materials/materials_db.csv')
    material = materials.get_by_id(7)
    material.height = 0.0817161767152128
    MicroStripCopiedCalc().calc(material.er, material.height, material.thickness,
                                50, 20)
    print(MicroStripCopiedCalc().calc(material.er, material.height, material.thickness,
                                      50, 20))
    print(MicroStripCopiedCalc().calc(material.er, material.height, material.thickness,
                                      70.7, 20))

