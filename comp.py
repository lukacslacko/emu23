def comp(lines, labels, pas=0):
  result = dict()
  addr = 0xC000
  insts = ["nop", "brk", "psh", "pop", "LDA", "ror", "tas", "tbs", "tcs", "tsa", "tsb", "tsc", "tcrah", "tcral", "tcpch", "tcpcl", "add", "sub", "or", "and", "xor", "tma", "tcm", "debug", None, "CLZ", "SEZ", "CLC", "SEC"]
  prefs = {"cc": 7, "cs": 6, "eq": 5, "ne": 4}
  for line in lines:
    #print("Compiling ", line)
    if not line or line[0] == ";":
      continue
    if line[0] == '.':
      if line.startswith('.b '):
        if line[3]=='\'':
          result[addr]=ord(line[4])
        else:
          result[addr]=int(line[3:])
        addr+=1
      if line.startswith('.org '):
        addr = int(line[5:])
      continue
    line = line.lower()
    if line[-1] == ":":
      labels[line[:-1]] = addr
      continue
    inst = 0
    pref = line[:2]
    if pref in prefs:
      inst = prefs[pref]
      line = line[2:]
    if line in insts:
      inst += 8*insts.index(line)
      result[addr] = inst
      addr += 1
      continue
    if pas == 1 and line[:3] == "lda":
      result[addr] = 4*8+inst
      addr += 1
      expr = line[4:]
      val = 0
      if expr.endswith("+1"):
        val = 1
        expr = expr[:-2]
      if expr[-1] == "l":
        val += labels[expr[:-1]]
        val &= 0xFF
      elif expr[-1] == "h":
        val += labels[expr[:-1]]
        val >>= 8
      elif expr.startswith("0x"):
        val += int(expr[2:], 16)
      else:
        val += int(expr)
      result[addr] = val
      addr += 1
    elif line[:3] == "lda":
      addr += 2
  return result

def build(lines, rom):
  labels = dict()
  comp(lines, labels, 0)
  # for label in labels.keys():
  #   print(label, hex(labels[label]))
  mem = comp(lines, labels, 1)
  for addr in mem:
    if addr<0xC000:
      continue
    rom[addr - 0xC000] = mem[addr]
