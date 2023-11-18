from typ import Type

class Label:
  name: str
  addr: int
  def __init__(self,name):
    self.name=name
    self.addr=None
  def __str__(self):
    return f"(Label){self.addr} {self.name}"
  def __repr__(self):
    return str(self)

class RodataHandle:
  name: str
  data: bytes
  def __init__(self,name,data):
    self.name=name
    self.data=data

  def __str__(self):
    return f"(RodataHandle){self.name} {self.bytes}"

  def __repr__(self):
    return str(self)

class Location:
  absolute: int
  stack: int
  label: Label = None
  rodata: RodataHandle = None

  def __init__(self, absolute: int, stack: int, label: Label=None, rodata: RodataHandle=None):
    self.absolute = absolute
    self.stack = stack
    self.label = label
    self.rodata = rodata

  @staticmethod
  def absolute(a: int) -> "Location":
    return Location(a, None)

  @staticmethod
  def stack(s: int) -> "Location":
    return Location(None, s)

  @staticmethod
  def code(label: Label) -> "Location":
    return Location(None, None, label)

  @staticmethod
  def rodata(rodata: RodataHandle) -> "Location":
    return Location(None, None, None, rodata)

  def __str__(self):
    if self.absolute is not None:
      return f"(Loc)asbolute({self.absolute})"
    if self.stack is not None:
      return f"(Loc)stack({self.stack})"
    if self.label is not None:
      return f"(Loc)label({self.label})"
    return "(Loc)None"

class Symbol:
  name: str
  loc: Location
  type: Type

  def __init__(self, name: str, loc: Location, type: Type):
    self.name = name
    self.loc = loc
    self.type = type

  def __str__(self):
    return f"(Symbol)name={self.name} {self.loc} {self.type}"
  def __repr__(self):
    return str(self)

SYMBOLS = [{}]

def add(name: str, loc: Location, type: Type) -> None:
  if name in SYMBOLS[-1]:
    raise ValueError(f"Symbol already defined {name}")
  SYMBOLS[-1][name] = Symbol(name, loc, type)

def get(name: str) -> Symbol:
  for SYM in reversed(SYMBOLS):
    if name in SYM:
      return SYM[name]
  return None

def total_local_stack_space() -> int:
  print(SYMBOLS, SYMBOLS[-1])
  return sum(sym.type.size for sym in SYMBOLS[-1].values() if sym.loc.stack is not None)

def push() -> None:
  SYMBOLS.append({})

def pop() -> None:
  SYMBOLS.pop()
