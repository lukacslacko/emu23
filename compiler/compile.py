from backend.api2 import Backend, PrimitiveType, Type, DataLoc, CodeLoc
from compiler.sta import statement
from compiler import sta, expression
from compiler.expression import Operator
from backend import api2


class StackElement:
    pass


class LocalVarDecl(StackElement):
    def __init__(self, name: str, v: DataLoc):
        self.name = name
        self.v = v

    def __str__(self):
        return f"local var {self.name} is {self.v}"

    def __repr__(self):
        return str(self)


class Block(StackElement):
    pass


class FunInfo:
    code: CodeLoc
    ret: DataLoc
    args: list[DataLoc]


stack = []
static_vars = dict()
funs = dict()


def _find_local_var(name: str) -> DataLoc:
    for s in reversed(stack):
        if isinstance(s, LocalVarDecl) and s.name == name:
            return s.v
    return None


def _find_var(name: str) -> DataLoc:
    if name in static_vars:
        return static_vars[name]
    return _find_local_var(name)


def _parse_type(tokens: list[str]) -> Type:
    if len(tokens) != 1:
        raise ValueError(f"Need single token type: {tokens}")
    return PrimitiveType(tokens[0])


def compute(e: expression.Expr, target: DataLoc, backend: Backend):
    if e.operator == Operator.LEAF:
        v = _find_var(e.operator_name)
        if v is not None:
            if v.type() != target.type():
                raise ValueError(
                    f"Different types of target {target} and source {v} in expression {e}"
                )
            backend.copy(source=v, target=target)
            return
        backend.set(target=target, value=int(e.operator_name))
        return
    if e.operator == Operator.UNARY:
        raise NotImplementedError(f"Unary operators not implemented in {e}")
    if e.operator == Operator.BINARY:
        left_temp = backend.create_temp_var(target.type())
        right_temp = backend.create_temp_var(target.type())
        compute(e.operands[0], left_temp, backend)
        compute(e.operands[1], right_temp, backend)
        backend.binary_operate(
            api2.BinaryOperation(e.operator_name), left_temp, right_temp, target
        )
        backend.release_temp_var(left_temp)
        backend.release_temp_var(right_temp)


def compile_decl(st: sta.Decl, backend: Backend):
    global static_vars, stack
    ty = _parse_type(st.type)
    name = st.name
    if st.storage == sta.Storage.LOCAL:
        if name in static_vars:
            raise ValueError(f"{name} is both static and local in {st}")
        stack.append(LocalVarDecl(name, backend.create_local_var(ty)))
    elif st.storage == sta.Storage.STATIC:
        if _find_local_var(name) is not None:
            raise ValueError(f"{name} is both local and static in {st}")
        static_vars[name] = backend.create_static_var(ty)


def compile_assignment(st: sta.Assignment, backend: Backend):
    rex = expression.parse(st.rvalue)
    lex = expression.parse(st.lvalue)
    if lex.operator != Operator.LEAF:
        raise ValueError(f"lvalue must be a leaf {st}")
    lvar = _find_var(lex.operator_name)
    if lvar is None:
        raise ValueError(f"Cannot find lvalue {lex.operator_name} in {st}")
    try:
        compute(rex, lvar, backend)
    except ValueError as e:
        raise ValueError(f"Computation error {e} in {st}")


def compile_block(st: sta.Block, backend: Backend):
    global stack
    stack.append(Block())
    backend.begin_block()
    compile(st.lines, backend)
    backend.end_block()
    while True:
        s = stack.pop()
        if isinstance(s, Block):
            break
        if isinstance(s, LocalVarDecl):
            backend.comment(f"compiler forgetting local var {s.name}: {s.v}")


def compile_fundef(st: sta.Fundef, backend: Backend):
    global funs, stack
    if len(stack) > 0:
        raise ValueError(f"Fundef with non-empty stack {st}, {stack}")
    if st.name in funs:
        raise ValueError(f"Function already defined {st.name} in {st}")
    info = FunInfo()
    info.code = backend.get_label(f"funstart_{st.name}")
    backend.link_label_to_here(info.code)
    ret_type = _parse_type(st.result[1])
    ret_name = st.result[0]
    arg_types = [_parse_type(input[1]) for input in st.inputs]
    info.ret, info.args = backend.begin_func(ret_type, arg_types)
    funs[st.name] = info
    stack.append(LocalVarDecl(ret_name, info.ret))
    for input, dl in zip(st.inputs, info.args):
        stack.append(LocalVarDecl(input[0], dl))
    compile(st.body, backend)
    backend.end_function()
    while stack:
        backend.comment(f"Compiler forgetting {stack.pop()}")


def compile(lines: list[list[str]], backend: Backend):
    sts = list(map(statement, lines))
    print("\n".join(list(map(str, sts))))
    for st in sts:
        backend.comment(str(st))
        if isinstance(st, sta.Decl):
            compile_decl(st, backend)
        elif isinstance(st, sta.Assignment):
            compile_assignment(st, backend)
        elif isinstance(st, sta.Block):
            compile_block(st, backend)
        elif isinstance(st, sta.Fundef):
            compile_fundef(st, backend)
        else:
            raise NotImplementedError(f"Cannot compile {st}")
