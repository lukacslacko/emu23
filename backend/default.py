from backend.api2 import Backend, BinaryOperation, Type, CodeLoc, DataLoc


class DefaultCodeLocation(CodeLoc):
    def __init__(self, line: int):
        self._line = line

    def __str__(self):
        return f"code@{self._line}"


class DefaultDataLocation(DataLoc):
    def __init__(self, loc: str, typ: Type):
        self._loc = loc
        self._type = typ

    def type(self) -> Type:
        return self._type

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
        self._tempvars = set()

    def name() -> str:
        return "Default"

    def comment(self, comment: str) -> None:
        self._code.append(f"; {comment}")

    def link(self):
        pass

    def write_to_file(self, filename: str):
        with open(filename, "w") as f:
            f.write("\n".join(self._code))

    def copy(self, source: DefaultDataLocation, target: DefaultDataLocation):
        self._code.append(f"copy {source} to {target}")

    def set(self, target: DefaultDataLocation, value):
        self._code.append(f"set {target} to {value}")

    def binary_operate(
        self, op: BinaryOperation, left: DataLoc, right: DataLoc, result: DataLoc
    ) -> None:
        self._code.append(
            f"binary operate {op} on left {left} and right {right} into {result}"
        )

    def create_static_var(self, t: Type) -> DefaultDataLocation:
        v = DefaultDataLocation(f"mem@{self._mem_ptr}", t)
        self._mem_ptr += v.size()
        self._code.append(f"create static var {v}")
        return v

    def create_local_var(self, t: Type) -> DefaultDataLocation:
        v = DefaultDataLocation(f"stack@{self._stack_ptr}", t)
        self._stack_ptr += v.size()
        self._code.append(f"create local var {v}")
        return v

    def _dispose_local_var(self, v: DefaultDataLocation) -> None:
        self._stack_ptr -= v.size()
        self._code.append(f"dispose local var {v}")

    def create_temp_var(self, t: Type) -> DefaultDataLocation:
        idx = max(self._tempvars) + 1 if self._tempvars else 0
        self._tempvars.add(idx)
        v = DefaultDataLocation(f"Reg {idx}", t)
        self._code.append(f"create temp var {v}")
        return v

    def release_temp_var(self, tvar: DataLoc) -> None:
        idx = int(tvar._loc.split(" ")[1])
        self._tempvars.remove(idx)
        self._code.append(f"release temp var {tvar}")

    def begin_func(
        self, return_type: Type, args: list[Type]
    ) -> tuple[DataLoc, list[DataLoc]]:
        self._ret_val = self.create_local_var(return_type)
        self._arg_vals = [self.create_local_var(t) for t in args]
        return (self._ret_val, self._arg_vals)

    def end_function(self) -> None:
        for v in reversed(self._arg_vals):
            self._dispose_local_var(v)
