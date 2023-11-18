from backend import Backend, Label, Register, Asm
from sym import Location

class LabelPy(Label):
  pass

class AsmPy(Asm):
  @staticmethod
  def name() -> str:
    return "Py"
  def __init__(self, body: str, label: LabelPy=None):
    self.body = body
    self.label = label
    self.linked = False

  def __str__(self):
    return f"AsmPy {self.body}, label {self.label}, linked {self.linked}"

  def __repr__(self):
    return str(self)

  def link(self, addr: int):
    if self.linked:
      return
    self.linked = True
    if "%" in self.body:
      if self.label is None:
        raise ValueError(f"No label for {addr} in {self}")
      self.body = self.body.replace("%", str(self.label.addr))
    self.body = f"""
    def line_{addr}() -> int:
      next_line = {addr + 1}
{self.body}
      return next_line
    """

class BackendPy(Backend):
  def __init__(self):
    pass

  def comment(self, comment: str) -> None:
    self.code.append(AsmPy(f"    # {comment}"))

  def label(self, name: str) -> LabelPy:
    label = LabelPy(name)
    self.labels.append(label)
    return label

  def link(self, data_segment_size: int=0):
    for addr, c in enumerate(self.code):
      c.link(addr)
    self.code.append(AsmPy(f"""
    from backend import Register, i8REGS
    REGISTERS = {{reg: 0 for reg in Register}}
    def make_i8(i: int) -> int:
      return ((i+0x80)%0x100)-0x80
    STACK = []

    MEM = [0] * {data_segment_size}

    DEBUG = True

    def debug():
      if DEBUG:
        print(curr_line, REGISTERS, STACK, MEM)
    
    last_line = {len(self.code)}
    curr_line = 0
    while curr_line < last_line:
      curr_line = eval(f'line_{{curr_line}}()')
      for i8reg in i8REGS:
        REGISTERS[i8reg] = make_i8(REGISTERS[i8reg])
      debug()
    """))

  def write_to_file(self, file_name: str):
    file_name = file_name + ".py"
    with open(file_name, "w") as f:
      for c in self.code:
        f.write("\n".join(map(lambda s: s[4:], c.body.split("\n"))))

  def link_label_to_here(self, label: Label):
    if not isinstance(label, LabelPy):
      raise TypeError("Want LabelPy")
    label.addr = len(self.code)

  def jump_if_zero_i8(self, cond: Register, label: Label):
    self.code.append(AsmPy(f"""
      if REGISTERS[{cond}] == 0:
        next_line = %
    """, label))

  def jump(self, label: Label):
    self.code.append(AsmPy(f"""
      next_line = %
    """, label))

  def push_i8(self, source: Register):
    self.stack_ptr += 1
    self.code.append(AsmPy(f"""
      STACK.append(REGISTERS[{source}])
    """))

  def pop_i8(self, target: Register):
    self.stack_ptr -= 1
    self.code.append(AsmPy(f"""
      REGISTERS[{target}] = STACK.pop()
    """))

  def set_i8(self, value: int, target: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{target}] = {value}
    """))

  def load_i8(self, loc: Location, target: Register):
    if loc.absolute is not None:
      self.code.append(AsmPy(f"""
      REGISTERS[{target}] = MEM[{loc.absolute}]
      """))
    elif loc.stack is not None:
      self.code.append(AsmPy(f"""
      REGISTERS[{target}] = STACK[{loc.stack-self.stack_ptr}]
      """))
    else:
      raise ValueError(f"Can't load from {loc}")
  
  def store_i8(self, loc: Location, source: Register):
    if loc.absolute is not None:
      self.code.append(AsmPy(f"""
      MEM[{loc.absolute}] = REGISTERS[{source}] 
      """))
    elif loc.stack is not None:
      self.code.append(AsmPy(f"""
      STACK[{loc.stack-self.stack_ptr}] = REGISTERS[{source}]
      """))
    else:
      raise ValueError(f"Can't store to {loc}")

  def copy_i8(self, source: Register, target: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{target}] = REGISTERS[{source}]
    """))

  def add_i8(self, left: Register, right: Register, result: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{result}] = REGISTERS[{left}] + REGISTERS[{right}]
    """))

  def sub_i8(self, left: Register, right: Register, result: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{result}] = REGISTERS[{left}] - REGISTERS[{right}]
    """))

  def mul_i8(self, left: Register, right: Register, result: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{result}] = REGISTERS[{left}] * REGISTERS[{right}]
    """))

  def gt_i8(self, left: Register, right: Register, result: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{result}] = (REGISTERS[{left}] > REGISTERS[{right}])
    """))
  
  def lt_i8(self, left: Register, right: Register, result: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{result}] = (REGISTERS[{left}] < REGISTERS[{right}])
    """))
  
  def and_i8(self, left: Register, right: Register, result: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{result}] = (REGISTERS[{left}] & REGISTERS[{right}])
    """))
  
  def or_i8(self, left: Register, right: Register, result: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{result}] = (REGISTERS[{left}] | REGISTERS[{right}])
    """))
  
  def xor_i8(self, left: Register, right: Register, result: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{result}] = (REGISTERS[{left}] ^ REGISTERS[{right}])
    """))
  
  def eq_i8(self, left: Register, right: Register, result: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{result}] = (REGISTERS[{left}] == REGISTERS[{right}])
    """))

  def ne_i8(self, left: Register, right: Register, result: Register):
    self.code.append(AsmPy(f"""
      REGISTERS[{result}] = (REGISTERS[{left}] != REGISTERS[{right}])
    """))

  def move_sp(self, diff: int):
    self.stack_ptr += diff
    self.code.append(AsmPy(f"""
      # Move stack pointer {diff}
      global STACK
      if {diff} >= 0:
        STACK += [0] * {diff}
      else:
        STACK = STACK[:{diff}]
    """))
