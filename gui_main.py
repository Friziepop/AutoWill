import shutil
from threading import Thread
from typing import List

import PySimpleGUI as sg

from materials.material import Material
from materials.materials_db import MaterialDB
from symbol_creator.symbol_creator import SymbolCreator

MATERIALS_DB = "./materials/materials_db.csv"


def copy_files(pad_name: str, dst_path: str):
    shutil.copy2(src="orcad/io/ioport.pad", dst=dst_path)
    shutil.copy2(src=f"../orcad/resistor/{pad_name}.pad", dst=dst_path)
    shutil.copy2(src=f"orcad/package/wil_sym.dra", dst=dst_path)
    shutil.copy2(src=f"orcad/package/wil_sym.psm", dst=dst_path)


def run_script(mat_id: int, freq: float, er: float, tanl: float):
    SymbolCreator().create(material_id=mat_id, frequency=freq,
                           er=er, tanl=tanl)


def get_material_match(mat_name: str, resistor_name: str):
    possible_matches = [mat for mat in materials if
                        mat.name == mat_name and mat.resistor.name == resistor_name]
    if len(possible_matches) != 1:
        raise Exception("Error matching material")
    return possible_matches[0]


material_db = MaterialDB(MATERIALS_DB)
materials: List[Material] = material_db.get_all()

all_resistors_names = list(set([mat.resistor.name for mat in materials]))
materials_names = list(set([mat.name for mat in materials]))

resistor_names = all_resistors_names

sg.theme("Dark")
# Define the window's contents
layout = [
    [sg.Text("Enter frequency [GHZ]"), sg.Input(key='-FREQUENCY-')],
    [sg.Text("Enter material"),
     sg.Combo(materials_names, key='-MATERIAL_NAME-', readonly=True, change_submits=True)],
    [sg.Text("Enter resistor"), sg.Combo(resistor_names, key='-RESISTOR_NAME-', readonly=True, change_submits=True)],
    [sg.Text("Enter e_r"), sg.Input(key='-E_R-')],
    [sg.Text("Enter tanl"), sg.Input(key='-TANL-')],
    [sg.Text('Select a folder:'), sg.In(key='-DST_FOLDER-'), sg.FolderBrowse("Select")],
    [sg.Multiline(size=(50, 10), key='-OUTPUT-', reroute_stdout=True),
     sg.StatusBar("done", background_color="green", text_color="black", key="-STATUS_BAR-")],
    [sg.Button('Ok')]]

# Create the window
window = sg.Window('Symbol creator', layout)
ryn_script_thread = Thread(target=run_script, args=window)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read(timeout=1000)
    # See if user wants to quit or window was closed
    if event in ('4 quit', sg.WIN_CLOSED):
        break
    if event == '-MATERIAL_NAME-':
        res_combo = window['-RESISTOR_NAME-']
        resistor_names = [mat.resistor.name for mat in materials if mat.name == window['-MATERIAL_NAME-'].get()]
        res_combo.update(value=res_combo.get() if res_combo.get() in resistor_names else resistor_names[0],
                         values=resistor_names)

        match = get_material_match(mat_name=window['-MATERIAL_NAME-'].get(),
                                   resistor_name=window['-RESISTOR_NAME-'].get())
        window['-E_R-'].update(value=str(match.er))
        window['-TANL-'].update(value=str(match.tanl))

    if event == '-RESISTOR_NAME-':
        match = get_material_match(mat_name=window['-MATERIAL_NAME-'].get(),
                                   resistor_name=window['-RESISTOR_NAME-'].get())
        window['-E_R-'].update(value=str(match.er))
        window['-TANL-'].update(value=str(match.tanl))

    if event == 'Ok' and not ryn_script_thread.is_alive():
        selected_mat = get_material_match(mat_name=window['-MATERIAL_NAME-'].get(),
                                          resistor_name=window['-RESISTOR_NAME-'].get())
        print(
            f"chose frequency : {window['-FREQUENCY-'].get()},e_r:{window['-E_R-'].get()} ,tanl:{window['-TANL-'].get()} , material id : {selected_mat.id} , destination folder :{window['-DST_FOLDER-'].get()}")
        try:
            ryn_script_thread = Thread(target=run_script, args=(
                selected_mat.id, float(window['-FREQUENCY-'].get()), float(window['-E_R-'].get()),
                float(window['-TANL-'].get())))
            window['-STATUS_BAR-'].update(value="running", background_color="yellow")
            ryn_script_thread.start()
            dst_folder = window["-DST_FOLDER-"].get()
            copy_files(pad_name=selected_mat.resistor.pad_name, dst_path=dst_folder)
            # window.refresh()
        except Exception as e:
            print(f"error in symbol creator : {e}")
    if not ryn_script_thread.is_alive():
        window['-STATUS_BAR-'].update(value="done", background_color="green", text_color="black")
    window.refresh()

# Finish up by removing from the screen
window.close()