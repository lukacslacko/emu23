
def line_0() -> int:
  next_line = 1
# (Decl)Storage.LOCAL ['i8'] u
  return next_line

def line_1() -> int:
  next_line = 2

  # Move stack pointer 1
  global STACK
  if 1 >= 0:
    STACK += [0] * 1
  else:
    STACK = STACK[:1]

  return next_line

def line_2() -> int:
  next_line = 3
# (Decl)Storage.LOCAL ['i8'] v
  return next_line

def line_3() -> int:
  next_line = 4

  # Move stack pointer 1
  global STACK
  if 1 >= 0:
    STACK += [0] * 1
  else:
    STACK = STACK[:1]

  return next_line

def line_4() -> int:
  next_line = 5
# (Assignment)['v'] ['42']
  return next_line

def line_5() -> int:
  next_line = 6

  REGISTERS[Register.REG0_8] = 42

  return next_line

def line_6() -> int:
  next_line = 7

  STACK[-1] = REGISTERS[Register.REG0_8]
  
  return next_line

def line_7() -> int:
  next_line = 8
# (Assignment)['u'] ['110']
  return next_line

def line_8() -> int:
  next_line = 9

  REGISTERS[Register.REG0_8] = 110

  return next_line

def line_9() -> int:
  next_line = 10

  STACK[-2] = REGISTERS[Register.REG0_8]
  
  return next_line

def line_10() -> int:
  next_line = 11
# (Decl)Storage.LOCAL ['i8'] y
  return next_line

def line_11() -> int:
  next_line = 12

  # Move stack pointer 1
  global STACK
  if 1 >= 0:
    STACK += [0] * 1
  else:
    STACK = STACK[:1]

  return next_line

def line_12() -> int:
  next_line = 13
# (Assignment)['u'] ['100']
  return next_line

def line_13() -> int:
  next_line = 14

  REGISTERS[Register.REG0_8] = 100

  return next_line

def line_14() -> int:
  next_line = 15

  STACK[-3] = REGISTERS[Register.REG0_8]
  
  return next_line

def line_15() -> int:
  next_line = 16
# (Break)
  return next_line

def line_16() -> int:
  next_line = 17

  next_line = 20

  return next_line

def line_17() -> int:
  next_line = 18
# (Assignment)['u'] ['115']
  return next_line

def line_18() -> int:
  next_line = 19

  REGISTERS[Register.REG0_8] = 115

  return next_line

def line_19() -> int:
  next_line = 20

  STACK[-3] = REGISTERS[Register.REG0_8]
  
  return next_line

def line_20() -> int:
  next_line = 21

  # Move stack pointer -1
  global STACK
  if -1 >= 0:
    STACK += [0] * -1
  else:
    STACK = STACK[:-1]

  return next_line

def line_21() -> int:
  next_line = 22
# (Assignment)['v'] ['u']
  return next_line

def line_22() -> int:
  next_line = 23

  REGISTERS[Register.REG0_8] = STACK[-2]
  
  return next_line

def line_23() -> int:
  next_line = 24

  STACK[-1] = REGISTERS[Register.REG0_8]
  
  return next_line

from backend import Register, i8REGS
REGISTERS = {reg: 0 for reg in Register}
def make_i8(i: int) -> int:
  return ((i+0x80)%0x100)-0x80
STACK = []

MEM = [0] * 0

DEBUG = True

def debug():
  if DEBUG:
    print(curr_line, REGISTERS, STACK, MEM)

last_line = 24
curr_line = 0
while curr_line < last_line:
  curr_line = eval(f'line_{curr_line}()')
  for i8reg in i8REGS:
    REGISTERS[i8reg] = make_i8(REGISTERS[i8reg])
  debug()
