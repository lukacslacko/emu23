from enum import Enum

class Type(Enum):
  BOOL = "bool"
  INT8 = "i8"
  INT16 = "i16"
  PTR = "ptr"

class Operation(Enum):
  ADD = "add"
  SUB = "sub"
  # etc

class Location:
  pass

class CodeLocation(Location):
  pass

class DataLocation(Location):
  _typ: Type

class Backend:
  def name() -> str:
    return "???"

  ###########################################
  # Methods callable only outside of a block.
  ###########################################

  def link(self):
    pass

  def write_to_file(self, filename: str):
    pass

  def REG(self, num: int, type: Type) -> DataLocation:
    raise ValueError(f"Too many registers!")

  def BREAK_COUNTER(self) -> DataLocation:
    pass

  def begin_block(self) -> CodeLocation:
    pass

  ###########################################
  # Methods only callable outside a function.
  ###########################################

  def begin_function(self, return_type: Type, args: list[Type]) -> tuple[CodeLocation, DataLocation, list[DataLocation]]:
    pass

  ##########################################
  # Methods only callable inside a function.
  ##########################################

  def end_function(self) -> None:
    pass

  #######################################
  # Methods only callable within a block.
  #######################################

  def end_block(self):
    pass

  def break_block(self, level: int):
    pass
  
  ################################################
  # Methods callable within or outside of a block.
  ################################################

  def call(self, func: CodeLocation, return_type: Type, args: list[DataLocation]) -> DataLocation:
    pass
  
  def create_static_var(t: Type) -> DataLocation:
    pass

  def create_local_var(t: Type) -> DataLocation:
    pass

  def comment(self, comment: str):
    pass

  def execute_block(self, block: CodeLocation):
    pass

  def set_immediate(self, target: DataLocation, value: int):
    pass

  def jump(self, target: CodeLocation):
    pass

  def jump_if_zero(self, target: CodeLocation, condition: DataLocation):
    pass

  def jump_if_true(self, target: CodeLocation, condition: DataLocation):
    pass

  def jump_if_false(self, target: CodeLocation, condition: DataLocation):
    pass

  def push(self, source: DataLocation):
    pass

  def pop(self, target: DataLocation):
    pass

  def copy(self, source: DataLocation, target: DataLocation):
    pass

  def operate(
    self, 
    op: Operation, 
    left: DataLocation, 
    right: DataLocation, 
    result: DataLocation):
    pass


