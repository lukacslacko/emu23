class Type:
  name: str
  size: int

  def __init__(self, name: str, size: int):
    self.name = name
    self.size = size

  def __str__(self):
    return f"{self.name}({self.size})"

TYPES = [
  Type("i8", 1),
  Type("ptr", 3),
]

def update_types(new_types: list[Type]) -> None:
  global TYPES
  TYPES = new_types

def parse_type(tokens: list[str]) -> Type:
  for t in TYPES:
    if t.name == tokens[0]:
      return t
    
  raise ValueError(f"Unknown type {tokens[0]}")
  