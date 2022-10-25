import time
from typing import List

import PySimpleGUI as sg

from materials.material import Material
from materials.materials_db import MaterialDB

material_db = MaterialDB(csv_path="../materials/materials_db.csv")
materials: List[Material] = material_db.get_all()

resistors = {mat.resistor.id: mat.resistor.name for mat in materials}

materials_names = list(set([mat.name for mat in materials]))

# Define the window's contents
layout = [[sg.Text("Enter frequency [GHZ]?")],
          [sg.Input(key='-FREQUENCY-')],
          [sg.Text("Enter material?")],
          [sg.Combo(materials_names, key='-MATERIAL_NAME-', readonly=True)],
          [sg.Text("Enter resistor?")],
          [sg.Combo(materials_names, key='RESISTOR_NAME-', readonly=True)],
          [sg.Text("Enter e_r?")],
          [sg.Input(key='-E_R-')],
          [sg.Text("Enter tanl?")],
          [sg.Input(key='-TANL-')],
          [sg.Text(size=(40, 1), key='-OUTPUT-')],
          [sg.Button('Ok')]]

# Create the window
window = sg.Window('SYmbol creator', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == 'Ok':
        print("start to generate")
        possible_matches = [mat for mat in materials if mat.name == window['-MATERIAL_NAME-'] and mat.resistor.name == window['-RESISTOR_NAME-']]
        if len(possible_matches) != 1:
            print("Error matching material")
            break
        selected_mat = possible_matches[0]
        window['-OUTPUT-'].update(
            f"chose frequency : {window['-FREQUENCY-']},e_r:{window['-E_R-']} ,tanl:{window['-TANL-']} , material id : {selected_mat.id}")
        break
    # Output a message to the window

# Finish up by removing from the screen
window.close()
