from enum import Enum

from paren import paren

def find_first(what: str, tokens: list[str]) -> int:
  i=0
  while i < len(tokens):
    if tokens[i]==what:
      return i
    i+=1+paren(tokens[i:])
  raise ValueError(f"Could not find {what} in {tokens}")

def stat(tokens: list[str]) -> int:
  return find_first(";", tokens)

class Statement:
  pass

class Storage(Enum):
  STATIC = "static"
  LOCAL = "local"

class Decl(Statement):
  storage: Storage
  name: str
  type: list[str]

  def __init__(self, storage: Storage, name: str, type: list[str]):
    self.storage = storage
    self.name = name
    self.type = type

  def __str__(self):
    return f"(Decl){self.storage} {self.type} {self.name}"

class Assignment(Statement):
  lvalue: list[str]
  rvalue: list[str]

  def __init__(self, lvalue: list[str], rvalue: list[str]):
    self.lvalue = lvalue
    self.rvalue = rvalue

  def __str__(self):
    return f"(Assignment){self.lvalue} {self.rvalue}"

class Block(Statement):
  lines: list[str]

  def __init__(self, tokens: list[str]):
    self.lines = []
    while tokens:
      s = stat(tokens)
      if s < 1:
        raise ValueError(s, tokens)
      self.lines.append(tokens[:s])
      tokens = tokens[s+1:]
  def __str__(self):
    return f"(Block){self.lines}"

class Break(Statement):
  def __init__(self):
    pass

  def __str__(self):
    return "(Break)"

class If(Statement):
  cond: list[str]
  body: list[str]
  # TODO else

  def __init__(self, cond: list[str], body: list[str]):
    self.cond = cond
    self.body = body

  def __str__(self):
    return f"(If) {self.cond} (then) {self.body}"

class While(Statement):
  cond: list[str]
  body: list[str]

  def __init__(self, cond: list[str], body: list[str]):
    self.cond = cond
    self.body = body

  def __str__(self):
    return f"(While) {self.cond} (do) {self.body}"

class For(Statement):
  statement1: list[str]
  cond: list[str]
  statement3: list[str]
  body: list[str]

  def __init__(self, sta1, cond, sta3, body):
    self.statement1 = sta1
    self.cond = cond
    self.statement3 = sta3
    self.body = body

  def __str__(self):
    return f"(For) ({self.statement1};{self.cond};{self.statement3}) (do) {self.body}"

class Fundef(Statement):
  name: str
  inputs: list[tuple[str, list[str]]]
  result: tuple[str, list[str]]
  body: list[str]

  def __init__(self, name, inputs, result, body):
    self.name = name
    self.inputs = inputs
    self.result = result
    self.body = body

  def __str__(self):
    return f"(Fundef) {self.name} ({self.inputs}) -> {self.result} (do) {self.body}"

class Return(Statement):
  def __init__(self):
    pass
  def __str__(self):
    return "(Return)"

def statement(line: list[str]) -> Statement:
  if line[0] in ["static", "local"] and line[2] == ":":
    return Decl(Storage(line[0]),line[1],line[3:])
  if line[0] == "break":
    if len(line) > 1:
      raise ValueError(f"Things after break: {line}")
    return Break()
  if line[0] == "if":
    cond = paren(line[1:])
    return If(line[2:cond+1], line[cond+2:])
  if line[0] == "while":
    cond = paren(line[1:])
    return While(line[2:cond+1], line[cond+2:])
  if line[0] == "for":
    q = paren(line[1:])
    w = stat(line[2:q+1])
    e = stat(line[w+3:q+1])
    return For(line[2:w+2],line[w+3:w+e+3],line[e+w+4:q+1],line[q+2:])
  if line[0] == "fun":
    name = line[1]
    args_end = paren(line[2:])
    args = line[3:args_end+2]
    inputs = []
    input_end = find_first(";", args)
    input_args = args[0: input_end]
    result_arg = args[input_end+1:]
    while len(input_args) > 0:
      if input_args[0] == ",":
        input_args = input_args[1:]
      input_name = input_args[0]
      if input_args[1] != ":":
        raise ValueError(f"Missing : in argument: {input_args} in {line}")
      input_type_end = find_first(",", input_args) if "," in input_args else len(input_args)
      input_type = args[2:input_type_end]
      inputs.append((input_name, input_type))
      input_args = input_args[input_type_end:]
    result_name = result_arg[0]
    if result_arg[1] != ":":
      raise ValueError(f"Missing : in result: {result_arg} in {line}")
    result_type = result_arg[2:]
    body = line[args_end+4:]
    return Fundef(name, inputs, (result_name, result_type), body)
  if line[0] == "return":
    return Return()
  if paren(line)==len(line)-1:
    return Block(line[1:-1])
  i=0
  while i < len(line):
    if line[i]==':=':
      return Assignment(line[:i],line[i+1:])
    if line[i]=='+=':
      return Assignment(line[:i],line[:i]+["+"]+line[i+1:])
    if line[i]=='-=':
      return Assignment(line[:i],line[:i]+["-"]+line[i+1:])
    if line[i]=='*=':
      return Assignment(line[:i],line[:i]+["*"]+line[i+1:])
    if line[i]=='&=':
      return Assignment(line[:i],line[:i]+["&"]+line[i+1:])
    if line[i]=='|=':
      return Assignment(line[:i],line[:i]+["|"]+line[i+1:])
    if line[i]=='^=':
      return Assignment(line[:i],line[:i]+["^"]+line[i+1:])
    i+=1+paren(line[i:])
  raise ValueError(line)
