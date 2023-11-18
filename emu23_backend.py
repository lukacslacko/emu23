from backend import Backend, Register, Asm, i8REGS, ptrREGS, boolREGS, u8REGS, i16REGS, u16REGS, i24REGS, u24REGS
from sym import Location, Label, RodataHandle
import typ

def check_i8reg(r: Register):
  if not r in i8REGS:
    raise ValueError(f"Not i8 register {r}")

def check_ptrreg(r: Register):
  if not r in ptrREGS:
    raise ValueError(f"Not ptr register {r}")

def check_boolreg(r: Register):
  if not r in boolREGS:
    pass#raise ValueError(f"Not bool register {r}")

def check_u8reg(r: Register):
  if not r in u8REGS:
    raise ValueError(f"Not u8 register {r}")

def check_i16reg(r: Register):
  if not r in i16REGS:
    raise ValueError(f"Not i16 register {r}")

def check_u16reg(r: Register):
  if not r in u16REGS:
    raise ValueError(f"Not u16 register {r}")

def check_i24reg(r: Register):
  if not r in i24REGS:
    raise ValueError(f"Not i24 register {r}")

def check_u24reg(r: Register):
  if not r in u24REGS:
    raise ValueError(f"Not u24 register {r}")

class LabelEmu23(Label):
  addr: int
  ll: list[int] = []
  lh: list[int] = []
  lb: list[int] = []
  name: str
  def __init__(self, name):
    self.name=name
    self.addr=None
  def __str__(self):
    if self.addr is None:
      return f"UNLINKED LABEL `{self.name}`"
    return f"{self.addr:06x}`{self.name}`"
  def __repr__(self):
    return str(self)

class RodataHandleEmu23(RodataHandle):
  label: LabelEmu23
  def __init__(self,label):
    self.label=label
  def __str__(self):
    return str(self.label)
  def __repr__(self):
    return str(self)

class AsmEmu23(Asm):
  hasimm: bool
  op: int
  imm: int
  s: str
  addr: int
  label: LabelEmu23
  def bytes(self) -> int:
    return self.hasimm+1
  def __str__(self):
    return f"{self.addr:06x} {self.op:02x} {hex(self.imm)[2:].zfill(2) if self.hasimm else '  '} {self.s.replace('|',str(self.label))}" 
  def __repr__(self):
    return str(self)
  def __init__(self,s,op,imm=None,label=None):
    self.s=s
    self.label=label
    self.addr=0xdeadbeef
    self.op=op
    self.hasimm=False
    if imm is not None:
      self.imm=imm&0xff
      self.hasimm=True

def setra8(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I8,Register.REG0_U8,Register.REG0_BOOL]:
    return AsmEmu23("ra1",0x01)
  if r in [Register.REG1_I8,Register.REG1_U8,Register.REG1_BOOL]:
    return AsmEmu23("ra4",0x04)
  raise ValueError(f"{r}")
def setrb8(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I8,Register.REG0_U8,Register.REG0_BOOL]:
    return AsmEmu23("rb1",0x09)
  if r in [Register.REG1_I8,Register.REG1_U8,Register.REG1_BOOL]:
    return AsmEmu23("rb4",0x0c)
  raise ValueError(f"{r}")
def setra16h(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I16,Register.REG0_U16]:
    return AsmEmu23("ra2",0x02)
  if r in [Register.REG1_I16,Register.REG1_U16]:
    return AsmEmu23("ra5",0x05)
  raise ValueError(f"{r}")
def setrb16h(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I16,Register.REG0_U16]:
    return AsmEmu23("rb2",0x0a)
  if r in [Register.REG1_I16,Register.REG1_U16]:
    return AsmEmu23("rb5",0x0d)
  raise ValueError(f"{r}")
def setra16l(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I16,Register.REG0_U16]:
    return AsmEmu23("ra1",0x01)
  if r in [Register.REG1_I16,Register.REG1_U16]:
    return AsmEmu23("ra4",0x04)
  raise ValueError(f"{r}")
def setrb16l(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I16,Register.REG0_U16]:
    return AsmEmu23("rb1",0x09)
  if r in [Register.REG1_I16,Register.REG1_U16]:
    return AsmEmu23("rb4",0x0c)
  raise ValueError(f"{r}")
def setra24b(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I24,Register.REG0_U24,Register.REG0_PTR]:
    return AsmEmu23("ra3",0x03)
  if r in [Register.REG1_I24,Register.REG1_U24,Regsiter.REG1_PTR]:
    return AsmEmu23("ra6",0x06)
  raise ValueError(f"{r}")
def setrb24b(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I24,Register.REG0_U24,Register.REG0_PTR]:
    return AsmEmu23("rb3",0x0b)
  if r in [Register.REG1_I24,Register.REG1_U24,Register.REG1_PTR]:
    return AsmEmu23("rb6",0x0e)
  raise ValueError(f"{r}")
def setra24h(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I24,Register.REG0_U24,Register.REG0_PTR]:
    return AsmEmu23("ra2",0x02)
  if r in [Register.REG1_I24,Register.REG1_U24,Register.REG1_PTR]:
    return AsmEmu23("ra5",0x05)
  raise ValueError(f"{r}")
def setrb24h(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I24,Register.REG0_U24,Register.REG0_PTR]:
    return AsmEmu23("rb2",0x0a)
  if r in [Register.REG1_I24,Register.REG1_U24,Register.REG1_PTR]:
    return AsmEmu23("rb5",0x0d)
  raise ValueError(f"{r}")
def setra24l(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I24,Register.REG0_U24,Register.REG0_PTR]:
    return AsmEmu23("ra1",0x01)
  if r in [Register.REG1_I24,Register.REG1_U24,Register.REG1_PTR]:
    return AsmEmu23("ra4",0x04)
  raise ValueError(f"{r}")
def setrb24l(r: Register) -> AsmEmu23:
  if r in [Register.REG0_I24,Register.REG0_U24,Register.REG0_PTR]:
    return AsmEmu23("rb1",0x09)
  if r in [Register.REG1_I24,Register.REG1_U24,Regsiter.REG1_PTR]:
    return AsmEmu23("rb4",0x0c)
  raise ValueError(f"{r}")

class BackendEmu23(Backend):
  TYPES = [
    typ.Type("bool",1),
    typ.Type("i8",1),
    typ.Type("u8",1),
    typ.Type("i16",2),
    typ.Type("u16",2),
    typ.Type("i24",3),
    typ.Type("u24",3),
    typ.Type("ptr",3),
    typ.Type("call",5),
  ]
  entry: LabelEmu23=None
  rodata: bytearray = bytearray()
  handles: list[tuple[int,int]] = []
  data_segment_size: int=0
  did_link=False
  absolutes: dict[int,int] = {}
  rodata_base: int
  absolutes_base: int
  int_funcs: dict[str, LabelEmu23]={}
  saddr: int=0x810400
  def __repr__(self):
    return str(self)
  def __str__(self):
    string = f'entry: {self.entry}\ncode:\n'
    string += '\n'.join(map(str, self.code))
    string += '\n\nrodata:\n'
    for i in range(len(self.rodata)):
      string += f'{self.rodata[i]:02X}'
      if (i%16)==0:
        string += '\n'
      elif i==len(self.rodata)-1:
        string += '\n'
      else:
        string += ' '
    string += f'\ndata length: {self.data_segment_size}'
    return string
  def add_rodata(self, name: str, data: bytes) -> RodataHandle:
    self.handles.append((len(self.labels),len(self.rodata)))
    self.rodata+=data
    return RodataHandleEmu23(self.label(name))
  @staticmethod
  def name() -> str:
    return "Emu23"
  def __init__(self):
    self.addr=self.saddr
    self.entry=self.label("entry")
    self.link_label_to_addr(self.entry,self.addr)
    self.__add_insts([AsmEmu23("rb0",0x08)])
  def set_entry(self, entry: Label):
    if not isinstance(entry, LabelEmu23):
      raise TypeError()
    self.entry=entry
  def __add_insts(self,insts: list[AsmEmu23]):
    for inst in insts:
      inst.addr=self.addr
      self.code.append(inst)
      self.addr+=1
  def label(self,name: str) -> Label:
    label = LabelEmu23(name)
    self.labels.append(label)
    return label
  def __call(self, func: str):
    if not func in self.int_funcs:
      raise ValueError()
    label = self.int_funcs[func]
    label.lb.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |B",0x28,0xdeadbeef,label),AsmEmu23("tcpcb",0x6c)])
    label.lh.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |H",0x28,0xdeadbeef,label),AsmEmu23("tcpch",0x6b)])
    label.ll.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |L",0x28,0xdeadbeef,label),AsmEmu23("calll",0x3f)])
  def link_label_to_addr(self,label,addr):
    label.addr=addr
  def link_label_to_here(self,label: Label):
    if not isinstance(label,LabelEmu23):
      raise TypeError()
    self.link_label_to_addr(label,self.addr)
    super().comment(f"LABEL `{label.name}`")
  def write_to_file(self, file_name: str):
    if not self.did_link:
      raise ValueError("has to link before writing to file")
    with open(file_name+'.emu23', "wb") as f:
      f.write(b'\xfe\xed')
      d=self.addr-self.saddr
      f.write(d.to_bytes(3,'big'))
      d=len(self.rodata)
      f.write(d.to_bytes(3,'big'))
      d=self.data_segment_size
      f.write(d.to_bytes(3,'big'))
      d=self.entry.addr
      f.write(d.to_bytes(3,'big'))
      for asm in self.code:
        if isinstance(asm, AsmEmu23):
          f.write(asm.op.to_bytes(1,'big'))
          if asm.hasimm:
            f.write(asm.imm.to_bytes(1,'big'))
      f.write(self.rodata)
      f.write(bytes(f'\n\n\n{self}','ascii'))

  def leave(self):
    self.__add_insts([AsmEmu23("plf",0x1f),AsmEmu23("retl",0x41)])
  def enter(self):
    self.__add_insts([AsmEmu23("phf"),0x1e])

  #bool

  #i8
  def set_i8(self, value: int, target: Register):
    check_i8reg(target)
    if value==0:
      self.__add_insts([setra8(target),AsmEmu23("tba",0x23)])
      return
    self.__add_insts([setra8(target),AsmEmu23(f"tba {value}",0x22,value)])
  def copy_i8(self, source: Register, target: Register):
    check_i8reg(source)
    check_i8reg(target)
    if source==target:
      return
    self.__add_insts([setra8(source),setrb8(target),AsmEmu23("tab",0x21),AsmEmu23("rb0",0x08)])
  def add_i8(self, left: Register, right: Register, result: Register):
    check_i8reg(left)
    check_i8reg(right)
    check_i8reg(result)
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("add",0x11)])
    if result==right:
      self.__add_insts([AsmEmu23("tcb",0x25),AsmEmu23("rb0",0x08)])
      return
    if result!=left:
      self.__add_insts([setra8(result)])
    self.__add_insts([AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08)])
  def sub_i8(self, left: Register, right: Register, result: Register):
    check_i8reg(left)
    check_i8reg(right)
    check_i8reg(result)
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("sub",0x15)])
    if result==right:
      self.__add_insts([AsmEmu23("tcb",0x25),AsmEmu23("rb0",0x08)])
      return
    if result!=left:
      self.__add_insts([setra8(result)])
    self.__add_insts([AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08)])
  def mul_i8(self, left: Register, right: Register, result: Register):
    check_i8reg(left)
    check_i8reg(right)
    check_i8reg(result)
    super().mul_i8(left,right,result)
    # TODO
  def div_i8(self, left: Register, right: Register, result: Register):
    check_i8reg(left)
    check_i8reg(right)
    check_i8reg(result)
    raise
    # TODO
  def store_i8(self, loc: Location, source: Register):
    check_i8reg(source)
    if loc.stack is not None:
      offset = self.stack_ptr-loc.stack-1
      if offset==0:
        self.__add_insts([setra8(source),AsmEmu23("tasb",0x5f)])
        return
      if offset>255:
        raise ValueError("stack too deep")
      self.__add_insts([setra8(source),AsmEmu23(f"tasb {offset}",0x5e,offset)])
      return
    if loc.absolute is not None:
      if not loc.absolute in self.absolutes:
        self.absolutes[loc.absolute]=len(self.labels)
        self.label(f"absolute({loc.absolute})")
      label=self.labels[self.absolutes[loc.absolute]]
      label.lb.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |B",0x28,0xdeadbeef,label),AsmEmu23("tcrab",0x36)])
      label.lh.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |H",0x28,0xdeadbeef,label),AsmEmu23("tcrah",0x38)])
      label.ll.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |L",0x28,0xdeadbeef,label),AsmEmu23("tcral",0x3a),
                        setra8(source),AsmEmu23("tam",0x4f)])
      return
    raise ValueError()
  def load_i8(self, loc: Location, target: Register):
    check_i8reg(target)
    if loc.stack is not None:
      offset = self.stack_ptr-loc.stack-1
      if offset==0:
        self.__add_insts([setra8(target),AsmEmu23("tsba",0x5b)])
        return
      if offset>255:
        raise ValueError("stack too deep")
      self.__add_insts([setra8(target),AsmEmu23(f"tsba {offset}",0x5a,offset)])
      return
    if loc.absolute is not None:
      if not loc.absolute in self.absolutes:
        self.absolutes[loc.absolute]=len(self.labels)
        self.label(f"absolute({loc.absolute})")
      label=self.labels[self.absolutes[loc.absolute]]
      label.lb.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |B",0x28,0xdeadbeef,label),AsmEmu23("tcrab",0x36)])
      label.lh.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |H",0x28,0xdeadbeef,label),AsmEmu23("tcrah",0x38)])
      label.ll.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |L",0x28,0xdeadbeef,label),AsmEmu23("tcral",0x3a),
                        setra8(target),AsmEmu23("tma",0x53)])
      return
    if loc.rodata is not None:
      if not isinstance(loc.rodata, RodataHandleEmu23):
        raise TypeError()
      label=loc.rodata.label
      label=self.labels[self.absolutes[loc.absolute]]
      label.lb.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |B",0x28,0xdeadbeef,label),AsmEmu23("tcrab",0x36)])
      label.lh.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |H",0x28,0xdeadbeef,label),AsmEmu23("tcrah",0x38)])
      label.ll.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |L",0x28,0xdeadbeef,label),AsmEmu23("tcral",0x3a),
                        setra8(target),AsmEmu23("tma",0x53)])
      return
    raise ValueError()
  def push_i8(self, source: Register):
    check_i8reg(source)
    self.stack_ptr+=1
    self.__add_insts([setra8(source),AsmEmu23("pha",0x2b)])
  def pop_i8(self, target: Register):
    check_i8reg(target)
    self.stack_ptr-=1
    self.__add_insts([setra8(target),AsmEmu23("pla",0x2f)])
  def gt_i8(self, left: Register, right: Register, result: Register):
    check_i8reg(left)
    check_i8reg(right)
    check_boolreg(result)
    self.__add_insts([setra8(right),setrb8(left),AsmEmu23("sub",0x15),
                      setra8(result),AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08),
                      AsmEmu23("and 0x80",0x1c,0x80),AsmEmu23("tba",0x23),
                      AsmEmu23("sieq",0x49),AsmEmu23("tba 1",0x22,1)])
  def lt_i8(self, left: Register, right: Register, result: Register):
    self.gt_i8(right, left, result)
  def eq_i8(self, left: Register, right: Register, result: Register):
    check_i8reg(left)
    check_i8reg(right)
    check_boolreg(result)
    if (left==right):
      self.set_bool(True, result)
      return
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("cmp",0x59),
                      setra8(result),AsmEmu23("rb0",0x08),AsmEmu23("tba",0x23),
                      AsmEmu23("sine",0x4b),AsmEmu23("tba 1",0x22,1)])
  def ne_i8(self, left: Register, right: Register, result: Register):
    check_i8reg(left)
    check_i8reg(right)
    check_boolreg(result)
    if (left==right):
      self.set_bool(False, result)
      return
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("cmp",0x59),
                      setra8(result),AsmEmu23("rb0",0x08),AsmEmu23("tba",0x23),
                      AsmEmu23("sieq",0x49),AsmEmu23("tba 1",0x22,1)])
  def and_i8(self, left: Register, right: Register, result: Register):
    check_i8reg(left)
    check_i8reg(right)
    check_i8reg(result)
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("and",0x1d)])
    if result==right:
      self.__add_insts([AsmEmu23("tcb",0x25),AsmEmu23("rb0",0x08)])
      return
    if result!=left:
      self.__add_insts([setra8(result)])
    self.__add_insts([AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08)])
  def or_i8(self, left: Register, right: Register, result: Register):
    check_i8reg(left)
    check_i8reg(right)
    check_i8reg(result)
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("or",0x19)])
    if result==right:
      self.__add_insts([AsmEmu23("tcb",0x25),AsmEmu23("rb0",0x08)])
      return
    if result!=left:
      self.__add_insts([setra8(result)])
    self.__add_insts([AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08)])
  def xor_i8(self, left: Register, right: Register, result: Register):
    check_i8reg(left)
    check_i8reg(right)
    check_i8reg(result)
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("xor",0x1b)])
    if result==right:
      self.__add_insts([AsmEmu23("tcb",0x25),AsmEmu23("rb0",0x08)])
      return
    if result!=left:
      self.__add_insts([setra8(result)])
    self.__add_insts([AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08)])
  def load_i8_from_ptr(self, source: Register, target: Register):
    check_ptrreg(source)
    check_i8reg(target)
    raise
    # TODO
  def store_i8_to_ptr(self, source: Register, target: Register):
    check_i8reg(source)
    check_ptrreg(target)
    raise
    # TODO
  def cast_i8_to_bool(self, source: Register, target: Register):
    raise
  def cast_i8_to_u8(self, source: Register, target: Register):
    raise
  def cast_i8_to_i16(self, source: Register, target: Register):
    raise
  def cast_i8_to_u16(self, source: Register, target: Register):
    raise
  def cast_i8_to_i24(self, source: Register, target: Register):
    raise
  def cast_i8_to_u24(self, source: Register, target: Register):
    raise
  def cast_i8_to_ptr(self, source: Register, target: Register):
    raise

  #u8
  def set_u8(self, value: int, target: Register):
    check_u8reg(target)
    if value==0:
      self.__add_insts([setra8(target),AsmEmu23("tba",0x23)])
      return
    self.__add_insts([setra8(target),AsmEmu23(f"tba {value}",0x22,value)])
  def copy_u8(self, source: Register, target: Register):
    check_u8reg(source)
    check_u8reg(target)
    if source==target:
      return
    self.__add_insts([setra8(source),setrb8(target),AsmEmu23("tab",0x21),AsmEmu23("rb0",0x08)])
  def add_u8(self, left: Register, right: Register, result: Register):
    check_u8reg(left)
    check_u8reg(right)
    check_u8reg(result)
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("add",0x11)])
    if result==right:
      self.__add_insts([AsmEmu23("tcb",0x25),AsmEmu23("rb0",0x08)])
      return
    if result!=left:
      self.__add_insts([setra8(result)])
    self.__add_insts([AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08)])
  def sub_u8(self, left: Register, right: Register, result: Register):
    check_u8reg(left)
    check_u8reg(right)
    check_u8reg(result)
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("sub",0x15)])
    if result==right:
      self.__add_insts([AsmEmu23("tcb",0x25),AsmEmu23("rb0",0x08)])
      return
    if result!=left:
      self.__add_insts([setra8(result)])
    self.__add_insts([AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08)])
  def mul_u8(self, left: Register, right: Register, result: Register):
    check_u8reg(left)
    check_u8reg(right)
    check_u8reg(result)
    raise
    # TODO
  def div_u8(self, left: Register, right: Register, result: Register):
    check_u8reg(left)
    check_u8reg(right)
    check_u8reg(result)
    raise
    # TODO
  def store_u8(self, loc: Location, source: Register):
    check_u8reg(source)
    if loc.stack is not None:
      offset = self.stack_ptr-loc.stack-1
      if offset==0:
        self.__add_insts([setra8(source),AsmEmu23("tasb",0x5f)])
        return
      if offset>255:
        raise ValueError("stack too deep")
      self.__add_insts([setra8(source),AsmEmu23(f"tasb {offset}",0x5e,offset)])
      return
    if loc.absolute is not None:
      if not loc.absolute in self.absolutes:
        self.absolutes[loc.absolute]=len(self.labels)
        self.label(f"absolute({loc.absolute})")
      label=self.labels[self.absolutes[loc.absolute]]
      label.lb.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |B",0x28,0xdeadbeef,label),AsmEmu23("tcrab",0x36)])
      label.lh.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |H",0x28,0xdeadbeef,label),AsmEmu23("tcrah",0x38)])
      label.ll.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |L",0x28,0xdeadbeef,label),AsmEmu23("tcral",0x3a),
                        setra8(source),AsmEmu23("tam",0x4f)])
      return
    raise ValueError()
  def load_u8(self, loc: Location, target: Register):
    check_u8reg(target)
    if loc.stack is not None:
      offset = self.stack_ptr-loc.stack-1
      if offset==0:
        self.__add_insts([setra8(target),AsmEmu23("tsba",0x5b)])
        return
      if offset>255:
        raise ValueError("stack too deep")
      self.__add_insts([setra8(target),AsmEmu23(f"tsba {offset}",0x5a,offset)])
      return
    if loc.absolute is not None:
      if not loc.absolute in self.absolutes:
        self.absolutes[loc.absolute]=len(self.labels)
        self.label(f"absolute({loc.absolute})")
      label=self.labels[self.absolutes[loc.absolute]]
      label.lb.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |B",0x28,0xdeadbeef,label),AsmEmu23("tcrab",0x36)])
      label.lh.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |H",0x28,0xdeadbeef,label),AsmEmu23("tcrah",0x38)])
      label.ll.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |L",0x28,0xdeadbeef,label),AsmEmu23("tcral",0x3a),
                        setra8(target),AsmEmu23("tma",0x53)])
      return
    if loc.rodata is not None:
      if not isinstance(loc.rodata, RodataHandleEmu23):
        raise TypeError()
      label=loc.rodata.label
      label=self.labels[self.absolutes[loc.absolute]]
      label.lb.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |B",0x28,0xdeadbeef,label),AsmEmu23("tcrab",0x36)])
      label.lh.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |H",0x28,0xdeadbeef,label),AsmEmu23("tcrah",0x38)])
      label.ll.append(len(self.code))
      self.__add_insts([AsmEmu23("tbc |L",0x28,0xdeadbeef,label),AsmEmu23("tcral",0x3a),
                        setra8(target),AsmEmu23("tma",0x53)])
      return
    raise ValueError()
  def push_u8(self, source: Register):
    check_u8reg(source)
    self.stack_ptr+=1
    self.__add_insts([setra8(source),AsmEmu23("pha",0x2b)])
  def pop_u8(self, target: Register):
    check_u8reg(target)
    self.stack_ptr-=1
    self.__add_insts([setra8(target),AsmEmu23("pla",0x2f)])
  def gt_u8(self, left: Register, right: Register, result: Register):
    check_u8reg(left)
    check_u8reg(right)
    check_boolreg(result)
    raise
    # TODO
  def lt_u8(self, left: Register, right: Register, result: Register):
    self.gt_u8(right, left, result)
  def eq_u8(self, left: Register, right: Register, result: Register):
    check_u8reg(left)
    check_u8reg(right)
    check_boolreg(result)
    if (left==right):
      self.set_bool(True, result)
      return
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("cmp",0x59),
                      setra8(result),AsmEmu23("rb0",0x08),AsmEmu23("tba",0x23),
                      AsmEmu23("sine",0x4b),AsmEmu23("tba 1",0x22,1)])
  def ne_u8(self, left: Register, right: Register, result: Register):
    check_u8reg(left)
    check_u8reg(right)
    check_boolreg(result)
    if (left==right):
      self.set_bool(False, result)
      return
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("cmp",0x59),
                      setra8(result),AsmEmu23("rb0",0x08),AsmEmu23("tba",0x23),
                      AsmEmu23("sieq",0x49),AsmEmu23("tba 1",0x22,1)])
  def and_u8(self, left: Register, right: Register, result: Register):
    check_u8reg(left)
    check_u8reg(right)
    check_i8reg(result)
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("and",0x1d)])
    if result==right:
      self.__add_insts([AsmEmu23("tcb",0x25),AsmEmu23("rb0",0x08)])
      return
    if result!=left:
      self.__add_insts([setra8(result)])
    self.__add_insts([AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08)])
  def or_u8(self, left: Register, right: Register, result: Register):
    check_u8reg(left)
    check_u8reg(right)
    check_i8reg(result)
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("or",0x19)])
    if result==right:
      self.__add_insts([AsmEmu23("tcb",0x25),AsmEmu23("rb0",0x08)])
      return
    if result!=left:
      self.__add_insts([setra8(result)])
    self.__add_insts([AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08)])
  def xor_u8(self, left: Register, right: Register, result: Register):
    check_u8reg(left)
    check_u8reg(right)
    check_i8reg(result)
    self.__add_insts([setra8(left),setrb8(right),AsmEmu23("xor",0x1b)])
    if result==right:
      self.__add_insts([AsmEmu23("tcb",0x25),AsmEmu23("rb0",0x08)])
      return
    if result!=left:
      self.__add_insts([setra8(result)])
    self.__add_insts([AsmEmu23("tca",0x24),AsmEmu23("rb0",0x08)])
  def load_u8_from_ptr(self, source: Register, target: Register):
    raise
    # TODO
  def store_u8_to_ptr(self, source: Register, target: Register):
    raise
    # TODO
  def cast_u8_to_bool(self, source: Register, target: Register):
    raise
  def cast_u8_to_i8(self, source: Register, target: Register):
    raise
  def cast_u8_to_i16(self, source: Register, target: Register):
    raise
  def cast_u8_to_u16(self, source: Register, target: Register):
    raise
  def cast_u8_to_i24(self, source: Register, target: Register):
    raise
  def cast_u8_to_u24(self, source: Register, target: Register):
    raise
  def cast_u8_to_ptr(self, source: Register, target: Register):
    raise

  #i16

  #u16

  #i24

  #u24

  #ptr

  def move_sp(self, diff: int):
    self.stack_ptr += diff
    if diff<0:
      diff*=-1
      if diff<10:
        self.__add_insts([AsmEmu23("plb",0x30)]*diff)
        return
      if diff>255:
        raise ValueError("stack too deep")
      self.__add_insts([AsmEmu23("tsplc",0x66),AsmEmu23("ra7",0x07),
                        AsmEmu23("tca",0x24),AsmEmu23(f"add {diff}",0x10,diff),
                        AsmEmu23("tcspl",0x64),AsmEmu23("tsphc",0x65),
                        AsmEmu23("tca",0x24),AsmEmu23("adc",0x13),
                        AsmEmu23("tcsph",0x63)])
      return
    if diff<10:
      self.__add_insts([AsmEmu23("phb",0x2d)]*diff)
      return
    if diff>255:
      raise ValueError("stack too deep")
    self.__add_insts([AsmEmu23("tsplc",0x66),AsmEmu23("ra7",0x07),
                  AsmEmu23("tca",0x24),AsmEmu23(f"sub {diff}",0x14,diff),
                  AsmEmu23("tcspl",0x64),AsmEmu23("tsphc",0x65),
                  AsmEmu23("tca",0x24),AsmEmu23("sbc",0x17),
                  AsmEmu23("tcsph",0x63)])
  def set_ptr_from_loc(self, loc: Location, target: Register):
    check_ptrreg(target)
    if loc.absolute is not None:
      if not loc.absolute in self.absolutes:
        self.absolutes[loc.absolute]=len(self.labels)
        self.label(f"absolute({loc.absolute})")
      label=self.labels[self.absolutes[loc.absolute]]
      self.__add_insts([setra24b(target)])
      label.lb.append(len(self.code))
      self.__add_insts([AsmEmu23("tba |B",0x23,0xdeadbeef,label),setra24h(target)])
      label.lh.append(len(self.code))
      self.__add_insts([AsmEmu23("tba |H",0x23,0xdeadbeef,label),setra24l(target)])
      label.ll.append(len(self.code))
      self.__add_insts([AsmEmu23("tba |L",0x23,0xdeadbeef,label)])
      return
    if loc.stack is not None:
      offset = self.stack_ptr-loc.stack-1
      if offset>255:
        raise ValueError("stack too deep")
      self.__add_insts([setra24l(target),AsmEmu23("tsplc",0x66),AsmEmu23("tca",0x24)])
      if offset!=0:
        self.__add_insts([AsmEmu23(f"add {offset}",0x10,offset),
                          AsmEmu23("tca",0x24)])
      self.__add_insts([setra24h(target),AsmEmu23("tsphc",0x65),AsmEmu23("tca",0x24)])
      if offset!=0:
        self.__add_insts([AsmEmu23(f"adc",0x13),AsmEmu23("tca",0x24)])
      self.__add_insts([setra24b(target),AsmEmu23("tspbc",0x68),AsmEmu23("tca",0x24)])
      return
    if loc.label is not None:
      self.__add_insts([setra24b(target)])
      loc.label.lb.append(len(self.code))
      self.__add_insts([AsmEmu23("tba |B",0x23,0xdeadbeef,loc.label),setra24h(target)])
      loc.label.lh.append(len(self.code))
      self.__add_insts([AsmEmu23("tba |H",0x23,0xdeadbeef,loc.label),setra24l(target)])
      loc.label.ll.append(len(self.code))
      self.__add_insts([AsmEmu23("tba |L",0x23,0xdeadbeef,loc.label)])
      return
    if loc.rodata is not None:
      if not isinstance(loc.rodata, RodataHandleEmu23):
        raise TypeError()
      self.__add_insts([setra24b(target)])
      loc.rodata.label.lb.append(len(self.code))
      self.__add_insts([AsmEmu23("tba |B",0x23,0xdeadbeef,loc.rodata.label),setra24h(target)])
      loc.rodata.label.lh.append(len(self.code))
      self.__add_insts([AsmEmu23("tba |H",0x23,0xdeadbeef,loc.rodata.label),setra24l(target)])
      loc.rodata.label.ll.append(len(self.code))
      self.__add_insts([AsmEmu23("tba |L",0x23,0xdeadbeef,loc.rodata.label)])
      return
    raise ValueError()
  def offset_ptr(self, source: Register, offset: int, target: Register):
    check_ptrreg(source)
    check_ptrreg(target)
    offset&=0xffffff
    if offset==0:
      self.copy_ptr(source, target)
      return
    self.__add_insts([setra24l(source)])
    if (offset&0xff)==0:
      self.__add_insts([AsmEmu23("add",0x11)])
    else:
      self.__add_insts([AsmEmu23(f"add {offset&0xff}",0x10,offset&0xff)])
    if source!=target:
      self.__add_insts([setra24l(target)])
    self.__add_insts([AsmEmu23("tca",0x24),setra24h(source)])
    if (offset&0xff00)==0:
      self.__add_insts([AsmEmu23("adc",0x13)])
    else:
      self.__add_insts([AsmEmu23(f"adc {(offset&0xff00)>>8}",0x12,(offset&0xff00)>>8)])
    if source!=target:
      self.__add_insts([setra24h(target)])
    self.__add_insts([AsmEmu23("tca",0x24),setra24b(source)])
    if (offset&0xff0000)==0:
      self.__add_insts([AsmEmu23("adc",0x13)])
    else:
      self.__add_insts([AsmEmu23(f"adc {(offset&0xff0000)>>16}",0x12,(offset&0xff0000)>>16)])
    if source!=target:
      self._add_insts(psetra24b(target))
    self.__add_insts([AsmEmu23("tca",0x24)])
    return
  def jump(self, label: Label):
    if not isinstance(label,LabelEmu23):
      raise TypeError()
    label.lb.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |B",0x28,0xdeadbeef,label),AsmEmu23("tcpcb",0x6c)])
    label.lh.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |H",0x28,0xdeadbeef,label),AsmEmu23("tcpch",0x6b)])
    label.ll.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |L",0x28,0xdeadbeef,label),AsmEmu23("jmpl",0x3d)])
  def jump_if_false(self, cond: Register, label: Label):
    if not isinstance(label,LabelEmu23):
      raise TypeError()
    check_boolreg(cond)
    self.__add_insts([setra8(cond),AsmEmu23("cmp",0x59)])
    label.lb.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |B",0x28,0xdeadbeef,label),AsmEmu23("tcpcb",0x6c)])
    label.lh.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |H",0x28,0xdeadbeef,label),AsmEmu23("tcpch",0x6b)])
    label.ll.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |L",0x28,0xdeadbeef,label),AsmEmu23("sne",0x4c),AsmEmu23("jmpl",0x3d)])
  def jump_if_true(self, cond: Register, label: Label):
    if not isinstance(label,LabelEmu23):
      raise TypeError()
    check_boolreg(cond)
    self.__add_insts([setra8(cond),AsmEmu23("cmp",0x59)])
    label.lb.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |B",0x28,0xdeadbeef,label),AsmEmu23("tcpcb",0x6c)])
    label.lh.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |H",0x28,0xdeadbeef,label),AsmEmu23("tcpch",0x6b)])
    label.ll.append(len(self.code))
    self.__add_insts([AsmEmu23("tbc |L",0x28,0xdeadbeef,label),AsmEmu23("seq",0x4a),AsmEmu23("jmpl",0x3d)])
  def link(self, data_segment_size: int=0):
    if self.did_link:
      raise ValueError("")
    self.data_segment_size=data_segment_size
    self.did_link=True
    dptr=(self.addr&0xfffc00)+0x400
    self.rodata_base=dptr
    for handle in self.handles:
      self.link_label_to_addr(self.labels[handle[0]],dptr)
      dptr+=handle[1]
    self.absolutes_base=(dptr&0xfffc00)+0x400
    for absolute in self.absolutes:
      self.link_label_to_addr(self.labels[self.absolutes[absolute]],self.absolutes_base+absolute)
    for label in self.labels:
      if label.addr is None:
        raise ValueError(f"Label {label} is not linked")
      for lb in label.lb:
        self.code[lb].imm=(label.addr&0xff0000)>>16
      for lh in label.lh:
        self.code[lh].imm=(label.addr&0x00ff00)>>8
      for ll in label.ll:
        self.code[ll].imm=(label.addr&0x0000ff)