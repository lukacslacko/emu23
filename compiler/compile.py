from backend.api2 import Backend, Type, DataLoc, CodeLoc
from compiler.sta import statement
from compiler import sta


class StackElement:
    pass


class LocalVarDecl(StackElement):
    def __init__(self, name: str, v: DataLoc):
        self.name = name
        self.v = v


stack = []
static_vars = dict()


def _find_local_var(name: str) -> DataLoc:
    for s in reversed(stack):
        if isinstance(s, LocalVarDecl) and s.name == name:
            return s.v
    return None


def _find_var(name: str) -> DataLoc:
    if name in static_vars:
        return static_vars[name]
    return _find_local_var(name)


def compile_decl(st: sta.Decl, backend: Backend):
    if len(st.type) != 1:
        raise ValueError(f"Require single token type: {st}")
    ty = Type(st.type[0])
    name = st.name
    if st.storage == sta.Storage.LOCAL:
        if name in static_vars:
            raise ValueError(f"{name} is both static and local in {st}")
        stack.append(LocalVarDecl(name, backend.create_local_var(ty)))
    elif st.storage == sta.Storage.STATIC:
        if _find_local_var(name) is not None:
            raise ValueError(f"{name} is both local and static in {st}")
        static_vars[name] = backend.create_static_var(ty)


def compile(lines: list[list[str]], backend: Backend):
    sts = list(map(statement, lines))
    print("\n".join(list(map(str, sts))))
    for st in sts:
        backend.comment(str(st))
        if isinstance(st, sta.Decl):
            compile_decl(st, backend)
        else:
            raise NotImplementedError(f"Cannot compile {st}")
