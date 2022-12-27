import shutil
import time
from typing import List

import PySimpleGUI as sg

from materials.material import Material
from materials.materials_db import MaterialDB
from symbol_creator import MATERIALS_DB, SymbolCreator


def copy_files(pad_name: str, dst_path: str):
    shutil.copy2(src="../orcad/io/ioport.pad", dst=dst_path)
    shutil.copy2(src=f"../orcad/resistor/{pad_name}.pad", dst=dst_path)
    shutil.copy2(src=f"../orcad/package/wil_sym.dra", dst=dst_path)
    shutil.copy2(src=f"../orcad/package/wil_sym.psm", dst=dst_path)


material_db = MaterialDB(MATERIALS_DB)
materials: List[Material] = material_db.get_all()

all_resistors_names = list(set([mat.resistor.name for mat in materials]))
materials_names = list(set([mat.name for mat in materials]))

resistor_names = all_resistors_names

# Define the window's contents
layout = [[sg.Text("output")],
          [sg.Text("Enter frequency [GHZ]"), sg.Input(key='-FREQUENCY-')],
          [sg.Text("Enter material"),
           sg.Combo(materials_names, key='-MATERIAL_NAME-', readonly=True, change_submits=True)],
          [sg.Text("Enter resistor"), sg.Combo(resistor_names, key='-RESISTOR_NAME-', readonly=True)],
          [sg.Text("Enter e_r"), [sg.Input(key='-E_R-')]],
          [sg.Text("Enter tanl"), sg.Input(key='-TANL-')],
          [sg.Text('Select a folder:'), sg.FolderBrowse(key='-DST_FOLDER-')],
          [sg.Output(size=(50, 10), key='-OUTPUT-')],
          [sg.Button('Ok')]]

# Create the window
window = sg.Window('Symbol creator', layout)

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
    if event == 'Ok':
        possible_matches = [mat for mat in materials if
                            mat.name == window['-MATERIAL_NAME-'].get() and mat.resistor.name == window[
                                '-RESISTOR_NAME-'].get()]
        if len(possible_matches) != 1:
            print("Error matching material")
            continue
        selected_mat = possible_matches[0]
        print(
            f"chose frequency : {window['-FREQUENCY-'].get()},e_r:{window['-E_R-'].get()} ,tanl:{window['-TANL-'].get()} , material id : {selected_mat.id} , destination folder :{window['-DST_FOLDER-'].get()}")
        try:
            SymbolCreator().create(material_id=selected_mat.id, frequency=float(window['-FREQUENCY-'].get()),
                                   er=float(window['-E_R-'].get()), tanl=float(window['-TANL-'].get()))
            dst_folder = window["-DST_FOLDER-"].get()
            copy_files(pad_name=selected_mat.resistor.pad_name, dst_path=dst_folder)
            window.refresh()
            break
        except Exception as e:
            print(f"error in symbol creator : {e}")

# Finish up by removing from the screen
window.close()
