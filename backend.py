from enum import Enum
from sym import Label, Location, RodataHandle
import typ

class Register(Enum):
  REG0_I8 = 0
  REG1_I8 = 1
  REG0_PTR = 2
  REG1_PTR = 3
  REG0_BOOL = 4
  REG1_BOOL = 5
  REG0_U8 = 6
  REG1_U8 = 7
  REG0_I16 = 8
  REG1_I16 = 9
  REG0_U16 = 10
  REG1_U16 = 11
  REG0_I24 = 12
  REG1_I24 = 13
  REG0_U24 = 14
  REG1_U24 = 15

i8REGS=[
  Register.REG0_I8,
  Register.REG1_I8,
]

u8REGS=[
  Register.REG0_U8,
  Register.REG1_U8,
]

ptrREGS=[
  Register.REG0_PTR,
  Register.REG1_PTR,
]

boolREGS=[
  Register.REG0_BOOL,
  Register.REG1_BOOL,
]

i16REGS=[
  Register.REG0_I16,
  Register.REG1_I16,
]

u16REGS=[
  Register.REG0_U16,
  Register.REG1_U16,
]

i24REGS=[
  Register.REG0_I24,
  Register.REG1_I24,
]

u24REGS=[
  Register.REG0_U24,
  Register.REG1_U24,
]

class Asm:
  def __init__(self, s: str, label: Label = None):
    self.s = s
    self.label = label
  
  def bytes(self) -> int:
    return 1

  def __str__(self) -> str:
    return self.s + ("" if self.label is None else f" {self.label}")

  def __repr__(self) -> str:
    return str(self)


class DebugAsm(Asm):
  def bytes(self) -> int:
    return 0

  def __str__(self) -> str:
    return f"; {self.s}"

class Backend:
  stack_ptr: int = 0
  addr: int = 0
  code: list[Asm] = []
  labels: list[Label] = []
  handles: list[RodataHandle] = []
  entry: Label=None

  TYPES=typ.TYPES+[typ.Type("call",3)]

  @staticmethod
  def name() -> str:
    return "Backend"

  def comment(self, comment: str) -> None:
    self.code.append(DebugAsm(comment))

  def set_entry(self, entry: Label):
    self.entry=entry

  def add_rodata(self, name: str, data: bytes) -> RodataHandle:
    handle = RodataHandle(name, data)
    self.handles.append(handle)
    return handle

  def label(self,name: str) -> Label:
    label=Label(name)
    self.labels.append(label)
    return label

  def link(self, data_segment_size: int=0):
    for idx in range(len(self.code)):
      self.code[idx] = f"{idx:03}: {self.code[idx]}"

  def write_to_file(self, file_name: str):
    pass

  def link_label_to_here(self,label: Label):
    label.addr = len(self.code)

  def enter(self):
    self.code.append(Asm(f"Enter function"))

  def leave(self):
    self.code.append(Asm(f"Leave function"))

  def push_ptr(self, source: Register):
    self.code.append(Asm(f"Push ptr {source}"))

  def pop_ptr(self, target: Register):
    self.code.append(Asm(f"Pop ptr {target}"))

  def set_ptr_from_int(self, value: int, target: Register):
    self.code.append(Asm(f"Set ptr {target} from int {value}"))

  def set_ptr_from_loc(self, value: Location, target: Register):
    self.code.append(Asm(f"Set ptr {target} from loc {value}"))

  def load_ptr(self, loc: Location, target: Register):
    self.code.append(Asm(f"Load ptr {target} from loc {loc}"))

  def store_ptr(self, loc: Location, source: Register):
    self.code.append(Asm(f"Store ptr {source} to loc {loc}"))

  def copy_ptr(self, source: Register, target: Register):
    self.code.append(Asm(f"Copy ptr {source} to ptr {target}"))

  def add_ptr(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Add ptr {left} to ptr {right}"))

  def sub_ptr(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Sub ptr {left} to ptr {right}"))

  def and_ptr(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"And ptr {left} to ptr {right}"))

  def or_ptr(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Or ptr {left} to ptr {right}"))

  def xor_ptr(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Xor ptr {left} to ptr {right}"))

  def cast_i8_to_ptr(self, source: Register, target: Register):
    self.code.append(Asm(f"Cast i8 to ptr {source} to ptr {target}"))

  def load_i8_from_ptr(self, source: Register, target: Register):
    self.code.append(Asm(f"Load i8 from ptr {source} to {target}"))

  def store_i8_to_ptr(self, source: Register, target: Register):
    self.code.append(Asm(f"Store i8 from {source} to ptr {target}"))

  def load_ptr_from_ptr(self, source: Register, target: Register):
    self.code.append(Asm(f"Load ptr from ptr {source} to {target}"))

  def store_ptr_to_ptr(self, source: Register, target: Register):
    self.code.append(Asm(f"Store ptr from {source} to ptr {target}"))

  def cast_ptr_to_i8(self, source: Register, target: Register):
    pass

  def cast_i8_to_bool(self, source: Register, target: Register):
    pass

  def cast_bool_to_i8(self, source: Register, target: Register):
    pass

  def jump_if_zero_i8(self, cond: Register, label: Label):
    self.code.append(Asm(f"Jump if i8 {cond} is zero", label))

  def jump(self, label: Label):
    self.code.append(Asm(f"Jump", label))

  def push_i8(self, source: Register):
    self.stack_ptr += 1
    self.code.append(Asm(f"Pushing i8 {source}"))

  def pop_i8(self, target: Register):
    self.stack_ptr -= 1
    self.code.append(Asm(f"Popping i8 {target}"))
  
  def set_i8(self, value: int, target: Register):
    self.code.append(Asm(f"Setting i8 {target} to {value}"))
  
  def load_i8(self, loc: Location, target: Register):
    self.code.append(Asm(f"Load i8 from {loc} to {target}"))

  def store_i8(self, loc: Location, source: Register):
    self.code.append(Asm(f"Store i8 from {source} to {loc}"))

  def copy_i8(self, source: Register, target: Register):
    self.code.append(Asm(f"Copy i8 from {source} to {target}"))

  def add_i8(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Add i8 {left} and {right} to {result}"))

  def sub_i8(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Sub i8 {left} and {right} to {result}"))

  def mul_i8(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Multiply i8 {left} and {right} to {result}"))

  def gt_i8(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Is i8 {left} > {right} to {result}"))

  def lt_i8(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Is i8 {left} < {right} to {result}"))

  def and_i8(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"And i8 {left} and {right} to {result}"))

  def or_i8(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Or i8 {left} and {right} to {result}"))

  def xor_i8(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Xor i8 {left} and {right} to {result}"))

  def eq_i8(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Is i8 {left} == {right} to {result}"))

  def ne_i8(self, left: Register, right: Register, result: Register):
    self.code.append(Asm(f"Is i8 {left} != {right} to {result}"))

  def move_sp(self, diff: int):
    self.stack_ptr += diff
    self.code.append(Asm(f"Move stack pointer {diff}"))