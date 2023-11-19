from backend.api2 import Backend, Type, CodeLoc, DataLoc


class DefaultCodeLocation(CodeLoc):
    def __init__(self, line: int):
        self._line = line

    def __str__(self):
        return f"code@{self._line}"


class DefaultDataLocation(DataLoc):
    def __init__(self, loc: str, typ: Type):
        self._loc = loc
        self._type = typ

    def __str__(self):
        return f"@{self._loc}({self._type.name})"

    def __repr__(self):
        return str(self)

    def size(self) -> int:
        return 1


class DefaultBackend(Backend):
    def __init__(self):
        self._code = []
        self._stack_ptr = 0
        self._mem_ptr = 0

    def name() -> str:
        return "Default"

    def comment(self, comment: str) -> None:
        self._code.append(f"; {comment}")

    def link(self):
        pass

    def write_to_file(self, filename: str):
        with open(filename, "w") as f:
            f.write("\n".join(self._code))

    def create_local_var(self, t: Type) -> DefaultDataLocation:
        v = DefaultDataLocation(f"stack@{self._stack_ptr}", t)
        self._stack_ptr += v.size()
        self._code.append(f"create local var {v}")
        return v

    def dispose_local_var(self, v: DefaultDataLocation) -> None:
        self._stack_ptr -= v.size()
        self._code.apped(f"dispose local var {v}")

    def begin_func(
        self, return_type: Type, args: list[Type]
    ) -> tuple[DataLoc, list[DataLoc]]:
        self._ret_val = self.create_local_var(return_type)
        self._arg_vals = [self.create_local_var(t) for t in args]
        return (self._ret_val, self._arg_vals)

    def end_func(self) -> None:
        for v in reversed(self._arg_vals):
            self._dispose_local_var(v)
