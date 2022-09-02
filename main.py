# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np

from awr_optimizer.awr_equation_manager import AwrEquationManager
from awr_optimizer.awr_optimizer import AwrOptimizer
from awr_optimizer.extractor import Extractor
from awr_optimizer.optimization_constraint import OptimizationConstraint

from materials.materials_db import MaterialDB
from copy import deepcopy

x = 5

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
