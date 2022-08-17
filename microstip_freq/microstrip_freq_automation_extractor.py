import pickle
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm


def main():
    # all unitr are in mills
    dict_ans = {}
    freqs = [round(0.1 * x, 1) for x in range(0, 1000)]
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.microwaves101.com/calculators/1201-microstrip-calculator")
    sleep(2)
    er = driver.find_element(value="edt_msEr")
    er.clear()
    er.send_keys(4.4)
    tanl = driver.find_element(value="edt_msTand")
    tanl.clear()
    tanl.send_keys(0.018)
    rho = driver.find_element(value="edt_msRho")
    rho.clear()
    rho.send_keys(0.7)
    freq_form = driver.find_element(value="edt_msFreq")

    height = driver.find_element(value="edt_msHeight")
    height.clear()
    height.send_keys(60)
    tanl = driver.find_element(value="edt_msThickness")
    tanl.clear()
    tanl.send_keys(1.377952755905512)

    zo = driver.find_element(value="edt_msZo")
    zo.clear()
    zo.send_keys(50)
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

    with open('freq2width_dict.pickle', 'wb') as handle:
        pickle.dump(dict_ans, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    # main()
    with open('freq2width_dict.pickle', 'rb') as handle:
        b_dict = pickle.load(handle)
        for key, val in b_dict.items():
            print(f"{key}:{val}")
