from backend.api2 import Backend, Type, DataLoc, CodeLoc
from compiler.sta import statement
from compiler import sta


class StackElement:
    pass


class LocalVarDecl(StackElement):
    def __init__(self, v: DataLoc):
        self._v = v


stack = []
local_vars = dict()


def compile_decl(st: sta.Decl, backend: Backend):
    if len(st.type) != 1:
        raise ValueError(f"Require single token type: {st}")
    ty = Type(st.type[0])
    name = st.name
    local_vars[name] = backend.create_local_var(ty)
    stack.append(local_vars[name])


def compile(lines: list[list[str]], backend: Backend):
    sts = list(map(statement, lines))
    print("\n".join(list(map(str, sts))))
    for st in sts:
        backend.comment(str(st))
        if isinstance(st, sta.Decl):
            compile_decl(st, backend)
        else:
            raise NotImplementedError(f"Cannot compile {st}")
