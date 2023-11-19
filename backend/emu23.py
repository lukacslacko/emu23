from backend.api2 import *

class Emu23CodeLoc(CodeLoc):
  def __init__(self, name: str):
    self.name=name
    self.ll=[]
    self.lh=[]
    self.lb=[]
    self.addr=None

class Emu23DataLoc(DataLoc):
  pass

class Emu23Backend(Backend):
  def name() -> str:
    return 'Emu23'

  def __init__(self) -> None:
    self.code=[]
    self.labels=[]
    self.labelnames=[]
    self.addr=0

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
