import jsonpython
from typing import TypeVar

T = TypeVar("T")

def config_class(filename: str):
    def wrapper(cls: T) -> T:
        def new_constructor(self: T) -> None:
            obj = jsonpython.from_file(cls, filename) # type: ignore
            self.__dict__.update(obj.__dict__)
        cls.__init__ = new_constructor # type: ignore
        return cls
    return wrapper

"""
Example config class.

# config.json
# {
#   "lol": 1,
#   "name": "sss"
# }


@config_class("config.json")
class Config:
    lol: int
    name: str

config = Config()
print(config.name) # sss

"""
        