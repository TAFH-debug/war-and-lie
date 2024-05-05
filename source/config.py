import jsonpython

"""
Global configs, everything related to game that should not be hardcoded.
"""
class GlobalConfig:
    sprite_path: str
    
    def __init__(self) -> "GlobalConfig":
        obj = jsonpython.from_file(GlobalConfig, "config.json")
        self.__dict__.update(obj.__dict__)
        
class UnitsConfig:
    units: list
    
    def __init__(self) -> "UnitsConfig":
        obj = jsonpython.from_file(UnitsConfig, "units_config.json")
        self.__dict__.update(obj.__dict__)
            
