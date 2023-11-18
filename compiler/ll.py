from sta import stat, statement, Decl, Assignment, Storage, Block, Break, If, While, For, Fundef
import sym
from typ import Type, parse_type, update_types
import expression
from expression import Expr, Operator
from backend import Backend, Register, Asm, DebugAsm
from emu23_backend import BackendEmu23
from x86_backend import BackendX86
from py_backend import BackendPy



def symbol(e: Expr) -> sym.Location:
  if e.operator != Operator.LEAF:
    raise ValueError(f"Is not a symbol {e}")
  return sym.get(e.operator_name)

TARGET0 = {8: Register.REG0_I8, "ptr": Register.REG0_PTR}
TARGET1 = {8: Register.REG1_I8, "ptr": Register.REG1_PTR}

def compute(e: Expr, backend: Backend, targets: dict[int, Register]) -> None:
  if e.operator == Operator.LEAF:
    if sym.get(e.operator_name):
      s = sym.get(e.operator_name)
      if s.type.name == "i8":
        return backend.load_i8(s.loc, targets[8])
      if s.type.name == "ptr":
        return backend.load_ptr(s.loc, targets["ptr"])
      raise ValueError(f"Can't handle strange type data {e}")
    else:
      val = e.operator_name
      valtype = "i8"
      val = int(val)
      if val < -127 or val > 127:
        raise ValueError(f"Not an i8 {val}")
      backend.set_i8(val, targets[8])
      return
  if e.operator == Operator.UNARY:
    if e.operator_name == "&":
      operand = e.operands[0]
      if operand.operator != Operator.LEAF:
        raise ValueError(f"Can't compute non-leaf address {e}")
      leaf_sym = sym.get(operand.operator_name)
      backend.set_ptr_from_loc(leaf_sym.loc, targets["ptr"])
      return
    if e.operator_name == "*":
      compute(e.operands[0], backend, TARGET0)
      backend.load_i8_from_ptr(TARGET0["ptr"], targets[8])
      return
  if e.operator == Operator.BINARY:
    compute(e.operands[0], backend, TARGET0)
    backend.push_i8(Register.REG0_I8)
    compute(e.operands[1], backend, TARGET1)
    backend.pop_i8(Register.REG0_I8)
    OPS = {
      "+": backend.add_i8, 
      "*": backend.mul_i8, 
      ">": backend.gt_i8, 
      "-": backend.sub_i8,
      "<": backend.lt_i8,
      "&": backend.and_i8,
      "|": backend.or_i8,
      "^": backend.xor_i8,
      "==":backend.eq_i8,
      "!=":backend.ne_i8,
    }
    OPS[e.operator_name](Register.REG0_I8, Register.REG1_I8, targets[8])
    return
  raise ValueError(f"Can't compute {e}")
  
data_ptr = 0

def compile(lines: list[list[str]], backend: Backend) -> None:
  global data_ptr
  
  sts = list(map(statement, lines))
  print("\n".join(list(map(str, sts))))

  print("Generating code...")

  for st in sts:
    if isinstance(st, Decl):
      backend.comment(str(st))
      ty = parse_type(st.type)
      name = st.name
      if st.storage == Storage.STATIC:
        loc = sym.Location.absolute(data_ptr)
        data_ptr += ty.size
      if st.storage == Storage.LOCAL:
        # TODO batch up local variable creation
        loc = sym.Location.stack(backend.stack_ptr)
        backend.move_sp(ty.size)
      sym.add(name, loc, ty)
    elif isinstance(st, Assignment):
      backend.comment(str(st))
      rex = expression.parse(st.rvalue)
      lex = expression.parse(st.lvalue)
      compute(rex, backend, TARGET0)
      left_symbol = symbol(lex)
      if left_symbol.type.name == "i8":
        backend.store_i8(left_symbol.loc, Register.REG0_I8)
      elif left_symbol.type.name == "ptr":
        backend.store_ptr(left_symbol.loc, Register.REG0_PTR)
      else:
        raise ValueError(f"Can't store to {left_symbol}")
    elif isinstance(st, Block):
      sym.push()
      end_of_block = backend.label("end-of-block")
      sym.add("__end_of_block", sym.Location.code(end_of_block), parse_type(["ptr"]))
      compile(st.lines, backend)
      backend.link_label_to_here(end_of_block)
      backend.move_sp(-sym.total_local_stack_space())
      sym.pop()
    elif isinstance(st, Break):
      backend.comment(str(st))
      backend.jump(sym.get("__end_of_block").loc.label)
    elif isinstance(st, If):
      backend.comment(str(st))
      compute(expression.parse(st.cond), backend, TARGET0)
      label = backend.label(f"if-after")
      backend.jump_if_zero_i8(TARGET0[8], label)
      compile(find_lines(st.body + [";"]), backend)
      backend.link_label_to_here(label)
    elif isinstance(st, While):
      backend.comment(str(st))
      head = backend.label("while-head")
      backend.link_label_to_here(head)
      after = backend.label("while-after")
      compute(expression.parse(st.cond), backend, TARGET0)
      backend.jump_if_zero_i8(TARGET0[8], after)
      compile(find_lines(st.body + [";"]), backend)
      backend.jump(head)
      backend.link_label_to_here(after)
    elif isinstance(st, For):
      backend.comment(str(st))
      compile(find_lines(st.statement1 + [";"]), backend)
      head = backend.label("for-head")
      backend.link_label_to_here(head)
      after = backend.label("for-after")
      compute(expression.parse(st.cond), backend, TARGET0)
      backend.jump_if_zero_i8(TARGET0[8], after)
      compile(find_lines(st.body + [";"]), backend)
      compile(find_lines(st.statement3 + [";"]), backend)
      backend.jump(head)
      backend.link_label_to_here(after)
    elif isinstance(st, Fundef):
      backend.comment(str(st))
      sym.push()
      stack_offset=0
      ty=parse_type(st.result[1])
      sym.add(st.result[0], Location.stack(backend.stack_ptr+stack_offset), ty)
      stack_pos+=ty
      for arg in st.inputs:
        ty=parse_type(arg[1])
        sym.add(arg[0], Location.stack(backend.stack_ptr+stack_offset), ty)
        stack_pos+=ty
      stack_offset+=parse_type(["call"]).size
      backend.stack_ptr+=stack_offset
      after = backend.label("fundef-after")
      backend.jump(after)
      head = backend.label("fundef-head")
      backend.link_label_to_here(head)
      backend.enter()
      compile(find_lines(st.body + [";"]), backend)
      backend.leave()
      backend.link_label_to_here(after)
      backend.stack_ptr-=stack_offset
      sym.pop()
      sym.add(st.name, sym.Location.code(head), parse_type(["ptr"]))
    else:
      raise ValueError(f"Strange statement {st}")

backend = BackendEmu23()
# backend = Backend()
# backend = BackendX86()
# backend = BackendPy()

if hasattr(backend, "TYPES"):
  update_types(backend.TYPES)

with open("input.ll", "r") as f:
  tokens = parse(f.read())
  l = find_lines(tokens)
  print("\n".join(map(str, l)))
  print("\nCompiling...")
  compile(l, backend)
  backend.link(data_ptr)
  print("\nCode:")
  backend.write_to_file("linked")
  if not isinstance(backend, BackendPy):
    print("\n".join(map(str, backend.code)))#enumerate(backend.code))))
