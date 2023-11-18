from enum import Enum

class CodeLoc:
  pass

class DataLoc:
  pass

class Operation(Enum):
  ADD = 'add'
  SUB = 'sub'
  # TODO: more operations

class Type(Enum):
  BOOL = 'bool'
  I8 = 'i8'
  I16 = 'i16'
  PTR = 'ptr'

class Backend:
  def name() -> str:
    return '???'

  def set_entry(self, entry: CodeLoc) -> None:
    pass

  def link(self) -> None:
    pass

  def write_to_file(self, filename: str) -> None:
    pass

  def cast(self, source: DataLoc, target: DataLoc) -> None:
    pass

  def create_static_var(self, t: Type) -> DataLoc:
    pass

  def get_label(self) -> CodeLoc:
    pass

  def link_label_to_here(self, label: CodeLoc) -> None:
    pass

  def begin_func(self, return_type: Type, args: list[Type]) -> tuple[DataLoc,list[DataLoc]]:
    pass

  def begin_block(self) -> None:
    pass

  def create_local_var(self, t: Type) -> DataLoc:
    pass

  def copy(self, source: DataLoc, target: DataLoc) -> None:
    pass

  def set(self, target: DataLoc, value: Any) -> None:
    pass

  def comment(self, comment: str) -> None:
    pass

  def create_temp_var(self, t: Type) -> DataLoc:
    pass

  def release_temp_var(self, tvar: DataLoc) -> None:
    pass

  def jump(self, target: CodeLoc) -> None:
    pass

  def jump_ptr(self, target: DataLoc) -> None:
    pass

  def jump_if_zero(self, cond: DataLoc, target: CodeLoc) -> None:
    pass

  def jump_if_not_zero(self, cond: DataLoc, target: CodeLoc) -> None:
    pass

  def call(self, func: CodeLoc, args: list[DataLoc], target: DataLoc) -> None:
    pass

  def call_ptr(self, func: DataLoc, args: list[DataLoc], target: DataLoc) -> None:
    pass

  def operate(self, op: Operation, left: DataLoc, right: DataLoc, result: DataLoc) -> None:
    pass

  def break(self, level: int) -> None:
    pass

  def end_block(self):
    pass

  def end_function(self) -> None:
    pass
