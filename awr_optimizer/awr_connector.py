from abc import ABC

from pyawr_utils import awrde_utils
import pyawr.mwoffice as mwoffice

class AwrConnector (ABC):
    def __init__(self):
        super(AwrConnector, self).__init__()
        self._awrde = None
        self._proj = None

    def connect(self):
        self._awrde = awrde_utils.establish_link()
        self._proj = awrde_utils.Project(self._awrde)