from sta import stat

def parse(s: str) -> list[str]:
  if s == "":
    return []
  if s[0] in [" ", "\n", "\t"]:
    return parse(s[1:])
  if s[:2] == "//":
    return parse(s[s.find("\n")+1:])
  if s[:2] == "/*":
    return parse(s[s.find("*/")+2:])
  if s[:2] in ["<<", ">>", ":=", "+=", "-=", "*=", "/=", "&=", "|=", "^=", "<=", ">=", "==", "!="]:
    return [s[:2]] + parse(s[2:])
  if s[0] in ",:.()+-*/^&|=<>[];{}":
    return [s[0]] + parse(s[1:])
  if s[0] == "\"":
    n = s[0]
    s = s[1:]
    while s[0] != "\"":
      n += s[0]
      s = s[1:]
    return [n] + parse(s[1:])
  if s[0].isalnum() or s[0] == "_":
    n = ""
    while s[0].isalnum() or s[0] == "_":
      n += s[0]
      s = s[1:]
    return [n] + parse(s)
  raise ValueError(s)

def find_lines(tokens: list[str]) -> list[list[str]]:
  lines = []
  while tokens:
    s = stat(tokens)
    if s < 1:
      raise ValueError(s, tokens)
    lines.append(tokens[:s])
    tokens = tokens[s+1:]
  return lines
  