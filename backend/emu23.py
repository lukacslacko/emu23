from backend.api2 import *

class Emu23CodeLoc(CodeLoc):
  def __init__(self, name: str):
    self.name=name
    self.ll=[]
    self.lh=[]
    self.lb=[]
    self.addr=None

class Emu23DataLoc(DataLoc):
  def size(self):
    return 4

class Emu23Backend(Backend):
  def name() -> str:
    return 'Emu23'

  def __init__(self) -> None:
    self.code=[]
    self.labels=[]
    self.labelnames=[]
    self.addr=0
    self.isinfunc=False
    self.blocks=[]
    self.lefttvar=None
    self.righttvar=None
    self.stack_ptr=0

  def set_entry(self, entry: Emu23CodeLoc) -> None:
    self.entry = entry

  def link(self) -> None:
    pass

  def write_to_file(self, filename: str) -> None:
    pass

  def comment(self, comment: str) -> None:
    self.code.append(([],';'+comment))

  def get_label(self, name: str) -> Emu23CodeLoc:
    i=0
    while name+str(i) in self.labelnames:
      i+=1
    self.labelnames.append(name+str(i))
    l=Emu23CodeLoc(name+str(i))
    self.labels.append(l)
    return l

  def link_label_to_here(self, label: Emu23CodeLoc) -> None:
    self.comment(label.name+':')
    label.addr=self.addr

  #begin_func

  def begin_block(self) -> None:
    self.blocks.append([])

  def copy(self, source: DataLoc, target: DataLoc) -> None:
    pass

  def set(self, target: DataLoc, value: Any) -> None:
    pass

  def create_temp_ver(self, t: Type) -> DataLoc:
    pass

  def release_temp_var(self, tvar: DataLoc) -> None:
    pass

  def jump(self, target: CodeLoc) -> None:
    pass
    # tbc targetB
    # tcpcb
    # tbc targetH
    # tcpch
    # tbc targetL
    # jmpl

  def jump_if_zero(self, cond: DataLoc, target: CodeLoc) -> None:
    pass

  def jump_if_not_zero(self, cond: DataLoc, target: CodeLoc) -> None:
    pass

  # call

  # call_ptr

  def break_(self, level: int) -> None:
    pass

  def end_block(self) -> None:
    self.break_(1)

  def return_(self) -> None:
    pass

  def end_function(self) -> None:
    self.isinfunc = False
    self.return_()

  # binary_operate

  # unary_operate
