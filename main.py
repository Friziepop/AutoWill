# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import win32com.client as win32
from awr_optimizer import AwrOptimizer


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    awr = win32.DispatchEx("MWOApp.MWOffice")
    path = f"{os.getcwd()}\\WilkingsonPowerDivider.emp"
    print (f"opening path :{path}")
    awr.Open(path)
    # optimizer = AwrOptimizer()
    # optimizer.connect()
    # optimizer.run_optimizer()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
