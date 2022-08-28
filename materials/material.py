from dataclasses import dataclass


@dataclass
class Material:
    id:int
    name: str
    er: float
    tanl: float
    rho: float
    height: float
    thickness: float
    start_freq: float
    end_freq: float
    description: str

    def __init__(self,
                 id : int,
                 name: str,
                 er: float,
                 tanl: float,
                 rho: float,
                 height: float,
                 thickness: float,
                 start_freq: float,
                 end_freq: float,
                 description: str = "",
                 ):
        self.id = id
        self.height = height
        self.thickness = thickness
        self.start_freq = start_freq
        self.end_freq = end_freq
        self.description = description
        self.rho = rho
        self.tanl = tanl
        self.er = er
        self.name = name
