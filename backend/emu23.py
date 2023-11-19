from backend.api2 import *

class Emu23CodeLoc(CodeLoc):
  def __init__(self, name: str):
    self.name=name
    self.ll=[]
    self.lh=[]
    self.lb=[]
    self.addr=None

class Emu23DataLoc(DataLoc):
  def type(self) -> Type:
    return self.typ

  def __init__(self, typ: Type, stack: int=None, absolute: int=None, r: bool=False) -> None:
    self.typ = typ
    self.stack = stack
    self.absolute = absolute
    self.r = r

class Emu23Backend(Backend):
  def name() -> str:
    return 'Emu23'

  def __init__(self) -> None:
    self.code=[]
    self.labels=[]
    self.labelnames=[]
    self.addr=0
    self.isinfunc=False
    self.staticsize=0
    self.ntvar=False

  def create_static_var(self, t: Type) -> DataLoc:
    if isinstance(t, PrimitiveType):
      t=self.to_complex_type(t)
    if t.align==1:
      pass
    elif t.align==2:
      self.staticsize+=self.staticsize%2
    elif t.align==4:
      self.staticsize+=3
      self.staticsize&=-4
    else:
      raise ValueError('weird alignment')
    self.staticsize+=t.size
    return Emu23DataLoc(t,None,self.staticsize-t.size)

  def set_entry(self, entry: CodeLoc) -> None:
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

  def link_label_to_here(self, label: CodeLoc) -> None:
    self.comment(label.name+':')
    label.addr=self.addr

  def __so(self, t: Type) -> int:
    if isinstance(t, PrimitiveType):
      t=self.to_complex_type(t)
    return t.size

  def create_local_var(self, t: Type) -> DataLoc:
    self.blocks[-1].append(t)
    self.stack_ptr+=self.__so(t)
    for _ in range(self.__so(t)):
      self.code.append(([0x2d],'phb'))
    return Emu23DataLoc(t,self.stack_ptr)

  def begin_func(self, return_type: Type, args: list[Type]) -> typle[DataLoc, list[DataLoc]]:
    if self.isinfunc:
      raise
    self.blocks=[[]]
    self.lefttvar=None
    self.righttvar=None
    self.stack_ptr=-1
    r=self.create_local_var(return_type)
    a=[]
    for arg in args:
      a.append(self.create_local_var(arg)
    self.stack_ptr+=5
    self.code.append([0x1e],'phf')
    return r,a

  def begin_block(self) -> None:
    self.blocks.append([])

  def copy(self, source: DataLoc, target: DataLoc) -> None:
    pass

  def set(self, target: DataLoc, value: Any) -> None:
    pass

  def create_temp_ver(self, t: PrimitiveType) -> DataLoc:
    if self.lefttvar is None:
      l=Emu23DataLoc(t)
      self.lefttvar = l
      return l
    elif self.righttvar is None:
      l=Emu23DataLoc(t,None,None,True)
      self.righttvar=l
      return l
    else:
      s=self.__so(t)
      if self.ntvar:
        #
	self.righttvar.stack=self.stack_ptr
	self.righttvar.r=False
	self.righttvar=Emu23DataLoc(t,None,None,True)
	#TODO

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
    self.code+=[([0x1f],'plf'),([0x43],'retl')]

  def end_function(self) -> None:
    self.isinfunc = False
    self.return_()

  # binary_operate

  # unary_operate

  def to_complex_type(primitive: PrimitiveType) -> ComplexType:
    if primitive == PrimitiveType.BOOL or primitive == PrimitiveType.I8:
      return ComplexType(1,1)
    elif primitive = PrimitiveType.I16:
      return ComplexType(2,2)
    elif primitive = PrimitiveType.PTR:
      return ComplexType(3,4)
    else:
      raise

  def offset(base: DataLoc, offset: int, primitive: PrimitiveType) -> DataLoc:
    if base.stack is not None:
      return Emu23DataLoc(primitive, base.stack-offset)
    elif base.absolute is not None:
      return Emu23DataLoc(primitive, None, base.absolute+offset)
    else:
      raise
