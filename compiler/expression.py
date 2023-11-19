from enum import Enum

from compiler.paren import paren


class Operator(Enum):
    LEAF = "leaf"
    BINARY = "binary"
    UNARY = "unary"


class Expr:
    operator: Operator
    operator_name: str
    operands: list["Expr"]

    def __init__(
        self, operator: Operator, operator_name: str = None, operands: list["Expr"] = []
    ):
        self.operator = operator
        self.operator_name = operator_name
        self.operands = operands

    def __expr__(self):
        return str(self)

    def __str__(self):
        return f"{self.operator}'{self.operator_name}'({', '.join(map(str, self.operands))})"


def find_first(token: str, tokens: list[str]) -> int:
    idx = 0
    while idx < len(tokens):
        if tokens[idx] == token:
            return idx

        idx += 1 + paren(tokens[idx:])
    return None


def parse(tokens: list[str]) -> Expr:
    if tokens[0] == "(" and paren(tokens) == len(tokens) - 1:
        return parse(tokens[1:-1])
    if len(tokens) == 1:
        return Expr(Operator.LEAF, tokens[0])
    if tokens[0] in ["*", "&"]:
        return Expr(Operator.UNARY, tokens[0], [parse(tokens[1:])])
    for op in ["+", "-", "*", "/", ">", "<", "=="]:
        idx = find_first(op, tokens)
        if idx is not None:
            return Expr(
                Operator.BINARY, op, [parse(tokens[:idx]), parse(tokens[idx + 1 :])]
            )
    raise ValueError(f"Can't parse expression {tokens}")
