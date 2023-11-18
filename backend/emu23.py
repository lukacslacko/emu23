from backend.api import *
from enum import Enum

_SIZE = {
  Type.BOOL: 1,
  Type.INT8: 1,
  Type.INT16: 2,
  Type.PTR: 3,
}

class Emu23CodeLocation(CodeLocation):
  def __init__(self, addr: int):
    self._addr = addr

  def __str__(self):
    return f"code@{self._addr:06x}"

class Emu23DataLocationTypes(Enum):
  STACK = "stack"
  MEM = "mem"
  BREAK_COUNTER = "brkc"

class Emu23DataLocation(DataLocation):
  def __init__(self, typ: Type, loctyp: Emu23DataLocationTypes, loc: int):
    self._loc = loc
    self._type = typ
    self._loctyp = loctyp

  def __str__(self):
    return f"@{self._loctyp.value}{self._loc}({self._type.value})"

  def __repr__(self):
    return str(self)

  def size(self) -> int:
    return _SIZE[self._typ]

class Emu23Backend(Backend):
  pass
