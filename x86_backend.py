from backend import Asm, Backend, Register
from sym import Location
from typ import Type

class AsmX86(Asm):
  def __init__(self, s: str, size: int):
    self.s = s
    self.size = size

  def bytes(self) -> int:
    return self.size

REG = {
  Register.REG0_I8: "AX",
  Register.REG1_I8: "BX",
}

class BackendX86(Backend):
  @staticmethod
  def name() -> str:
    return "X86"
  TYPES = [
    Type("i8", 2),
  ]

  def push_i8(self, source: Register) -> list[Asm]:
    self.stack_ptr += 2
    return [AsmX86(f"push {REG[source]}", 1)]
  def pop_i8(self, target: Register) -> list[Asm]:
    self.stack_ptr -= 2
    return [AsmX86(f"pop {REG[target]}", 1)]
  def set_i8(self, value: int, target: Register) -> list[Asm]:
    return [AsmX86(f"mov {REG[target]}, {value}", 3)]
  def store_i8(self, loc: Location, target: Register) -> list[Asm]:
    if loc.absolute is not None:
      return [AsmX86(f"mov [{loc.absolute}], {REG[target]}", 5)]
    if loc.stack is not None:
      return [AsmX86(f"mov [SP+{self.stack_ptr-loc.stack}], {REG[target]}", 5)]
  def load_i8(self, loc: Location, target: Register) -> list[Asm]:
    if loc.absolute is not None:
      return [AsmX86(f"mov {REG[target]}, [{loc.absolute}]", 5)]
    if loc.stack is not None:
      return [AsmX86(f"mov {REG[target]}, [SP+{self.stack_ptr-loc.stack}]", 5)]
  def copy_i8(self, source: Register, target: Register) -> list[Asm]:
    if source == target:
      return []
    return [AsmX86(f"mov {REG[target]}, {REG[source]}", 1)]
  def add_i8(self, left: Register, right: Register, result: Register) -> list[Asm]:
    if result == left:
      return [AsmX86(f"add {REG[left]}, {REG[right]}", 1)]
    elif result == right:
      return [AsmX86(f"add {REG[right]}, {REG[left]}", 1)]
    else:
      return [
        AsmX86(f"mov {REG[result]}, {REG[right]}", 1), 
        AsmX86(f"add {REG[result]}, {REG[left]}", 1)]
  def mul_i8(self, left: Register, right: Register, result: Register) -> list[Asm]:
    if result == left:
      return [AsmX86(f"add {REG[left]}, {REG[right]}", 1)]
    elif result == right:
      return [AsmX86(f"add {REG[right]}, {REG[left]}", 1)]
    else:
      return [
        AsmX86(f"mov {REG[result]}, {REG[right]}", 1), 
        AsmX86(f"mul {REG[result]}, {REG[left]}", 1)]
  def move_sp(self, diff: int) -> list[Asm]:
    self.stack_ptr += diff
    if diff > 0:
      return [AsmX86(f"sub SP, {diff}", 3)]
    else:
      return [AsmX86(f"add SP, {-diff}", 3)]