import math
import pickle
from time import sleep
from typing import Dict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

fr4_params = {
    "prefix":"fr4","er": 4.4, "tanl": 0.018, "rho": 0.7, "height": 60, "thickness": 1.377952755905512, "z0": 50
}
ro4350_params = {
        "prefix": "ro4350","er": 3.66, "tanl": 0.0037, "rho": 0.7, "height": 3.93701, "thickness": 0.039370079, "z0": 50
}

def extract(config_dict: Dict):
    # all unitr are in mills
    dict_ans = {}
    dict_ans_root = {}
    freqs = [round(0.1 * x, 1) for x in range(0, 1000)]
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.microwaves101.com/calculators/1201-microstrip-calculator")
    sleep(2)
    er = driver.find_element(value="edt_msEr")
    er.clear()
    er.send_keys(config_dict["er"])
    tanl = driver.find_element(value="edt_msTand")
    tanl.clear()
    tanl.send_keys(config_dict["tanl"])
    rho = driver.find_element(value="edt_msRho")
    rho.clear()
    rho.send_keys(config_dict["rho"])
    freq_form = driver.find_element(value="edt_msFreq")

    height = driver.find_element(value="edt_msHeight")
    height.clear()
    height.send_keys(config_dict["height"])
    thickness = driver.find_element(value="edt_msThickness")
    thickness.clear()
    thickness.send_keys(config_dict["thickness"])

    zo = driver.find_element(value="edt_msZo")
    zo.clear()
    zo.send_keys(config_dict["z0"])
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
        val = float(width.get_attribute("value")) * 0.0254
        print(f"{freq}:{val}")
        dict_ans[f"{freq}"] = val

    with open(f'{config_dict["prefix"]}_freq2width_dict.pickle', 'wb') as handle:
        pickle.dump(dict_ans, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # root
    print("now root")
    zo.clear()
    zo.send_keys(config_dict["z0"] * math.sqrt(2))
    angle.clear()
    angle.send_keys(180)

    for freq in tqdm(freqs):
        freq_form.clear()
        freq_form.send_keys(freq)
        btn_sy.click()
        sleep(0.1)
        val = float(width.get_attribute("value")) * 0.0254
        print(f"{freq}:{val}")
        dict_ans[f"{freq}"] = val

    with open(f'{config_dict["prefix"]}_freq2width_root_dict.pickle', 'wb') as handle:
        pickle.dump(dict_ans_root, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    extract(config_dict=ro4350_params)
