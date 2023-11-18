from backend.api import Backend, Type, CodeLocation, DataLocation

_SIZE = {
  Type.BOOL: 1,
  Type.INT8: 1,
  Type.INT16: 2,
  Type.PTR: 4,
}

class DefaultCodeLocation(CodeLocation):
  def __init__(self, line: int):
    self._line = line
    
  def __str__(self):
    return f"code@{self._line}"

class DefaultDataLocation(DataLocation):
  def __init__(self, loc: str, typ: Type):
    self._loc = loc
    self._type = Type
    
  def __str__(self):
    return f"@{self._loc}({self._type.value})"
  
  def __repr__(self):
    return str(self)
  
  def size(self) -> int:
    return _SIZE[self._typ]

class DefaultBackend(Backend):
  def __init__(self):
    self._code = []
    self._stack_ptr = 0
    
  def name() -> str:
    return "Default"
  
  def link(self):
    pass
  
  def _dispose_local_var(self, v: DefaultDataLocation):
    self._code.append("dispose of {v}")
    self._stack_ptr -= v.size()
    
  def create_local_var(self, t: Type) -> DefaultDataLocation:
    v = DefaultDataLocation(f"stack@{self._stack_ptr}", t)
    self._stack_ptr += v.size()
    return v
  
  def write_to_file(self, filename: str):
    with open(filename, "w") as f:
      f.write("\n".join(self._code))
  
  def REG(self, num: int, type: Type) -> DefaultDataLocation:
    return DefaultDataLocation(f"REG{num}({type.value})")
  
  def BREAK_COUNTER(self) -> DataLocation:
    return DefaultDataLocation("break_counter")
  
  def begin_block(self) -> CodeLocation:
    self._begin_block = len(self._code)
    self._code.append("begin block")
    return DefaultCodeLocation(self._begin_block)

  def begin_function(self, return_type: Type, args: list[Type]) -> tuple[DataLocation, list[DataLocation]]:
    self._ret_val = self.create_local_var(return_type)
    self._arg_vals = [self.create_local_var(t) for t in args]
    return (self._ret_val, self._arg_vals)
  
  def end_function(self) -> None:
    for v in reversed(self._arg_vals):
      self._dispose_local_var(v)
    
  def end_block(self):
    _end_block = len(self._code)
    for i in range(self._begin_block, self._end_block):
      if "{block_end}" in self._code[i]:
        self._code[i] = self._code[i].format(block_end=_end_block)
    for v in reversed(self._local_vars):
      self._dispose_local_var(v)
    self._code.append("end block")  