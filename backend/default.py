from backend.api import Backend, Type, CodeLocation, DataLocation

class DefaultCodeLocation(CodeLocation):
  def __init__(self, desc: str, line: int):
    self._desc = desc
    self._line = line

class DefaultDataLocation(DataLocation):
  pass

class DefaultBackend(Backend):
  pass
