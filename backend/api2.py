from enum import Enum
from typing import Any, Union


class PrimitiveType(Enum):
    BOOL = "bool"
    I8 = "i8"
    I16 = "i16"
    PTR = "ptr"

class ComplexType:
    size: int
    align: int

    def __init__(self, size: int, align: int):
        self.size = size
        self.align = align


Type = Union[PrimitiveType, ComplexType]


class CodeLoc:
    pass


class DataLoc:
    def type(self) -> Type:
        return None


class BinaryOperation(Enum):
    ADD = "+"
    SUB = "-"
    XOR = "xor"
    AND = "and"
    OR = "or"
    GT = "gt"
    LT = "lt"
    GTE = "gte"
    LTE = "lte"
    EQ = "eq"
    NE = "ne"
    MUL = "*"
    # div
    # mod
    # TODO: more operations


class UnaryOperation(Enum):
    NOT = "not"
    NEG = "neg"
    ADDR = "addrof"
    # NOTE: more operations


class Backend:
    def name() -> str:
        return "???"

    def set_entry(self, entry: CodeLoc) -> None:
        pass

    def asmfunc(self, asm: str) -> None:
        pass

    def link(self) -> None:
        pass

    def write_to_file(self, filename: str) -> None:
        pass

    def create_static_var(self, t: Type) -> DataLoc:
        pass

    def get_label(self, name: str) -> CodeLoc:
        pass

    def link_label_to_here(self, label: CodeLoc) -> None:
        pass

    def begin_func(
        self, return_type: Type, args: list[Type]
    ) -> tuple[DataLoc, list[DataLoc]]:
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

    def binary_operate(
        self, op: BinaryOperation, left: DataLoc, right: DataLoc, result: DataLoc
    ) -> None:
        pass

    def unary_operate(
        self, op: UnaryOperation, source: DataLoc, target: DataLoc
    ) -> None:
        pass

    def break_(self, level: int) -> None:
        pass

    def end_block(self) -> None:
        pass

    def return_(self) -> None:
        pass

    def end_function(self) -> None:
        self.return_()

    def to_complex_type(primitive: PrimitiveType) -> ComplexType:
        pass

    def offset(base: DataLoc, offset: int, primitive: PrimitiveType) -> DataLoc:
        pass
